from datetime import date
from typing import Sequence

from db.models.misdar import MisdarAttendance
from Repositories.Interfaces.misdar import IMisdarAttendanceRepo
from Services.Interfaces.misdar import IMisdarAttendanceService


class MisdarAttendanceService(IMisdarAttendanceService):
    def __init__(self, repository: IMisdarAttendanceRepo) -> None:
        self._repository = repository

    async def get_by_date_range(self, start_date: date, end_date: date) -> Sequence[MisdarAttendance]:
        return await self._repository.get_by_date_range(start_date, end_date)

    async def get_by_misdar_type(self, misdar_type: str) -> Sequence[MisdarAttendance]:
        return await self._repository.get_by_misdar_type(misdar_type)

    def get_absence_report(self) -> Sequence[MisdarAttendance]:
        return self._repository.get_absence_report()
