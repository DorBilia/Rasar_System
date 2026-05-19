from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.indications import Indication, IndicationType, IndicationTypeMisdarType, OrganizationIndication
from Repositories.AbstractRepo import AbstractRepo
from Repositories.Interfaces.indication import (
    ISoldierIndicationRepo,
    IOrganizationIndicationRepo,
    OrganizationIndicationMinimalRow,
)


class SoldierIndicationRepository(AbstractRepo[Indication], ISoldierIndicationRepo):
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


class OrganizationIndicationRepository(AbstractRepo[OrganizationIndication], IOrganizationIndicationRepo):

    def __init__(self, db: AsyncSession):
        super().__init__(db, OrganizationIndication)

    async def get_all_minimal(self) -> Sequence[OrganizationIndicationMinimalRow]:
        stmt = (
            select(
                OrganizationIndication.id,
                OrganizationIndication.uuid,
                IndicationType.indication_description,
                OrganizationIndication.start_date,
                OrganizationIndication.end_date,
                func.count(Indication.id).label("soldiers_affected"),
            )
            .join(IndicationType, OrganizationIndication.indication_type == IndicationType.id)
            .outerjoin(Indication, Indication.organization_id == OrganizationIndication.id)
            .group_by(
                OrganizationIndication.id,
                OrganizationIndication.uuid,
                IndicationType.indication_description,
                OrganizationIndication.start_date,
                OrganizationIndication.end_date,
            )
        )
        result = await self.db.execute(stmt)
        return [
            OrganizationIndicationMinimalRow(
                id=row.id,
                uuid=row.uuid,
                indication_description=row.indication_description,
                start_date=row.start_date,
                end_date=row.end_date,
                soldiers_affected=row.soldiers_affected,
            )
            for row in result.all()
        ]

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
