from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Services.soldier import SoldierService
from Services.Interfaces.soldier import ISoldierService
from Services.Interfaces.indication import IIndicationService, ISoldierIndicationService
from Repositories.doh1 import Doh1Repository
from Repositories.Interfaces.doh1 import IDoh1Repo
from Repositories.soldier import SoldierRepository
from Repositories.Interfaces.soldier import ISoldierRepo

from db.db import get_db


__all__ = [
    "get_soldier_repository",
    "get_doh1_repository",
    "get_soldier_service",
]

async def get_soldier_repository(db: AsyncSession = Depends(get_db)) -> ISoldierRepo:
    return SoldierRepository(db)


async def get_doh1_repository(db: AsyncSession = Depends(get_db)) -> IDoh1Repo:
    return Doh1Repository(db)

from .indication import get_indication_service, get_soldier_indication_service

async def get_soldier_service(
        repository: ISoldierRepo = Depends(get_soldier_repository),
        doh1_repository: IDoh1Repo = Depends(get_doh1_repository),
        indication_service: IIndicationService = Depends(get_indication_service),
        soldier_indication_service: ISoldierIndicationService = Depends(get_soldier_indication_service),
) -> ISoldierService:
    return SoldierService(repository, doh1_repository, indication_service, soldier_indication_service)
