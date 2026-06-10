from API.schemas.organization import *
from typing import List, Optional
from Repositories.organization import BranchRepository, SectionRepository, UnitRepository
from Services.Interfaces.organization import IBranchService, ISectionService, IUnitService


class UnitService(IUnitService):
    def __init__(self, repository: UnitRepository) -> None:
        self._repository = repository

    async def get_all(self) -> List[UnitSchema]:
        rows = await self._repository.get_all()
        return [UnitSchema.model_validate(r) for r in rows]

    async def get_by_id(self, unit_id: int) -> Optional[UnitSchema]:
        row = await self._repository.get_by_id(unit_id)
        if row is None:
            return None
        return UnitSchema.model_validate(row)

    async def create(self, request: CreateUnitRequest) -> UnitSchema:
        created = await self._repository.create(**request.model_dump())
        return UnitSchema.model_validate(created)

    async def update(self, unit_id: int, request: UpdateUnitRequest) -> Optional[UnitSchema]:
        payload = request.model_dump(exclude_unset=True)
        if not payload:
            return await self.get_by_id(unit_id)
        row = await self._repository.update(unit_id, **payload)
        if row is None:
            return None
        return UnitSchema.model_validate(row)

    async def delete(self, unit_id: int) -> bool:
        return await self._repository.delete(unit_id)


class BranchService(IBranchService):
    def __init__(self, repository: BranchRepository) -> None:
        self._repository = repository

    async def get_all(self) -> List[BranchSchema]:
        rows = await self._repository.get_all()
        return [BranchSchema.model_validate(r) for r in rows]

    async def get_by_id(self, branch_id: int) -> Optional[BranchSchema]:
        row = await self._repository.get_by_id(branch_id)
        if row is None:
            return None
        return BranchSchema.model_validate(row)

    async def create(self, request: CreateBranchRequest) -> BranchSchema:
        created = await self._repository.create(**request.model_dump())
        return BranchSchema.model_validate(created)

    async def update(self, branch_id: int, request: UpdateBranchRequest) -> Optional[BranchSchema]:
        payload = request.model_dump(exclude_unset=True)
        if not payload:
            return await self.get_by_id(branch_id)
        row = await self._repository.update(branch_id, **payload)
        if row is None:
            return None
        return BranchSchema.model_validate(row)

    async def delete(self, branch_id: int) -> bool:
        return await self._repository.delete(branch_id)


class SectionService(ISectionService):
    def __init__(self, repository: SectionRepository) -> None:
        self._repository = repository

    async def get_all(self) -> List[SectionSchema]:
        rows = await self._repository.get_all()
        return [SectionSchema.model_validate(r) for r in rows]

    async def get_by_id(self, section_id: int) -> Optional[SectionSchema]:
        row = await self._repository.get_by_id(section_id)
        if row is None:
            return None
        return SectionSchema.model_validate(row)

    async def create(self, request: CreateSectionRequest) -> SectionSchema:
        created = await self._repository.create(**request.model_dump())
        return SectionSchema.model_validate(created)

    async def update(self, section_id: int, request: UpdateSectionRequest) -> Optional[SectionSchema]:
        payload = request.model_dump(exclude_unset=True)
        if not payload:
            return await self.get_by_id(section_id)
        row = await self._repository.update(section_id, **payload)
        if row is None:
            return None
        return SectionSchema.model_validate(row)

    async def delete(self, section_id: int) -> bool:
        return await self._repository.delete(section_id)
