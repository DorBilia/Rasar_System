from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db.models.biror import Biror, BirorType, BirorResult
from Repositories.AbstractRepo import AbstractRepo
from Repositories.Interfaces.biror import IBirorRepo
from sqlalchemy.ext.asyncio import AsyncSession


class BirorRepository(AbstractRepo[Biror], IBirorRepo):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Biror)

    async def get_by_result(self, biror_result: int) -> Sequence[Biror]:
        stmt = (
            select(Biror)
            .where(Biror.biror_result == biror_result)
            .options(selectinload(Biror.soldier))
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()


class BirorTypeRepository(AbstractRepo[BirorType]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, BirorType)


class BirorResultRepository(AbstractRepo[BirorResult]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, BirorResult)
