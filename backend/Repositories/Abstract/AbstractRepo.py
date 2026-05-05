from typing import Optional, List

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
    async def get_by_id(self, id: int) -> Optional[object]:
        pass

    @abstractmethod
    async def get_all(self) -> List[object]:
        pass

    @abstractmethod
    async def update(self, id: int, **updates) -> Optional[object]:
        pass

    @abstractmethod
    async def delete(self, biror_id: int) -> bool:
        pass
