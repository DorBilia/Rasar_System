from Repositories.Interfaces.baseRepo import IBaseRepo
from db.models.biror import Biror
from typing import Sequence
from abc import abstractmethod


class IBirorRepo(IBaseRepo[Biror]):
    @abstractmethod
    async def get_by_type(self, biror_type: int) -> Sequence[Biror]:
        pass
