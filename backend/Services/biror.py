import uuid
from API.schemas.biror import *
from typing import List, Optional, Sequence
from Repositories.biror import BirorTypeRepository
from Repositories.Interfaces.biror import IBirorRepo
from Services.Interfaces.biror import IBirorService, IBirorTypeService


class BirorService(IBirorService):
    def __init__(self, repository: IBirorRepo) -> None:
        self._repository = repository

    async def get_by_uuid(self, biror_uuid: str) -> Optional[BirorSchema]:
        row = await self._repository.get_by_uuid(biror_uuid)
        if row is None:
            return None
        return BirorSchema.model_validate(row)

    async def create(self, request: CreateBirorRequest) -> BirorSchema:
        data = request.model_dump()
        data["uuid"] = str(uuid.uuid4())
        created = await self._repository.create(**data)
        return BirorSchema.model_validate(created)

    async def update(self, biror_uuid: str, request: UpdateBirorRequest) -> Optional[BirorSchema]:
        payload = request.model_dump(exclude_unset=True)
        if not payload:
            return await self.get_by_uuid(biror_uuid)
        row = await self._repository.update_by_uuid(biror_uuid, **payload)
        if row is None:
            return None
        return BirorSchema.model_validate(row)

    async def delete(self, biror_uuid: str) -> bool:
        return await self._repository.delete_by_uuid(biror_uuid)

    async def get_by_result(self, biror_result: int) -> Sequence[BirorSchema]:
        rows = await self._repository.get_by_result(biror_result)
        return [BirorSchema.model_validate(r) for r in rows]

    async def get_for_soldier(self, soldier_id: int) -> Sequence[BirorSchema]:
        rows = await self._repository.get_for_soldier(soldier_id)
        return [BirorSchema.model_validate(r) for r in rows]


class BirorTypeService(IBirorTypeService):
    def __init__(self, repository: BirorTypeRepository) -> None:
        self._repository = repository

    async def get_all(self) -> List[BirorTypeSchema]:
        rows = await self._repository.get_all()
        return [BirorTypeSchema.model_validate(r) for r in rows]

    async def get_by_id(self, biror_type_id: int) -> Optional[BirorTypeSchema]:
        row = await self._repository.get_by_id(biror_type_id)
        if row is None:
            return None
        return BirorTypeSchema.model_validate(row)

    async def create(self, request: CreateBirorTypeRequest) -> BirorTypeSchema:
        data = request.model_dump()
        data["uuid"] = str(uuid.uuid4())
        created = await self._repository.create(**data)
        return BirorTypeSchema.model_validate(created)

    async def update(self, biror_type_id: int, request: UpdateBirorTypeRequest) -> Optional[BirorTypeSchema]:
        payload = request.model_dump(exclude_unset=True)
        if not payload:
            return await self.get_by_id(biror_type_id)
        row = await self._repository.update(biror_type_id, **payload)
        if row is None:
            return None
        return BirorTypeSchema.model_validate(row)

    async def delete(self, biror_type_id: int) -> bool:
        return await self._repository.delete(biror_type_id)
