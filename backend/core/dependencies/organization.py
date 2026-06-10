from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_db
from Repositories.organization import BranchRepository, SectionRepository, UnitRepository
from Services.Interfaces.organization import IBranchService, ISectionService, IUnitService
from Services.organization import BranchService, SectionService, UnitService


async def get_unit_repository(db: AsyncSession = Depends(get_db)) -> UnitRepository:
    return UnitRepository(db)


async def get_branch_repository(db: AsyncSession = Depends(get_db)) -> BranchRepository:
    return BranchRepository(db)


async def get_section_repository(db: AsyncSession = Depends(get_db)) -> SectionRepository:
    return SectionRepository(db)


async def get_unit_service(
    repository: UnitRepository = Depends(get_unit_repository),
) -> IUnitService:
    return UnitService(repository)


async def get_branch_service(
    repository: BranchRepository = Depends(get_branch_repository),
) -> IBranchService:
    return BranchService(repository)


async def get_section_service(
    repository: SectionRepository = Depends(get_section_repository),
) -> ISectionService:
    return SectionService(repository)
