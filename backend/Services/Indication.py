from typing import Sequence

from db.models.indications import Indication, IndicationType
from Repositories.Interfaces.indication import IIndicationRepo
from Services.Interfaces.indication import IIndicationService


class IndicationService(IIndicationService):
    def __init__(self, repository: IIndicationRepo) -> None:
        self._repository = repository

    async def get_by_indication_type(self, indication_type: IndicationType) -> Sequence[Indication]:
        return await self._repository.get_by_indication_type(indication_type)

    async def can_soldier_attend_misdar(self, soldier_id: int, misdar_id: int) -> bool:
        return await self._repository.can_soldier_attend_misdar(soldier_id, misdar_id)
