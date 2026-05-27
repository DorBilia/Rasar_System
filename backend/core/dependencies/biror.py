from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Repositories.biror import BirorRepository, BirorTypeRepository, BirorResultRepository
from Repositories.Interfaces.biror import IBirorRepo
from Services.biror import BirorService
from Services.Interfaces.biror import IBirorService

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
