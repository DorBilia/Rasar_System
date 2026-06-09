import uuid
from datetime import date, datetime, timedelta, timezone
from typing import Optional

from jwt import PyJWTError
from starlette.authentication import AuthenticationError

from API.schemas.admin import AdminCreateUserRequest, AdminUpdateUserRequest, AdminUserResponse
from API.schemas.auth import AuthRequest, TokenResponse, UserResponse, AuthCredentials
from core.enums import RoleNameEnum
from core.security import create_access_token, generate_raw_refresh_token, hash_refresh_token, decode_access_token, \
    generate_csrf_token, verify_and_extract_signed_token
from core.security import hash_password, verify_password
from Repositories.Interfaces.refresh_token import IRefreshTokenRepo
from Repositories.Interfaces.user import IUserRepo
from Services.Interfaces.user import IUserService
from settings import settings


def _utcnow() -> datetime:
    return datetime.now()


class UserService(IUserService):

    def __init__(
            self,
            user_repo: IUserRepo,
            refresh_repo: IRefreshTokenRepo):
        self.user_repo = user_repo
        self.refresh_repo = refresh_repo

    async def register(self, register: AuthRequest) -> UserResponse:
        existing = await self.user_repo.get_by_email(register.email)
        if existing is not None:
            raise ValueError("user_exists")

        # Make the first user the admin
        n = await self.user_repo.count_users()
        role = RoleNameEnum.ADMIN if n == 0 else RoleNameEnum.VIEWER

        await self.user_repo.create(
            uuid=str(uuid.uuid4()),
            email=register.email,
            password_hash=hash_password(register.password),
            role=role,
            is_active=True,
            created_at=date.today())
        created = await self.user_repo.get_by_email(register.email)
        assert created is not None
        return UserResponse.model_validate(created)

    async def issue_tokens(self, user) -> TokenResponse:
        role_member_name = user.role.name
        access = create_access_token(subject=user.uuid, role_member_name=role_member_name)
        raw_refresh = generate_raw_refresh_token()
        h = hash_refresh_token(raw_refresh)
        exp = _utcnow() + timedelta(seconds=settings.REFRESH_TOKEN_EXPIRES_SECONDS)

        await self.refresh_repo.create(token_hash=h, user_uuid=user.uuid, expires_at=exp)

        csrf_token = generate_csrf_token()

        return TokenResponse(
            accessToken=access,
            refreshToken=raw_refresh,
            csrf_token=csrf_token)

    async def login(self, login: AuthRequest) -> Optional[TokenResponse]:
        user = await self.user_repo.get_by_email(login.email)
        if user is None or not user.is_active:
            return None
        if not verify_password(login.password, user.password_hash):
            return None
        return await self.issue_tokens(user)

    async def refresh(self, refresh_token: str, signed_csrf_token: str) -> TokenResponse:
        h = hash_refresh_token(refresh_token)
        current_token = await self.refresh_repo.get_by_hash(h)
        if current_token is None or not verify_and_extract_signed_token(signed_csrf_token):
            raise ValueError("invalid_refresh")
        if current_token.expires_at < _utcnow():
            await self.revoke(refresh_token)
            raise ValueError("invalid_refresh")

        await self.refresh_repo.delete_by_hash(h)

        user = await self.user_repo.get_by_uuid(current_token.user_uuid)
        if user is None or not user.is_active:
            raise ValueError("invalid_refresh")

        return await self.issue_tokens(user)

    async def revoke(self, refresh_token: str) -> None:
        h = hash_refresh_token(refresh_token)
        await self.refresh_repo.delete_by_hash(h)

    async def authenticate_user(self, creds: AuthCredentials) -> UserResponse:

        if creds is None or creds.scheme != "bearer":
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

    async def verify_admin(self, creds: AuthCredentials) -> bool:
        user = await self.authenticate_user(creds)
        return user.role == RoleNameEnum.ADMIN

    async def create_user(self, request: AdminCreateUserRequest) -> AdminUserResponse:
        existing = await self.user_repo.get_by_email(request.email)
        if existing is not None:
            raise ValueError("user_exists")

        await self.user_repo.create(
            uuid=str(uuid.uuid4()),
            email=request.email,
            password_hash=hash_password(request.password),
            role=request.role,
            is_active=request.is_active,
            created_at=date.today(),
        )
        created = await self.user_repo.get_by_email(request.email)
        assert created is not None
        return AdminUserResponse.model_validate(created)

    async def update_user(
            self,
            user_uuid: str,
            request: AdminUpdateUserRequest,
            actor_uuid: str,
    ) -> AdminUserResponse:
        user = await self.user_repo.get_by_uuid(user_uuid)
        if user is None:
            raise ValueError("user_not_found")

        if user_uuid == actor_uuid:
            if request.role is not None and request.role != user.role:
                raise ValueError("cannot_change_own_role")
            if request.is_active is False:
                raise ValueError("cannot_deactivate_self")

        updates: dict = {}
        if request.email is not None:
            if request.email != user.email:
                existing = await self.user_repo.get_by_email(request.email)
                if existing is not None:
                    raise ValueError("user_exists")
            updates["email"] = request.email
        if request.password is not None:
            updates["password_hash"] = hash_password(request.password)
        if request.role is not None:
            updates["role"] = request.role
        if request.is_active is not None:
            updates["is_active"] = request.is_active

        if not updates:
            return AdminUserResponse.model_validate(user)

        updated = await self.user_repo.update_by_uuid(user_uuid, **updates)
        assert updated is not None
        return AdminUserResponse.model_validate(updated)

    async def delete_user(self, user_uuid: str, actor_uuid: str) -> bool:
        if user_uuid == actor_uuid:
            raise ValueError("cannot_delete_self")
        return await self.user_repo.delete_by_uuid(user_uuid)

    async def get_user_by_email(self, email: str) -> Optional[AdminUserResponse]:
        user = await self.user_repo.get_by_email(email)
        if user is None:
            return None
        return AdminUserResponse.model_validate(user)

    async def get_users(self) -> list[AdminUserResponse]:
        users = await self.user_repo.get_all()
        return [AdminUserResponse.model_validate(user) for user in users]
