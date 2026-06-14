import io
import uuid
import pandas as pd
from API.schemas.soldier import *
from Repositories.Interfaces.doh1 import IDoh1Repo
from Repositories.Interfaces.soldier import ISoldierRepo
from Services.Interfaces.soldier import ISoldierService
from core.utils import ExcelCols, excel_to_doh1


async def _get_status_updates(db_soldiers, incoming_soldiers: List[int]) -> List[dict]:
    status_updates = []
    for soldier in db_soldiers:
        if soldier.is_active:
            if soldier.id not in incoming_soldiers:
                status_updates.append({"id": soldier.id, "is_active": False})
        else:
            if soldier.id in incoming_soldiers:
                status_updates.append({"id": soldier.id, "is_active": True})
    return status_updates


class SoldierService(ISoldierService):
    soldier_repo: ISoldierRepo

    def __init__(self, soldier_repo: ISoldierRepo, doh1_repo: IDoh1Repo) -> None:
        self.soldier_repo = soldier_repo
        self.doh1_repo = doh1_repo

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

    async def get_all_filtered(self, filter_request: FilterSoldiersRequest) -> FilterSoldiersResponse:
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
            next_cursor_id=filter_request.next_cursor_id,
            limit=filter_request.limit)

        next_id = rows[-1].id if rows else None
        soldiers = [MinimalSoldier.model_validate(r) for r in rows]
        return FilterSoldiersResponse(soldiers=soldiers, next_cursor_id=next_id)

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

    async def add_doh1_manual(self, request: Doh1Request) -> bool:

        result = await self.doh1_repo.create(
            uuid=str(uuid.uuid4()),
            soldier_id=request.soldier_id,
            doh1_date=request.doh1_date,
            doh1_value=request.doh1_value)

        return result is not None

    async def handle_doh1_excel(self, file_bytes: bytes) -> bool:
        buffer = io.BytesIO(file_bytes)

        try:
            df = pd.read_excel(buffer, engine='openpyxl')

            df_clean = df.replace({pd.NA: None, float('nan'): None})
            records = df_clean.to_dict(orient="records")

            if not records:
                raise Exception

            incoming_soldier = [item[ExcelCols.ID] for item in records]
            existing_soldiers = await self.soldier_repo.get_all()
            doh1_records = await excel_to_doh1(records)
            updates = await _get_status_updates(existing_soldiers, incoming_soldier)

            soldier_update = await self.soldier_repo.change_soldiers_status(updates)
            doh1_creation = await self.doh1_repo.create_many(doh1_records)

            return soldier_update and doh1_creation is not None
        finally:
            buffer.close()
