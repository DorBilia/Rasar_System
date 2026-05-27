import uuid
from collections import defaultdict
from calendar import monthrange
from datetime import datetime, timedelta
from typing import Sequence

from API.schemas.misdar import *

from core.enums import DayOfWeek, Doh1ValueEnum, ScanNote
from db.models.soldier import Soldier
from Repositories.Interfaces.doh1 import IDoh1Repo
from Repositories.Interfaces.indication import ISoldierIndicationRepo
from Repositories.Interfaces.misdar import IMisdarAttendanceRepo
from Repositories.Interfaces.soldier import ISoldierRepo
from Services.Interfaces.misdar import IMisdarService
from Repositories.misdar import MisdarTypeRepository


class DuplicateMisdarScanError(Exception):
    pass


class MisdarTypeNotFoundError(Exception):
    pass


class MisdarService(IMisdarService):
    def __init__(
            self,
            repository: IMisdarAttendanceRepo,
            type_repository: MisdarTypeRepository,
            indication_repository: ISoldierIndicationRepo,
            soldier_repository: ISoldierRepo,
            doh1_repository: IDoh1Repo,
    ):
        self._repository = repository
        self._type_repository = type_repository
        self._indication_repository = indication_repository
        self._soldier_repository = soldier_repository
        self._doh1_repository = doh1_repository

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
        rows = await self._type_repository.get_all_with_days()
        result: list[MisdarTypeSchema] = []
        for row in rows:
            result.append(
                MisdarTypeSchema(
                    id=row.id,
                    misdar_name=row.misdar_name,
                    misdar_time=row.misdar_time,
                    misdar_length=row.misdar_length,
                    misdar_days=[d.misdar_day for d in row.misdar_days],
                )
            )
        return result

    async def create_type(self, request: CreateMisdarTypeRequest) -> MisdarTypeSchema:
        created = await self._type_repository.create_with_days(
            misdar_name=request.misdar_name,
            misdar_time=request.misdar_time,
            misdar_length=request.misdar_length,
            misdar_days=request.misdar_days,
        )
        assert created is not None
        return MisdarTypeSchema(
            id=created.id,
            misdar_name=created.misdar_name,
            misdar_time=created.misdar_time,
            misdar_length=created.misdar_length,
            misdar_days=[d.misdar_day for d in created.misdar_days],
        )

    async def get_type_by_id(self, misdar_type_id: int) -> Optional[MisdarTypeSchema]:
        row = await self._type_repository.get_by_id_with_days(misdar_type_id)
        if row is None:
            return None
        return MisdarTypeSchema(
            id=row.id,
            misdar_name=row.misdar_name,
            misdar_time=row.misdar_time,
            misdar_length=row.misdar_length,
            misdar_days=[d.misdar_day for d in row.misdar_days])

    async def update_type(
            self,
            misdar_type_id: int,
            request: UpdateMisdarTypeRequest) -> Optional[MisdarTypeSchema]:
        updated = await self._type_repository.update_with_days(
            misdar_type_id,
            misdar_name=request.misdar_name,
            misdar_time=request.misdar_time,
            misdar_length=request.misdar_length,
            misdar_days=request.misdar_days)
        if updated is None:
            return None
        return MisdarTypeSchema(
            id=updated.id,
            misdar_name=updated.misdar_name,
            misdar_time=updated.misdar_time,
            misdar_length=updated.misdar_length,
            misdar_days=[d.misdar_day for d in updated.misdar_days])

    async def delete_type(self, misdar_type_id: int) -> bool:
        return await self._type_repository.delete(misdar_type_id)

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

        scan_note = await self._resolve_scan_note(soldier, misdar_type)

        created = await self._repository.create(
            uuid=str(uuid.uuid4()),
            soldier_id=soldier_id,
            misdar_type=misdar_type,
            misdar_date=misdar_date,
            scan_time=scan_time,
            scan_note=scan_note,
        )

        return ScanResponse(soldier_id=soldier_id, scan_note=scan_note, uuid=created.uuid)

    async def _resolve_scan_note(self, soldier: Soldier, misdar_type: int) -> ScanNote:
        if not soldier.is_active:
            return ScanNote.SOLDIER_INACTIVE

        can_attend = await self._indication_repository.can_soldier_attend_misdar(
            soldier.id, misdar_type
        )
        if not can_attend:
            return ScanNote.CONFLICT

        return ScanNote.SUCCESS

    async def delete_scan(self, soldier_uuid: str) -> bool:
        return await self._repository.delete_by_uuid(soldier_uuid)

    async def get_soldier_attendances_for_month(self, soldier_id: int, selected_date: date) -> Sequence[AttendanceDay]:
        month_start = selected_date.replace(day=1)
        days_in_month = monthrange(selected_date.year, selected_date.month)[1]

        doh1_records = await self._doh1_repository.get_doh1_on_month(soldier_id, selected_date)
        attendance_records = await self._repository.get_misdar_attendances_for_month(soldier_id, selected_date)
        misdar_days = await self._repository.get_misdar_days()

        doh1_by_date = {record.doh1_date: record for record in doh1_records}

        # Build a map for date : misdar types attended to in this date
        attended_by_date: dict[date, set[int]] = defaultdict(set)
        for attendance in attendance_records:
            attended_by_date[attendance.misdar_date].add(attendance.misdar_type)

        # Build a map for day : misdar types on this day
        misdar_types_by_weekday: dict[DayOfWeek, set[int]] = defaultdict(set)
        for misdar_day in misdar_days:
            misdar_types_by_weekday[misdar_day.misdar_day].add(misdar_day.misdar_type)

        # Build map for attendance flags - misdar type : can/can't atten this misdar
        can_attend_by_type: dict[int, bool] = {}
        result: list[AttendanceDay] = []
        for misdars_in_day in misdar_types_by_weekday.values():
            for misdar_type in misdars_in_day:
                if misdar_type not in can_attend_by_type:
                    can_attend_by_type[misdar_type] = (
                        await self._indication_repository.can_soldier_attend_misdar(
                            soldier_id, misdar_type))

        for day_offset in range(days_in_month):
            current_date = month_start + timedelta(days=day_offset)
            doh1 = doh1_by_date.get(current_date)

            # Check whether the soldier is present
            if doh1 is None or doh1.doh1_value != Doh1ValueEnum.PRESENT:
                result.append(
                    AttendanceDay(
                        date=current_date,
                        base_status="not present",
                        misdar_statuses=None))
                continue

            misdar_statuses: list[MisdarAttendanceStatus] = []
            weekday = DayOfWeek(current_date.isoweekday())

            # Check for every misdar on the specific day if the soldier can attend it and if so, check if he attended
            for misdar_type in misdar_types_by_weekday.get(weekday, []):

                if not can_attend_by_type[misdar_type]:
                    continue

                status = (
                    "attended"
                    if misdar_type in attended_by_date.get(current_date, set())
                    else "didnt attend")
                misdar_statuses.append(
                    MisdarAttendanceStatus(misdar_type=misdar_type, status=status))

            base_status = (
                "didnt attend misdar"
                if any(status.status == "didnt attend" for status in misdar_statuses)
                else "attended")

            result.append(
                AttendanceDay(
                    date=current_date,
                    base_status=base_status,
                    misdar_statuses=misdar_statuses))

        return result

    async def get_misdar_days(self) -> Sequence[MisdarDay]:
        return [
            MisdarDay(day=misdar_day.misdar_day, misdar_type=misdar_day.misdar_type)
            for misdar_day in await self._repository.get_misdar_days()
        ]
