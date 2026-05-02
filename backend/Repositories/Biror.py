from sqlalchemy import select, update, delete
from typing import Optional, List
from db.models.Biror import Biror, BirorType
from Repositories import AbstractRepo


class BirorRepository(AbstractRepo):

    async def create(self, **kwargs) -> Biror:
        new_biror = Biror(
            **kwargs
        )
        self.db.add(new_biror)
        await self.db.commit()
        await self.db.refresh(new_biror)
        return new_biror

    async def get_by_id(self, biror_id: int) -> Optional[Biror]:
        result = await self.db.execute(select(Biror).where(Biror.id == biror_id))
        return result.scalar_one_or_none()

    async def get_all(self) -> List[Biror]:
        result = await self.db.execute(select(Biror))
        return result.scalars().all()

    async def get_all_for_soldier(self, soldier_id: int) -> List[Biror]:
        result = await self.db.execute(select(Biror).where(Biror.soldier_id == soldier_id))
        return result.scalars().all()

    async def update(self, biror_id: int, **updates) -> Optional[Biror]:
        query = (
            update(Biror)
            .where(Biror.id == biror_id)
            .values(**updates)
            .execution_options(synchronize_session=False)
        )
        await self.db.execute(query)
        await self.db.commit()
        return await self.get_by_id(biror_id)

    async def delete(self, biror_id: int) -> bool:
        query = delete(Biror).where(Biror.id == biror_id)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0


class BirorTypeRepository(AbstractRepo):

    async def create(self, description: str) -> BirorType:
        new_type = BirorType(description=description)
        self.db.add(new_type)
        await self.db.commit()
        await self.db.refresh(new_type)
        return new_type

    async def get_by_id(self, type_id: int) -> Optional[BirorType]:
        result = await self.db.execute(
            select(BirorType).where(BirorType.id == type_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> List[BirorType]:
        result = await self.db.execute(select(BirorType))
        return result.scalars().all()

    async def update(self, type_id: int, description: str) -> Optional[BirorType]:
        query = (
            update(BirorType)
            .where(BirorType.id == type_id)
            .values(description=description)
            .execution_options(synchronize_session="evaluate")
        )
        await self.db.execute(query)
        await self.db.commit()
        return await self.get_by_id(type_id)

    async def delete(self, type_id: int) -> bool:
        query = delete(BirorType).where(BirorType.id == type_id)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0
