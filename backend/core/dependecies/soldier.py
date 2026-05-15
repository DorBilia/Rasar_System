from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Services.soldier import SoldierService
from Services.Interfaces.soldier import ISoldierService
from Repositories.soldier import SoldierRepository
from Repositories.Interfaces.soldier import ISoldierRepo

from db.db import get_db


async def get_soldier_repository(db: AsyncSession = Depends(get_db)) -> ISoldierRepo:
    return SoldierRepository(db)


async def get_soldier_service(repository: ISoldierRepo = Depends(get_soldier_repository)) -> ISoldierService:
    return SoldierService(repository)
