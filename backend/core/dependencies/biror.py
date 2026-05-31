from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Repositories.biror import BirorRepository, BirorTypeRepository, BirorResultRepository
from Repositories.Interfaces.biror import IBirorRepo
from Services.biror import BirorService, BirorTypeService
from Services.Interfaces.biror import IBirorService, IBirorTypeService

from db.db import get_db


async def get_biror_repository(db: AsyncSession = Depends(get_db)) -> IBirorRepo:
    return BirorRepository(db)


async def get_biror_type_repository(db: AsyncSession = Depends(get_db)) -> BirorTypeRepository:
    return BirorTypeRepository(db)


async def get_biror_result_repository(db: AsyncSession = Depends(get_db)) -> BirorResultRepository:
    return BirorResultRepository(db)


async def get_biror_service(
    repository: IBirorRepo = Depends(get_biror_repository),
) -> IBirorService:
    return BirorService(repository)


async def get_biror_type_service(
    repository: BirorTypeRepository = Depends(get_biror_type_repository),
) -> IBirorTypeService:
    return BirorTypeService(repository)
