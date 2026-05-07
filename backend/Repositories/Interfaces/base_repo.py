from typing import Optional, List, Generic, TypeVar, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod

T = TypeVar("T")


class IBaseRepo(ABC, Generic[T]):
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
    async def get_for_soldier(self, soldier_id: str) -> Sequence[object]:
        # Easier to implement it that way, breaks SOLID principle
        pass

    @abstractmethod
    async def get_all(self) -> List[object]:
        pass

    @abstractmethod
    async def update(self, id: int, **updates) -> Optional[object]:
        # Gets key-value attribute in a dict form and updates the relevant fields in the object
        pass

    @abstractmethod
    async def delete(self, biror_id: int) -> bool:
        pass
