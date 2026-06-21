from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.biror import Biror, BirorType
from Repositories.AbstractRepo import AbstractRepo
from Repositories.Interfaces.biror import IBirorRepo


class BirorRepository(AbstractRepo[Biror], IBirorRepo):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Biror)

    async def get_by_type(self, biror_type: int) -> Sequence[Biror]:
        stmt = select(Biror).where(Biror.biror_type == biror_type)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_uuid(self, entity_uuid: str) -> Optional[Biror]:
        stmt = select(Biror).where(Biror.uuid == entity_uuid)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_for_soldier(self, soldier_id: int) -> Sequence[Biror]:
        stmt = select(Biror).where(Biror.soldier_id == soldier_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()


class BirorTypeRepository(AbstractRepo[BirorType]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, BirorType)
