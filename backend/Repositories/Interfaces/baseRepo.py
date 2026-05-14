from typing import Optional, List, Generic, TypeVar, Sequence
from abc import ABC, abstractmethod

T = TypeVar("T")


class IBaseRepo(ABC, Generic[T]):


    @abstractmethod
    async def create(self, **kwargs) -> T:
        pass

    @abstractmethod
    async def create_many(self, objects: list[T]) -> list[T]:
        pass

    async def get_by_id(self, id: int) -> Optional[object]:
        pass

    @abstractmethod
    async def get_for_soldier(self, soldier_id: str) -> Sequence[object]:
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