from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.enums import RoleNameEnum
from db.models.users import Role
from Repositories.Interfaces.role import IRoleRepo


class RoleRepository(IRoleRepo):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_role_name(self, role_name: RoleNameEnum) -> Optional[Role]:
        q = select(Role).where(Role.role_name == role_name)
        r = await self.db.execute(q)
        return r.scalar_one_or_none()
