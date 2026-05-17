from baseRepo import IBaseRepo
from db.models.indications import Indication, IndicationType, OrganizationIndication
from typing import Sequence
from abc import abstractmethod


class ISoldierIndicationRepo(IBaseRepo[Indication]):

    @abstractmethod
    async def get_by_indication_type(self, indication_type: IndicationType) -> Sequence[Indication]:
        pass

    @abstractmethod
    async def can_soldier_attend_misdar(self, soldier_id: int, misdar_id: int) -> bool:
        pass


class IOrganizationIndicationRepo(IBaseRepo[OrganizationIndication]):

    @abstractmethod
    async def get_by_indication_type(self, indication_type: IndicationType) -> Sequence[Indication]:
        pass
