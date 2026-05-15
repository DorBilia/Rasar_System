from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Repositories.indication import IndicationRepository, IndicationTypeRepository
from Repositories.Interfaces.indication import IIndicationRepo
from Services.indication import IndicationService
from Services.Interfaces.indication import IIndicationService

from db.db import get_db


async def get_indication_repository(db: AsyncSession = Depends(get_db)) -> IIndicationRepo:
    return IndicationRepository(db)


async def get_indication_type_repository(db: AsyncSession = Depends(get_db)) -> IndicationTypeRepository:
    return IndicationTypeRepository(db)


async def get_indication_service(
    repository: IIndicationRepo = Depends(get_indication_repository),
) -> IIndicationService:
    return IndicationService(repository)
