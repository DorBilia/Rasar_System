from typing import Sequence

from sqlalchemy.orm import selectinload

from db.models.indications import Indication, IndicationType, IndicationTypeMisdarType
from Repositories.AbstractRepo import AbstractRepo
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from Repositories.Interfaces.indication import IIndicationRepo


class IndicationRepository(AbstractRepo[Indication], IIndicationRepo):
    async def get_by_indication_type(self, indication_type: IndicationType) -> Sequence[Indication]:
        stmt = (
            select(Indication)
            .where(Indication.indication_type == indication_type.id)
            .options(selectinload(Indication.soldier)))
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def can_soldier_attend_misdar(self, soldier_id: int, misdar_id: int) -> bool:
        stmt = (
            select(Indication)
            .join(IndicationType, Indication.indication_type == IndicationType.id)
            .join(
                IndicationTypeMisdarType,
                IndicationType.id == IndicationTypeMisdarType.indication_type_id,
            )
            .where(
                Indication.soldier_id == soldier_id,
                IndicationTypeMisdarType.misdar_type_id == misdar_id,
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().first() is not None

    def __init__(self, db: AsyncSession):
        super().__init__(db, Indication)


class IndicationTypeRepository(AbstractRepo[IndicationType]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, IndicationType)
