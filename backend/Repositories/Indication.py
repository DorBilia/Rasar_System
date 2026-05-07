from sqlalchemy import select, update, delete
from typing import Optional, List
from db.models.indications import Indication, IndicationType
from Repositories.AbstractRepo import AbstractRepo


class IndicationRepository(AbstractRepo):

    async def create(self, **kwargs) -> Indication:
        new_indication = Indication(
            **kwargs
        )
        self.db.add(new_indication)
        await self.db.commit()
        await self.db.refresh(new_indication)
        return new_indication

    async def get_by_id(self, indication_id: int) -> Optional[Indication]:
        result = await self.db.execute(select(Indication).where(Indication.id == indication_id))
        return result.scalar_one_or_none()

    async def get_all_for_soldier(self, soldier_id: int) -> List[Indication]:
        result = await self.db.execute(select(Indication).where(Indication.soldier_id == soldier_id))
        return result.scalars().all()

    async def update(self, indication_id: int, **updates) -> Optional[Indication]:
        query = (
            update(Indication)
            .where(Indication.id == indication_id)
            .values(**updates)
            .execution_options(synchronize_session="fetch")
        )
        await self.db.execute(query)
        await self.db.commit()
        return await self.get_by_id(indication_id)

    async def delete(self, indication_id: int) -> bool:
        query = delete(Indication).where(Indication.id == indication_id)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0


class IndicationTypeRepository(AbstractRepo):

    async def create(self, description: str) -> IndicationType:
        new_type = IndicationType(description=description)
        self.db.add(new_type)
        await self.db.commit()
        await self.db.refresh(new_type)
        return new_type

    async def get_by_id(self, type_id: int) -> Optional[IndicationType]:
        result = await self.db.execute(
            select(IndicationType).where(IndicationType.id == type_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> List[IndicationType]:
        result = await self.db.execute(select(IndicationType))
        return result.scalars().all()

    async def update(self, type_id: int, description: str) -> Optional[IndicationType]:
        query = (
            update(IndicationType)
            .where(IndicationType.id == type_id)
            .values(description=description)
            .execution_options(synchronize_session="evaluate")
        )
        await self.db.execute(query)
        await self.db.commit()
        return await self.get_by_id(type_id)

    async def delete(self, type_id: int) -> bool:
        query = delete(IndicationType).where(IndicationType.id == type_id)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0
