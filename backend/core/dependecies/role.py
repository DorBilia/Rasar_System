from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Repositories.Interfaces.role import IRoleRepo
from Repositories.role import RoleRepository
from db.db import get_db


async def get_role_repository(db: AsyncSession = Depends(get_db)) -> IRoleRepo:
    return RoleRepository(db)
