from Repositories.Interfaces.baseRepo import IBaseRepo
from db.models.biror import Biror
from typing import Sequence
from abc import abstractmethod


class IBirorRepo(IBaseRepo[Biror]):

    @abstractmethod
    async def get_for_soldier(self, soldier_id: int) -> Sequence[Biror]:
        pass

    @abstractmethod
    async def get_by_result(self, result: str) -> Sequence[Biror]:
        pass