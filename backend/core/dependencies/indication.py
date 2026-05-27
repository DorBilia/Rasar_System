from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from Repositories.indication import SoldierIndicationRepository, IndicationTypeRepository, \
    OrganizationIndicationRepository
from Repositories.Interfaces.indication import IIndicationTypeRepo, ISoldierIndicationRepo, IOrganizationIndicationRepo
from Repositories.Interfaces.misdar import IMisdarTypeRepo
from Services.indication import SoldierIndicationService, OrganizationIndicationService, IndicationService
from Services.Interfaces.indication import ISoldierIndicationService, IOrganizationIndicationService
from db.db import get_db


async def get_soldier_indication_repository(db: AsyncSession = Depends(get_db)) -> ISoldierIndicationRepo:
    return SoldierIndicationRepository(db)


async def get_indication_type_repository(db: AsyncSession = Depends(get_db)) -> IIndicationTypeRepo:
    return IndicationTypeRepository(db)


async def get_organization_indication_repository(
        db: AsyncSession = Depends(get_db)) -> OrganizationIndicationRepository:
    return OrganizationIndicationRepository(db)

from .misdar import get_misdar_type_repository

async def get_indication_service(
        type_repository: IIndicationTypeRepo = Depends(get_indication_type_repository),
        misdar_type_repository: IMisdarTypeRepo = Depends(get_misdar_type_repository)) -> IndicationService:
    return IndicationService(type_repository, misdar_type_repository)


async def get_soldier_indication_service(
        soldier_repository: ISoldierIndicationRepo = Depends(get_soldier_indication_repository),
        org_repo: IOrganizationIndicationRepo = Depends(
            get_organization_indication_repository)) -> ISoldierIndicationService:
    return SoldierIndicationService(soldier_repository, org_repo)


async def get_organization_indication_service(
        repository: IOrganizationIndicationRepo = Depends(get_organization_indication_repository),
        soldier_indication_service: ISoldierIndicationService = Depends(
            get_soldier_indication_service)) -> IOrganizationIndicationService:
    return OrganizationIndicationService(repository, soldier_indication_service)
