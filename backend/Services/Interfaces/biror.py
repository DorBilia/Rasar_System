from abc import ABC, abstractmethod
from API.schemas.biror import *
from typing import List, Optional, Sequence


class BirorResultNotFoundError(Exception):
    pass


class BirorNotFoundError(Exception):
    pass


class IBirorService(ABC):
    @abstractmethod
    async def get_by_uuid(self, biror_uuid: str) -> Optional[BirorSchema]:
        pass

    @abstractmethod
    async def create(self, request: CreateBirorRequest) -> BirorSchema:
        pass

    @abstractmethod
    async def update(self, biror_uuid: str, request: UpdateBirorRequest) -> Optional[BirorSchema]:
        pass

    @abstractmethod
    async def delete(self, biror_uuid: str) -> bool:
        pass

    @abstractmethod
    async def get_by_biror_type(self, biror_type: int) -> Sequence[BirorSchema]:
        pass

    @abstractmethod
    async def get_for_soldier(self, soldier_id: int) -> Sequence[BirorSchema]:
        pass


class IBirorTypeService(ABC):
    @abstractmethod
    async def get_all(self) -> List[BirorTypeSchema]:
        pass

    @abstractmethod
    async def get_by_id(self, biror_type_id: int) -> Optional[BirorTypeSchema]:
        pass

    @abstractmethod
    async def create(self, request: CreateBirorTypeRequest) -> BirorTypeSchema:
        pass

    @abstractmethod
    async def update(self, biror_type_id: int, request: UpdateBirorTypeRequest) -> Optional[BirorTypeSchema]:
        pass

    @abstractmethod
    async def delete(self, biror_type_id: int) -> bool:
        pass


class IBirorResultService(ABC):
    @abstractmethod
    async def get_all(self) -> List[BirorResultSchema]:
        pass

    @abstractmethod
    async def get_by_uuid(self, biror_result_uuid: str) -> Optional[BirorResultSchema]:
        pass

    @abstractmethod
    async def create(self, request: CreateBirorResultRequest) -> BirorResultSchema:
        pass

    @abstractmethod
    async def update(self, biror_result_uuid: str, request: UpdateBirorResultRequest) -> Optional[BirorResultSchema]:
        pass

    @abstractmethod
    async def delete(self, biror_result_uuid: str) -> bool:
        pass
