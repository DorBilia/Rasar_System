from abc import ABC, abstractmethod
from typing import Sequence

from db.models.biror import Biror


class IBirorService(ABC):
    @abstractmethod
    async def get_by_result(self, biror_result: str) -> Sequence[Biror]:
        pass
