from typing import Optional

from sqlalchemy import delete as sql_delete, select, update as sql_update
from sqlalchemy.ext.asyncio import AsyncSession

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
