from typing import Generic, TypeVar, List, Optional, Type, Any, Sequence
from sqlalchemy import select, update, delete, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from core.Interfaces.base_repo import BaseRepo

T = TypeVar("T")


class AbstractRepo(BaseRepo[T], Generic[T]):
    def __init__(self, db: AsyncSession, model: Type[T]):
        super().__init__(db)
        self.db = db
        self.model = model

    async def create(self, **kwargs) -> T:
        new_entity = self.model(**kwargs)
        self.db.add(new_entity)
        await self.db.commit()
        await self.db.refresh(new_entity)
        return new_entity

    async def get_by_id(self, entity_id: int) -> Optional[T]:
        # Using getattr(self.model, 'id') makes it generic for models with 'id' column
        query = select(self.model).where(self.model.id == entity_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[T]:
        query = select(self.model)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update(self, entity_id: int, **updates) -> Optional[T]:
        # Gets key-value attribute in a dict form and updates the relevant fields in the object
        query = (
            update(self.model)
            .where(self.model.id == entity_id)
            .values(**updates)
            .execution_options(synchronize_session=False)
        )
        await self.db.execute(query)
        await self.db.commit()
        return await self.get_by_id(entity_id)

    async def delete(self, entity_id: int) -> bool:
        # Returns how many rows were affected, if 0 then object is not found
        query = delete(self.model).where(self.model.id == entity_id)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0  # check whether if this is valid
