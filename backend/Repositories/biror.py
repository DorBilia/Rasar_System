from typing import Sequence
from db.models.biror import Biror, BirorType, BirorResult
from Repositories.AbstractRepo import AbstractRepo
from Repositories.Interfaces.biror import IBirorRepo
from sqlalchemy.ext.asyncio import AsyncSession


class BirorRepository(AbstractRepo[Biror], IBirorRepo):

    async def get_by_result(self, result: str) -> Sequence[Biror]:
        pass

    def __init__(self, db: AsyncSession):
        super().__init__(db, Biror)


class BirorTypeRepository(AbstractRepo[BirorType]):
    # This doesn't have any unique functions... yet
    def __init__(self, db: AsyncSession):
        super().__init__(db, BirorType)


class BirorResultRepository(AbstractRepo[BirorResult]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, BirorResult)
