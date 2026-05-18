from abc import ABC, abstractmethod
from typing import Optional, Sequence
from API.schemas.indication import *


class IIndicationService(ABC):
    @abstractmethod
    async def get_types(self) -> List[IndicationType]:
        pass


class ISoldierIndicationService(ABC):

    @abstractmethod
    async def get_by_indication_type(self, indication_type: IndicationType) -> Sequence[SoldierIndicationResponse]:
        pass

    @abstractmethod
    async def can_soldier_attend_misdar(self, soldier_id: int, misdar_id: int) -> bool:
        pass

    @abstractmethod
    async def create(self, request: SoldierIndicationRequest) -> SoldierIndicationResponse:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[SoldierIndicationResponse]:
        pass

    @abstractmethod
    async def create_many(self, requests: List[SoldierIndicationRequest]):
        pass


class IOrganizationIndicationService(ABC):
    @abstractmethod
    async def create(self, request: OrganizationIndicationRequest) -> OrganizationIndicationResponse:
        pass

    @abstractmethod
    async def get_all(self) -> Sequence[OrganizationIndicationMinimal]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[OrganizationIndicationResponse]:
        pass

    @abstractmethod
    async def get_by_indication_type(self, indication_type: IndicationType) -> Sequence[OrganizationIndicationResponse]:
        pass
