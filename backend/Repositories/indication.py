from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.indications import Indication, IndicationType, IndicationTypeMisdarType, OrganizationIndication
from Repositories.AbstractRepo import AbstractRepo
from Repositories.Interfaces.indication import ISoldierIndicationRepo, IOrganizationIndicationRepo


class SoldierIndicationRepository(AbstractRepo[Indication], ISoldierIndicationRepo):
    async def get_by_indication_type(self, indication_type: IndicationType) -> Sequence[Indication]:
        stmt = (
            select(Indication)
            .where(Indication.indication_type == indication_type.id))
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_for_soldier(self, soldier_id: int) -> Sequence[Indication]:
        """Also return the indication info"""
        query = (
            select(self.model)
            .where(self.model.soldier_id == soldier_id)
            .options(selectinload(Indication.indication_type_ref))
        )
        result = await self.db.execute(query)
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


class OrganizationIndicationRepository(AbstractRepo[OrganizationIndication], IOrganizationIndicationRepo):

    def __init__(self, db: AsyncSession):
        super().__init__(db, OrganizationIndication)

    async def get_all_with_soldiers(self) -> Sequence[OrganizationIndication]:
        stmt = (select(OrganizationIndication)
                .options(selectinload(OrganizationIndication.indications)))
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_soldier_ids_by_organization_id(self, organization_id: int) -> Sequence[int]:
        stmt = select(Indication.soldier_id).where(
            Indication.organization_id == organization_id
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_indication_type(self, indication_type: IndicationType) -> Sequence[Indication]:
        stmt = (
            select(OrganizationIndication)
            .where(OrganizationIndication.indication_type == indication_type.id))
        result = await self.db.execute(stmt)
        return result.scalars().all()
