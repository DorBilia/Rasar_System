from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod


class AbstractRepo(ABC):
    db: AsyncSession

    def __init__(self, db: AsyncSession):
        self.db = db

    @abstractmethod
    async def create(self, **kwargs):
        pass

    @abstractmethod
    async def get_by_id(self, id: int):
        pass

    @abstractmethod
    async def get_all_for_soldier(self, soldier_id: int):
        pass

    @abstractmethod
    async def update(self, id: int, **updates):
        pass

    @abstractmethod
    async def delete(self, biror_id: int) -> bool:
        pass
