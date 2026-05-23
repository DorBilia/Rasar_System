from Repositories.Interfaces.baseRepo import IBaseRepo
from db.models.indications import Indication, IndicationType, OrganizationIndication
from typing import Sequence, NamedTuple
from datetime import date
from abc import abstractmethod
from core.enums import IndicationDescriptionEnum


class ISoldierIndicationRepo(IBaseRepo[Indication]):

    @abstractmethod
    async def get_by_indication_type(self, indication_type: IndicationType) -> Sequence[Indication]:
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
