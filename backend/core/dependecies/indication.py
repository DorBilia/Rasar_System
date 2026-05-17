from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Repositories.indication import SoldierIndicationRepository, IndicationTypeRepository, \
    OrganizationIndicationRepository
from Repositories.Interfaces.indication import ISoldierIndicationRepo
from Services.indication import SoldierIndicationService, OrganizationIndicationService, IndicationService
from Services.Interfaces.indication import ISoldierIndicationService, IOrganizationIndicationService

from db.db import get_db


async def get_soldier_indication_repository(db: AsyncSession = Depends(get_db)) -> ISoldierIndicationRepo:
    return SoldierIndicationRepository(db)


async def get_indication_type_repository(db: AsyncSession = Depends(get_db)) -> IndicationTypeRepository:
    return IndicationTypeRepository(db)


async def get_organization_indication_repository(
        db: AsyncSession = Depends(get_db)) -> OrganizationIndicationRepository:
    return OrganizationIndicationRepository(db)


async def get_indication_service(
        type_repository: IndicationTypeRepository = Depends(
            get_indication_type_repository)) -> IndicationService:
    return IndicationService(type_repository)


async def get_soldier_indication_service(
        repository: ISoldierIndicationRepo = Depends(
            get_soldier_indication_repository), ) -> ISoldierIndicationService:
    return SoldierIndicationService(repository)


async def get_organization_indication_service(
        repository: OrganizationIndicationRepository = Depends(get_organization_indication_repository)):
    return OrganizationIndicationService(repository)
