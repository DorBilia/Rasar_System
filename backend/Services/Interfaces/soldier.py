from abc import ABC, abstractmethod
from typing import Optional, Sequence

from API.schemas.soldier import BaseSoldier, FilterSoldiersRequest, FullSoldier, UpdateSoldierRequest


class ISoldierService(ABC):

    @abstractmethod
    async def create(self, soldier: FullSoldier) -> FullSoldier:
        pass

    @abstractmethod
    async def get_by_uuid(self, soldier_uuid: str) -> Optional[FullSoldier]:
        pass

    @abstractmethod
    async def get_all_filtered(self, filter_request: FilterSoldiersRequest) -> Sequence[BaseSoldier]:
        pass

    @abstractmethod
    async def update_soldier(self, soldier_uuid: str, updates: UpdateSoldierRequest) -> Optional[BaseSoldier]:
        pass

    @abstractmethod
    async def delete_soldier(self, soldier_uuid: str) -> bool:
        pass
