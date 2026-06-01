import uuid
from typing import Any, List, Optional, Sequence

from API.schemas.biror import *
from db.models.biror import Biror
from Repositories.biror import BirorResultRepository, BirorTypeRepository
from Repositories.Interfaces.biror import IBirorRepo
from Services.Interfaces.biror import (
    BirorNotFoundError,
    BirorResultNotFoundError,
    IBirorResultService,
    IBirorService,
    IBirorTypeService,
)


def _result_uuid_from_row(row: Biror) -> Optional[str]:
    if row.biror_result is None:
        return None
    if row.biror_result_ref is not None:
        return row.biror_result_ref.uuid
    return None


def _to_biror_schema(row: Biror) -> BirorSchema:
    return BirorSchema(
        uuid=row.uuid,
        soldier_id=row.soldier_id,
        biror_type=row.biror_type,
        biror_date=row.biror_date,
        biror_description=row.biror_description,
        comments=row.comments,
        biror_result=_result_uuid_from_row(row),
    )


class BirorService(IBirorService):
    def __init__(self, repository: IBirorRepo, result_repository: BirorResultRepository) -> None:
        self._repository = repository
        self._result_repository = result_repository

    async def _resolve_result_uuid(self, result_uuid: Optional[str]) -> Optional[int]:
        if result_uuid is None:
            return None
        row = await self._result_repository.get_by_uuid(result_uuid)
        if row is None:
            raise BirorResultNotFoundError()
        return row.id

    async def _prepare_biror_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload)
        if "biror_result" not in payload:
            return payload
        result_uuid = payload.pop("biror_result")
        payload["biror_result"] = await self._resolve_result_uuid(result_uuid)
        return payload

    async def get_by_uuid(self, biror_uuid: str) -> Optional[BirorSchema]:
        row = await self._repository.get_by_uuid(biror_uuid)
        if row is None:
            return None
        return _to_biror_schema(row)

    async def create(self, request: CreateBirorRequest) -> BirorSchema:
        data = await self._prepare_biror_payload(request.model_dump())
        data["uuid"] = str(uuid.uuid4())
        created = await self._repository.create(**data)
        loaded = await self._repository.get_by_uuid(created.uuid)
        return _to_biror_schema(loaded or created)

    async def update(self, biror_uuid: str, request: UpdateBirorRequest) -> Optional[BirorSchema]:
        payload = request.model_dump(exclude_unset=True)
        if not payload:
            return await self.get_by_uuid(biror_uuid)
        payload = await self._prepare_biror_payload(payload)
        row = await self._repository.update_by_uuid(biror_uuid, **payload)
        if row is None:
            return None
        loaded = await self._repository.get_by_uuid(biror_uuid)
        return _to_biror_schema(loaded or row)

    async def delete(self, biror_uuid: str) -> bool:
        return await self._repository.delete_by_uuid(biror_uuid)

    async def get_by_biror_type(self, biror_type: int) -> Sequence[BirorSchema]:
        rows = await self._repository.get_by_type(biror_type)
        return [_to_biror_schema(r) for r in rows]

    async def get_for_soldier(self, soldier_id: int) -> Sequence[BirorSchema]:
        rows = await self._repository.get_for_soldier(soldier_id)
        return [_to_biror_schema(r) for r in rows]


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


class BirorResultService(IBirorResultService):
    def __init__(
            self,
            repository: BirorResultRepository,
            biror_repository: IBirorRepo) -> None:
        self._repository = repository
        self._biror_repository = biror_repository

    async def get_all(self) -> List[BirorResultSchema]:
        rows = await self._repository.get_all()
        return [BirorResultSchema.model_validate(r) for r in rows]

    async def get_by_uuid(self, biror_result_uuid: str) -> Optional[BirorResultSchema]:
        row = await self._repository.get_by_uuid(biror_result_uuid)
        if row is None:
            return None
        return BirorResultSchema.model_validate(row)

    async def create(self, request: CreateBirorResultRequest) -> BirorResultSchema:
        biror = await self._biror_repository.get_by_uuid(request.biror_uuid)
        if biror is None:
            raise BirorNotFoundError()

        created = await self._repository.create(
            uuid=str(uuid.uuid4()),
            biror_result_description=request.biror_result_description,
        )
        updated = await self._biror_repository.update_by_uuid(
            request.biror_uuid,
            biror_result=created.id,
        )
        if updated is None:
            raise BirorNotFoundError()
        return BirorResultSchema.model_validate(created)

    async def update(self, biror_result_uuid: str, request: UpdateBirorResultRequest) -> Optional[BirorResultSchema]:
        payload = request.model_dump(exclude_unset=True)
        if not payload:
            return await self.get_by_uuid(biror_result_uuid)
        row = await self._repository.update_by_uuid(biror_result_uuid, **payload)
        if row is None:
            return None
        return BirorResultSchema.model_validate(row)

    async def delete(self, biror_result_uuid: str) -> bool:
        return await self._repository.delete_by_uuid(biror_result_uuid)
