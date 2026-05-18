from Repositories.Interfaces.baseRepo import IBaseRepo
from db.models.indications import Indication, IndicationType, OrganizationIndication
from typing import Sequence, NamedTuple
from datetime import date
from abc import abstractmethod
from core.enums import IndicationDescriptionEnum


class OrganizationIndicationMinimalRow(NamedTuple):
    id: int
    indication_description: IndicationDescriptionEnum
    start_date: date
    end_date: date
    soldiers_affected: int


class ISoldierIndicationRepo(IBaseRepo[Indication]):

    @abstractmethod
    async def get_by_indication_type(self, indication_type: IndicationType) -> Sequence[Indication]:
        pass

    @abstractmethod
    async def can_soldier_attend_misdar(self, soldier_id: int, misdar_id: int) -> bool:
        pass


class IOrganizationIndicationRepo(IBaseRepo[OrganizationIndication]):

    @abstractmethod
    async def get_all_minimal(self) -> Sequence[OrganizationIndicationMinimalRow]:
        pass

    @abstractmethod
    async def get_soldier_ids_by_organization_id(self, organization_id: int) -> Sequence[int]:
        pass

    @abstractmethod
    async def get_by_indication_type(self, indication_type: IndicationType) -> Sequence[Indication]:
        pass
