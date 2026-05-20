import uuid
from datetime import date, datetime, timedelta, timezone
from typing import Optional

from fastapi.security import HTTPAuthorizationCredentials
from jwt import PyJWTError
from starlette.authentication import AuthenticationError

from API.schemas.auth import RegisterRequest, TokenRequest, TokenResponse, UserResponse
from core.enums import RoleNameEnum
from core.security import create_access_token, generate_raw_refresh_token, hash_refresh_token, decode_access_token
from core.security import hash_password, verify_password
from Repositories.Interfaces.refresh_token import IRefreshTokenRepo
from Repositories.Interfaces.role import IRoleRepo
from Repositories.Interfaces.soldier import ISoldierRepo
from Repositories.Interfaces.user import IUserRepo
from Services.Interfaces.user import IUserService
from settings import settings


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class UserService(IUserService):

    def __init__(
            self,
            user_repo: IUserRepo,
            role_repo: IRoleRepo,
            refresh_repo: IRefreshTokenRepo,
            soldier_repo: ISoldierRepo):
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.refresh_repo = refresh_repo
        self.soldier_repo = soldier_repo

    async def register(self, register: RegisterRequest) -> UserResponse:
        soldier = await self.soldier_repo.get_by_id(register.soldier_id)
        if soldier is None:
            raise ValueError("soldier_not_found")

        existing = await self.user_repo.get_by_soldier_id(register.soldier_id)
        if existing is not None:
            raise ValueError("user_exists")

        # Make the first user the admin
        n = await self.user_repo.count_users()
        role_enum = RoleNameEnum.ADMIN if n == 0 else RoleNameEnum.VIEWER
        role = await self.role_repo.get_by_role_name(role_enum)
        if role is None:
            raise RuntimeError(
                f"Role {role_enum.name} is missing in the database; seed roles first."
            )

        await self.user_repo.create(
            uuid=str(uuid.uuid4()),
            soldier_id=register.soldier_id,
            password_hash=hash_password(register.password),
            role_id=role.id,
            is_active=True,
            created_at=date.today())
        created = await self.user_repo.get_by_soldier_id(register.soldier_id)
        assert created is not None
        return UserResponse.model_validate(created)

    async def issue_token_pair(self, user) -> TokenResponse:
        role_member_name = user.role.role_name.name
        access, expires_in = create_access_token(subject=user.uuid, role_member_name=role_member_name)
        raw_refresh = generate_raw_refresh_token()
        h = hash_refresh_token(raw_refresh)
        exp = _utcnow() + timedelta(seconds=settings.REFRESH_TOKEN_EXPIRES_SECONDS)
        await self.refresh_repo.create(token_hash=h, user_uuid=user.uuid, expires_at=exp)
        return TokenResponse(
            accessToken=access,
            expiresIn=expires_in,
            refreshToken=raw_refresh)

    async def login(self, login: TokenRequest) -> Optional[TokenResponse]:
        user = await self.user_repo.get_by_soldier_id(login.soldier_id)
        if user is None or not user.is_active:
            return None
        if not verify_password(login.password, user.password_hash):
            return None
        return await self.issue_token_pair(user)

    async def refresh(self, refresh_token: str) -> TokenResponse:
        h = hash_refresh_token(refresh_token)
        current_token = await self.refresh_repo.get_by_hash(h)
        if current_token is None:
            raise ValueError("invalid_refresh")

        await self.refresh_repo.delete_by_hash(h)

        user = await self.user_repo.get_by_uuid(current_token.user_uuid)
        if user is None or not user.is_active:
            raise ValueError("invalid_refresh")

        return await self.issue_token_pair(user)

    async def revoke(self, refresh_token: str) -> None:
        h = hash_refresh_token(refresh_token)
        await self.refresh_repo.delete_by_hash(h)

    async def authenticate_user(self, creds: HTTPAuthorizationCredentials) -> UserResponse:

        if creds is None or creds.scheme.lower() != "bearer":
            raise AuthenticationError()

        try:
            payload = decode_access_token(creds.credentials)

        except PyJWTError:
            raise AuthenticationError()

        sub = payload.get("sub")
        if not isinstance(sub, str):
            raise AuthenticationError()

        user = await self.user_repo.get_by_uuid(sub)
        if user is None or not user.is_active:
            raise AuthenticationError()

        return UserResponse.model_validate(user)
