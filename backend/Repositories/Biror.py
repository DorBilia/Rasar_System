from sqlalchemy import select, update, delete
from typing import Optional, Sequence
from db.models.Biror import Biror
from Repositories.Abstract import AbstractRepo


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

    async def get_all_for_soldier(self, soldier_id: int) -> Sequence[Biror]:
        result = await self.db.execute(select(Biror).where(Biror.soldier_id == soldier_id))
        return result.scalars().all()

    async def update(self, biror_id: int, **updates) -> Optional[Biror]:
        query = (
            update(Biror)
            .where(Biror.id == biror_id)
            .values(**updates)
            .execution_options(synchronize_session="fetch")
        )
        await self.db.execute(query)
        await self.db.commit()
        return await self.get_by_id(self.db, biror_id)

    async def delete(self, biror_id: int) -> bool:
        query = delete(Biror).where(Biror.id == biror_id)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0
