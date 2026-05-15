from abc import ABC, abstractmethod
from typing import Sequence

from db.models.indications import Indication, IndicationType


class IIndicationService(ABC):
    @abstractmethod
    async def get_by_indication_type(self, indication_type: IndicationType) -> Sequence[Indication]:
        pass

    @abstractmethod
    async def can_soldier_attend_misdar(self, soldier_id: int, misdar_id: int) -> bool:
        pass
