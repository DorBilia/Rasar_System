from Repositories.Interfaces.baseRepo import IBaseRepo
from db.models.indications import Indication, IndicationType, OrganizationIndication
from typing import Optional, Sequence, NamedTuple
from datetime import date
from abc import abstractmethod


class ISoldierIndicationRepo(IBaseRepo[Indication]):

    @abstractmethod
    async def get_by_indication_type(self, indication_type: int) -> Sequence[Indication]:
        pass

    @abstractmethod
    async def can_soldier_attend_misdar(self, soldier_id: int, misdar_id: int) -> bool:
        pass


class IOrganizationIndicationRepo(IBaseRepo[OrganizationIndication]):

    @abstractmethod
    async def get_all_with_soldiers(self) -> Sequence[OrganizationIndication]:
        """Gets the organization indication and all the additional soldiers of it"""
        pass

    @abstractmethod
    async def get_soldier_ids_by_organization_id(self, organization_id: int) -> Sequence[int]:
        pass

    @abstractmethod
    async def get_by_indication_type(self, indication_type: IndicationType) -> Sequence[Indication]:
        pass


class IIndicationTypeRepo(IBaseRepo[IndicationType]):
    @abstractmethod
    async def get_all_with_mappings(self) -> Sequence[IndicationType]:
        pass

    @abstractmethod
    async def get_by_id_with_mappings(self, entity_id: int) -> Optional[IndicationType]:
        pass

    @abstractmethod
    async def create_with_misdars(
            self,
            indication_description: str,
            weekly_arrivals: int,
            misdar_type_ids: Optional[list[int]]) -> Optional[IndicationType]:
        pass

    @abstractmethod
    async def update_with_misdars(
            self,
            entity_id: int,
            *,
            indication_description: Optional[str],
            weekly_arrivals: Optional[int] = None,
            misdar_type_ids: Optional[list[int]] = None,
    ) -> Optional[IndicationType]:
        pass
