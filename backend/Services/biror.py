from typing import Sequence

from Repositories.Interfaces.biror import IBirorRepo
from Services.Interfaces.biror import IBirorService
from db.models import Biror


class BirorService(IBirorService):
    def __init__(self, repository: IBirorRepo) -> None:
        self._repository = repository

    async def get_by_result(self, biror_result: str) -> Sequence[Biror]:
        return await self._repository.get_by_result(biror_result)
