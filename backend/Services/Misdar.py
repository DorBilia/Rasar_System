import uuid
from datetime import date, datetime, time, timedelta
from typing import Sequence

from API.schemas.misdar import (
    LateScanRequest,
    MisdarOverviewResponse,
    MisdarRequest,
    MisdarType as MisdarTypeSchema,
    ScanRequest,
    ScanResponse,
    SearchMisdarRequest)
from core.enums import Doh1ValueEnum, ScanNote
from db.models.misdar import MisdarType as MisdarTypeModel
from db.models.soldier import Soldier
from Repositories.Interfaces.baseRepo import IBaseRepo
from Repositories.Interfaces.indication import ISoldierIndicationRepo
from Repositories.Interfaces.misdar import IMisdarAttendanceRepo
from Repositories.Interfaces.soldier import ISoldierRepo
from Services.Interfaces.misdar import IMisdarService


class DuplicateMisdarScanError(Exception):
    pass


class MisdarTypeNotFoundError(Exception):
    pass


class MisdarService(IMisdarService):
    def __init__(
            self,
            repository: IMisdarAttendanceRepo,
            type_repository: IBaseRepo[MisdarTypeModel],
            indication_repository: ISoldierIndicationRepo,
            soldier_repository: ISoldierRepo,
    ):
        self._repository = repository
        self._type_repository = type_repository
        self._indication_repository = indication_repository
        self._soldier_repository = soldier_repository

    async def search(self, request: SearchMisdarRequest) -> Sequence[MisdarOverviewResponse]:

        result = await self._repository.get_filtered(
            misdar_date=request.misdar_date,
            misdar_type=request.misdar_type,
        )

        return [MisdarOverviewResponse.model_validate(r) for r in result]

    async def get_absence_report(self, request: MisdarRequest):
        pass

    async def get_summary_report(self, request: MisdarRequest):
        pass

    async def try_scan_start(self, misdar_type: int) -> bool:
        misdar_type = await self._type_repository.get_by_id(misdar_type)
        if misdar_type is None:
            return False

        now = datetime.now()
        start = datetime.combine(date.today(), misdar_type.misdar_time)
        end = start + timedelta(hours=misdar_type.misdar_length)
        return start <= now < end

    async def scan_active(self, request: ScanRequest) -> ScanResponse:
        return await self._record_scan(
            soldier_id=request.soldier_id,
            misdar_type=request.misdar_type,
            misdar_date=date.today(),
            scan_time=datetime.now().time(),
        )

    async def scan_late(self, request: LateScanRequest) -> ScanResponse:
        return await self._record_scan(
            soldier_id=request.soldier_id,
            misdar_type=request.misdar_type,
            misdar_date=request.misdar_date,
            scan_time=request.scan_time,
        )

    async def get_types(self) -> Sequence[MisdarTypeSchema]:
        rows = await self._type_repository.get_all()
        return [MisdarTypeSchema.model_validate(r) for r in rows]

    async def _record_scan(
            self,
            soldier_id: int,
            misdar_type: int,
            misdar_date: date,
            scan_time: time) -> ScanResponse:

        misdar_type_row = await self._type_repository.get_by_id(misdar_type)

        if misdar_type_row is None:
            raise MisdarTypeNotFoundError(misdar_type)

        soldier = await self._soldier_repository.get_by_id(soldier_id)
        if soldier is None:
            return ScanResponse(soldier_id=soldier_id, scan_note=ScanNote.SOLDIER_NOT_FOUND, uuid=None)

        if await self._repository.exists_for_soldier(soldier_id, misdar_date, misdar_type):
            raise DuplicateMisdarScanError()

        scan_note = await self._resolve_scan_note(soldier, misdar_type, misdar_date)

        created = await self._repository.create(
            uuid=str(uuid.uuid4()),
            soldier_id=soldier_id,
            misdar_type=misdar_type,
            misdar_date=misdar_date,
            scan_time=scan_time,
            scan_note=scan_note,
        )

        return ScanResponse(soldier_id=soldier_id, scan_note=scan_note, uuid=created.uuid)

    async def _resolve_scan_note(self, soldier: Soldier, misdar_type: int, misdar_date: date) -> ScanNote:
        if not soldier.is_active:
            return ScanNote.SOLDIER_INACTIVE

        doh1 = await self._soldier_repository.get_doh1_on_date(soldier.id, misdar_date)
        if doh1 is None or doh1.doh1_value != Doh1ValueEnum.PRESENT:
            return ScanNote.DOH1_NOT_PRESENT

        can_attend = await self._indication_repository.can_soldier_attend_misdar(
            soldier.id, misdar_type
        )
        if not can_attend:
            return ScanNote.CONFLICT

        return ScanNote.SUCCESS

    async def delete_scan(self, soldier_uuid: str) -> bool:
        return await self._repository.delete_by_uuid(soldier_uuid)
