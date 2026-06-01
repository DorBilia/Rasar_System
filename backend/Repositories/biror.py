from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db.models.biror import Biror, BirorType, BirorResult
from Repositories.AbstractRepo import AbstractRepo
from Repositories.Interfaces.biror import IBirorRepo
from sqlalchemy.ext.asyncio import AsyncSession


class BirorRepository(AbstractRepo[Biror], IBirorRepo):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Biror)

    async def get_by_type(self, biror_type: int) -> Sequence[Biror]:
        stmt = (select(Biror)
                .where(Biror.biror_type == biror_type)
                .options(selectinload(Biror.biror_result_ref)))
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_uuid(self, entity_uuid: str) -> Optional[Biror]:
        stmt = (
            select(Biror)
            .where(Biror.uuid == entity_uuid)
            .options(selectinload(Biror.biror_result_ref))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_for_soldier(self, soldier_id: int) -> Sequence[Biror]:
        stmt = (
            select(Biror)
            .where(Biror.soldier_id == soldier_id)
            .options(selectinload(Biror.biror_result_ref))
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_result(self, biror_result: int) -> Sequence[Biror]:
        stmt = (
            select(Biror)
            .where(Biror.biror_result == biror_result)
            .options(selectinload(Biror.biror_result_ref))
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()


class BirorTypeRepository(AbstractRepo[BirorType]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, BirorType)


class BirorResultRepository(AbstractRepo[BirorResult]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, BirorResult)
