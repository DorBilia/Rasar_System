from abc import ABC, abstractmethod
from typing import Optional, Sequence

from API.schemas.soldier import *


class ISoldierService(ABC):

    @abstractmethod
    async def create(self, soldier: CreateSoldierRequest) -> FullSoldier:
        pass

    @abstractmethod
    async def get_by_uuid(self, soldier_uuid: str) -> Optional[FullSoldier]:
        pass

    @abstractmethod
    async def get_all_filtered(self, filter_request: FilterSoldiersRequest) -> Sequence[MinimalSoldier]:
        pass

    @abstractmethod
    async def update_soldier(self, soldier_uuid: str, updates: UpdateSoldierRequest) -> Optional[MinimalSoldier]:
        pass

    @abstractmethod
    async def delete_soldier(self, soldier_uuid: str) -> bool:
        pass

    @abstractmethod
    async def add_doh1_manual(self, request: Doh1Request) -> bool:
        pass