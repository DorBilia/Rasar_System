from baseRepo import IBaseRepo
from db.models.indications import Indication, IndicationType
from typing import Sequence
from abc import abstractmethod


class IIndicationRepo(IBaseRepo[Indication]):

    @abstractmethod
    def get_by_indication_type(self, indication_type: IndicationType) -> Sequence[Indication]:
        pass

    @abstractmethod
    def can_soldier_attend_misdar(self, misdar_id: int) -> bool:
        pass


