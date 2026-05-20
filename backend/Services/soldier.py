import uuid
from typing import Optional, Sequence

from API.schemas.soldier import MinimalSoldier, FilterSoldiersRequest, FullSoldier, UpdateSoldierRequest, \
    CreateSoldierRequest
from Repositories.Interfaces.soldier import ISoldierRepo
from Services.Interfaces.soldier import ISoldierService


class SoldierService(ISoldierService):
    soldier_repo: ISoldierRepo

    def __init__(self, soldier_repo: ISoldierRepo) -> None:
        self.soldier_repo = soldier_repo

    async def create(self, soldier: CreateSoldierRequest) -> FullSoldier:
        data = soldier.model_dump()
        data.setdefault("is_active", True)
        data["uuid"] = str(uuid.uuid4())
        created = await self.soldier_repo.create(**data)
        return FullSoldier.model_validate(created)

    async def get_by_uuid(self, soldier_uuid: str) -> Optional[FullSoldier]:
        row = await self.soldier_repo.get_by_uuid(soldier_uuid)
        if row is None:
            return None
        return FullSoldier.model_validate(row)

    async def get_all_filtered(self, filter_request: FilterSoldiersRequest) -> Sequence[MinimalSoldier]: #TODO: fix model validate
        rows = await self.soldier_repo.get_all_filtered(
            unit=filter_request.unit,
            branch=filter_request.branch,
            section=filter_request.section,
            rank=filter_request.rank,
            discharge_date=filter_request.discharge_date,
            service_type=filter_request.service_type,
            phone_number=filter_request.phone_number,
            indication_type=filter_request.indication_type,
            search_term=filter_request.search_term,
            limit=filter_request.limit)
        return [MinimalSoldier.model_validate(r) for r in rows]

    async def update_soldier(self, soldier_uuid: str, updates: UpdateSoldierRequest) -> Optional[MinimalSoldier]:
        payload = updates.model_dump(exclude_unset=True)
        if not payload:
            row = await self.soldier_repo.get_by_uuid(soldier_uuid)
            if row is None:
                return None
            return MinimalSoldier.model_validate(row)
        row = await self.soldier_repo.update_by_uuid(soldier_uuid, **payload)
        if row is None:
            return None
        return MinimalSoldier.model_validate(row)

    async def delete_soldier(self, soldier_uuid: str) -> bool:
        return await self.soldier_repo.delete_by_uuid(soldier_uuid)
