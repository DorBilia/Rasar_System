from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.users import User
from Repositories.AbstractRepo import AbstractRepo
from Repositories.Interfaces.user import IUserRepo


class UserRepository(AbstractRepo[User], IUserRepo):

    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

    async def get_by_email(self, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def count_users(self) -> int:
        query = select(func.count()).select_from(User)
        result = await self.db.execute(query)
        return result.scalar_one()
