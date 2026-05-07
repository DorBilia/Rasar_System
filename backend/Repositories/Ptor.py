from sqlalchemy import select, update, delete
from typing import Optional, List
from db.models.exemptions import MedicalPtor as Ptor
from db.models.exemptions import MedicalPtorType as PtorType
from Repositories.AbstractRepo import AbstractRepo


class PtorRepository(AbstractRepo):

    async def create(self, **kwargs) -> Ptor:
        new_ptor = Ptor(
            **kwargs
        )
        self.db.add(new_ptor)
        await self.db.commit()
        await self.db.refresh(new_ptor)
        return new_ptor

    async def get_by_id(self, ptor_id: int) -> Optional[Ptor]:
        result = await self.db.execute(select(Ptor).where(Ptor.id == ptor_id))
        return result.scalar_one_or_none()

    async def get_all(self) -> List[Ptor]:
        result = await self.db.execute(select(Ptor))
        return result.scalars().all()

    async def get_all_for_soldier(self, soldier_id: int) -> List[Ptor]:
        result = await self.db.execute(select(Ptor).where(Ptor.soldier_id == soldier_id))
        return result.scalars().all()

    async def update(self, ptor_id: int, **updates) -> Optional[Ptor]:
        query = (
            update(Ptor)
            .where(Ptor.id == ptor_id)
            .values(**updates)
            .execution_options(synchronize_session=False)
        )
        await self.db.execute(query)
        await self.db.commit()
        return await self.get_by_id(ptor_id)

    async def delete(self, ptor_id: int) -> bool:
        query = delete(Ptor).where(Ptor.id == ptor_id)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0
    

class PtorTypeRepository(AbstractRepo):

    async def create(self, description: str) -> PtorType:
        new_type = PtorType(description=description)
        self.db.add(new_type)
        await self.db.commit()
        await self.db.refresh(new_type)
        return new_type

    async def get_by_id(self, type_id: int) -> Optional[PtorType]:
        result = await self.db.execute(
            select(PtorType).where(PtorType.id == type_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> List[PtorType]:
        result = await self.db.execute(select(PtorType))
        return result.scalars().all()

    async def update(self, type_id: int, description: str) -> Optional[PtorType]:
        query = (
            update(PtorType)
            .where(PtorType.id == type_id)
            .values(description=description)
            .execution_options(synchronize_session="evaluate")
        )
        await self.db.execute(query)
        await self.db.commit()
        return await self.get_by_id(type_id)

    async def delete(self, type_id: int) -> bool:
        query = delete(PtorType).where(PtorType.id == type_id)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0
