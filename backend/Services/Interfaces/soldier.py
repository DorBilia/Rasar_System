from abc import ABC, abstractmethod
from typing import Optional, Sequence

from API.schemas.soldier import *


class ISoldierService(ABC):

    @abstractmethod
    async def create(self, soldier: CreateSoldierRequest) -> FullSoldier:
        pass

    @abstractmethod
    async def get_by_id(self, soldier_id: int) -> Optional[FullSoldier]:
        pass

    @abstractmethod
    async def get_all_filtered(self, filter_request: FilterSoldiersRequest) -> FilterSoldiersResponse:
        """Gets all Active Soldiers according to a filter request"""
        pass

    @abstractmethod
    async def update_soldier(self, soldier_id: int, updates: UpdateSoldierRequest) -> Optional[MinimalSoldier]:
        pass

    @abstractmethod
    async def delete_soldier(self, soldier_id: int) -> bool:
        pass

    @abstractmethod
    async def add_doh1_manual(self, request: Doh1Request) -> bool:
        pass

    @abstractmethod
    async def handle_doh1_excel(self, file_bytes: bytes) -> bool:
        pass