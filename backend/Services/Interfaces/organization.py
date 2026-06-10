from abc import ABC, abstractmethod
from typing import List, Optional

from API.schemas.organization import *


class IUnitService(ABC):
    @abstractmethod
    async def get_all(self) -> List[UnitSchema]:
        pass

    @abstractmethod
    async def get_by_id(self, unit_id: int) -> Optional[UnitSchema]:
        pass

    @abstractmethod
    async def create(self, request: CreateUnitRequest) -> UnitSchema:
        pass

    @abstractmethod
    async def update(self, unit_id: int, request: UpdateUnitRequest) -> Optional[UnitSchema]:
        pass

    @abstractmethod
    async def delete(self, unit_id: int) -> bool:
        pass


class IBranchService(ABC):
    @abstractmethod
    async def get_all(self) -> List[BranchSchema]:
        pass

    @abstractmethod
    async def get_by_id(self, branch_id: int) -> Optional[BranchSchema]:
        pass

    @abstractmethod
    async def create(self, request: CreateBranchRequest) -> BranchSchema:
        pass

    @abstractmethod
    async def update(self, branch_id: int, request: UpdateBranchRequest) -> Optional[BranchSchema]:
        pass

    @abstractmethod
    async def delete(self, branch_id: int) -> bool:
        pass


class ISectionService(ABC):
    @abstractmethod
    async def get_all(self) -> List[SectionSchema]:
        pass

    @abstractmethod
    async def get_by_id(self, section_id: int) -> Optional[SectionSchema]:
        pass

    @abstractmethod
    async def create(self, request: CreateSectionRequest) -> SectionSchema:
        pass

    @abstractmethod
    async def update(self, section_id: int, request: UpdateSectionRequest) -> Optional[SectionSchema]:
        pass

    @abstractmethod
    async def delete(self, section_id: int) -> bool:
        pass
