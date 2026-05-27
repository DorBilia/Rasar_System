from typing import Optional, Sequence

from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.enums import IndicationDescriptionEnum
from db.models.indications import Indication, IndicationType, IndicationTypeMisdarType, OrganizationIndication
from db.models.misdar import MisdarType
from Repositories.AbstractRepo import AbstractRepo
from Repositories.Interfaces.indication import IIndicationTypeRepo, ISoldierIndicationRepo, IOrganizationIndicationRepo


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


class IndicationTypeRepository(AbstractRepo[IndicationType], IIndicationTypeRepo):
    def __init__(self, db: AsyncSession):
        super().__init__(db, IndicationType)

    async def get_all_with_mappings(self) -> Sequence[IndicationType]:
        query = select(IndicationType).options(selectinload(IndicationType.indication_mappings))
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id_with_mappings(self, entity_id: int) -> Optional[IndicationType]:
        query = (
            select(IndicationType)
            .where(IndicationType.id == entity_id)
            .options(selectinload(IndicationType.indication_mappings))
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create_with_misdars(
            self,
            indication_description: IndicationDescriptionEnum,
            weekly_arrivals: int,
            misdar_type_ids: Optional[list[int]]) -> Optional[IndicationType]:

        new_entity = IndicationType(
            indication_description=indication_description,
            weekly_arrivals=weekly_arrivals,
        )
        self.db.add(new_entity)
        await self.db.flush()

        if misdar_type_ids is not None:
            mappings = [
                IndicationTypeMisdarType(indication_type_id=new_entity.id, misdar_type_id=misdar_type_id)
                for misdar_type_id in misdar_type_ids
            ]
            self.db.add_all(mappings)

        await self.db.commit()
        return await self.get_by_id_with_mappings(new_entity.id)

    async def update_with_misdars(
            self,
            entity_id: int,
            indication_description: IndicationDescriptionEnum = None,
            weekly_arrivals: Optional[int] = None,
            misdar_type_ids: Optional[list[int]] = None) -> Optional[IndicationType]:
        row = await self.get_by_id_with_mappings(entity_id)
        if row is None:
            return None

        if indication_description is not None:
            row.indication_description = indication_description
        if weekly_arrivals is not None:
            row.weekly_arrivals = weekly_arrivals

        if misdar_type_ids is not None:
            await self.db.execute(
                delete(IndicationTypeMisdarType).where(IndicationTypeMisdarType.indication_type_id == entity_id)
            )
            self.db.add_all(
                [
                    IndicationTypeMisdarType(indication_type_id=entity_id, misdar_type_id=misdar_type_id)
                    for misdar_type_id in misdar_type_ids
                ]
            )

        await self.db.commit()
        return await self.get_by_id_with_mappings(entity_id)


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
