import uuid
from datetime import date
from typing import Optional

from sqlalchemy import delete as sql_delete, select, update as sql_update
from sqlalchemy.ext.asyncio import AsyncSession

from API.schemas.user import Login, Register
from core.security import hash_password, verify_password
from db.models.users import User
from Repositories.AbstractRepo import AbstractRepo
from Repositories.Interfaces.user import IUserRepo


class UserRepository(AbstractRepo[User], IUserRepo):

    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

    async def get_by_id(self, entity_id: int) -> Optional[User]:
        return await self.get_by_soldier_id(entity_id)

    async def get_by_soldier_id(self, soldier_id: int) -> Optional[User]:
        query = select(User).where(User.soldier_id == soldier_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def register(self, command: Register) -> User:
        existing = await self.get_by_soldier_id(command.soldier_id)
        if existing is not None:
            raise ValueError(f"User already exists for soldier_id={command.soldier_id}")

        return await self.create(
            uuid=str(uuid.uuid4()),
            soldier_id=command.soldier_id,
            password_hash=hash_password(command.password),
            role_id=command.role_id,
            is_active=True,
            created_at=date.today(),
        )

    async def login(self, command: Login) -> Optional[User]:
        user = await self.get_by_soldier_id(command.soldier_id)
        if user is None or not user.is_active:
            return None
        if not verify_password(command.password, user.password_hash):
            return None
        return user

    async def update(self, entity_id: int, **updates) -> Optional[User]:
        query = (
            sql_update(User)
            .where(User.soldier_id == entity_id)
            .values(**updates)
            .execution_options(synchronize_session=False)
        )
        await self.db.execute(query)
        await self.db.commit()
        return await self.get_by_soldier_id(entity_id)

    async def update_by_uuid(self, entity_uuid: str, **updates) -> Optional[User]:
        query = (
            sql_update(User)
            .where(User.uuid == entity_uuid)
            .values(**updates)
            .execution_options(synchronize_session=False)
        )
        await self.db.execute(query)
        await self.db.commit()
        return await self.get_by_uuid(entity_uuid)

    async def delete(self, entity_id: int) -> bool:
        query = sql_delete(User).where(User.soldier_id == entity_id)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0
