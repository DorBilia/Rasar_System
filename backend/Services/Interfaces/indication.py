from abc import ABC, abstractmethod
from typing import Sequence
from API.schemas.indication import *


class IIndicationService(ABC):
    @abstractmethod
    async def get_types(self) -> List[IndicationTypeSchema]:
        pass

    @abstractmethod
    async def create_type(self, request: CreateIndicationTypeRequest) -> IndicationTypeSchema:
        pass

    @abstractmethod
    async def get_type_by_id(self, indication_type_id: int) -> Optional[IndicationTypeSchema]:
        pass

    @abstractmethod
    async def update_type(self, indication_type_id: int, request: UpdateIndicationTypeRequest) -> Optional[IndicationTypeSchema]:
        pass

    @abstractmethod
    async def delete_type(self, indication_type_id: int) -> bool:
        pass


class ISoldierIndicationService(ABC):

    @abstractmethod
    async def get_by_indication_type(self, indication_type: IndicationTypeSchema) -> Sequence[SoldierIndicationResponse]:
        pass

    @abstractmethod
    async def can_soldier_attend_misdar(self, soldier_id: int, misdar_id: int) -> bool:
        pass

    @abstractmethod
    async def create(self, request: SoldierIndicationRequest) -> SoldierIndicationResponse:
        pass

    @abstractmethod
    async def get_by_uuid(self, indication_uuid: str) -> Optional[SoldierIndicationResponse]:
        pass

    @abstractmethod
    async def create_many(self, requests: List[SoldierIndicationRequest]):
        pass

    @abstractmethod
    async def get_all_for_soldier(self, soldier_id: int) -> Sequence[SoldierIndicationWithDescription]:
        pass

    @abstractmethod
    async def delete(self, indication_uuid: str):
        pass


class IOrganizationIndicationService(ABC):
    @abstractmethod
    async def create(self, request: OrganizationIndicationRequest) -> OrganizationIndicationResponse:
        pass

    @abstractmethod
    async def get_all(self) -> Sequence[OrganizationIndicationMinimal]:
        pass

    @abstractmethod
    async def get_by_uuid(self, indication_uuid: str) -> Optional[OrganizationIndicationResponse]:
        pass

    @abstractmethod
    async def delete(self, indication_uuid: str):
        pass
