from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Repositories.biror import BirorRepository, BirorTypeRepository, BirorResultRepository
from Repositories.Interfaces.biror import IBirorRepo
from Services.biror import BirorResultService, BirorService, BirorTypeService
from Services.Interfaces.biror import IBirorResultService, IBirorService, IBirorTypeService

from db.db import get_db


__all__ = [
    "get_biror_repository",
    "get_biror_type_repository",
    "get_biror_result_repository",
    "get_biror_service",
    "get_biror_type_service",
    "get_biror_result_service",
]

async def get_biror_repository(db: AsyncSession = Depends(get_db)) -> IBirorRepo:
    return BirorRepository(db)


async def get_biror_type_repository(db: AsyncSession = Depends(get_db)) -> BirorTypeRepository:
    return BirorTypeRepository(db)


async def get_biror_result_repository(db: AsyncSession = Depends(get_db)) -> BirorResultRepository:
    return BirorResultRepository(db)


async def get_biror_service(
    repository: IBirorRepo = Depends(get_biror_repository),
    result_repository: BirorResultRepository = Depends(get_biror_result_repository),
) -> IBirorService:
    return BirorService(repository, result_repository)


async def get_biror_type_service(
    repository: BirorTypeRepository = Depends(get_biror_type_repository),
) -> IBirorTypeService:
    return BirorTypeService(repository)


async def get_biror_result_service(
    repository: BirorResultRepository = Depends(get_biror_result_repository),
    biror_repository: IBirorRepo = Depends(get_biror_repository),
) -> IBirorResultService:
    return BirorResultService(repository, biror_repository)
