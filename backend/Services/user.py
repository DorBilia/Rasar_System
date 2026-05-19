import uuid
from datetime import date
from typing import Optional

from API.schemas.user import Login, Register, UserResponse
from core.security import hash_password, verify_password
from Repositories.Interfaces.user import IUserRepo
from Services.Interfaces.user import IUserService


class UserService(IUserService):
    user_repo: IUserRepo

    def __init__(self, user_repo: IUserRepo):
        self.user_repo = user_repo

    async def register(self, register: Register) -> UserResponse:
        existing = await self.user_repo.get_by_soldier_id(register.soldier_id)
        if existing is not None:
            raise ValueError(f"User already exists for soldier_id={register.soldier_id}")

        created = await self.user_repo.create(
            uuid=str(uuid.uuid4()),
            soldier_id=register.soldier_id,
            password_hash=hash_password(register.password),
            role_id=register.role_id,
            is_active=True,
            created_at=date.today(),
        )
        return UserResponse.model_validate(created)

    async def login(self, login: Login) -> Optional[UserResponse]:
        user = await self.user_repo.get_by_soldier_id(login.soldier_id)
        if user is None or not user.is_active:
            return None
        if not verify_password(login.password, user.password_hash):
            return None
        return UserResponse.model_validate(user)
