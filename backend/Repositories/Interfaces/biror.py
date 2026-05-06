from base_repo import IBaseRepo
from db.models.biror import Biror, BirorType
from typing import Sequence
from abc import abstractmethod


class IBirorRepoI(IBaseRepo[Biror]):

    @abstractmethod
    async def get_for_soldier(self, soldier_id: int) -> Sequence[Biror]:
        pass

