from datetime import date
from typing import Optional, Sequence
from abc import abstractmethod

from Repositories.Interfaces.baseRepo import IBaseRepo
from db.models.misdar import MisdarAttendance, MisdarTypeDays


class IMisdarAttendanceRepo(IBaseRepo[MisdarAttendance]):

    @abstractmethod
    async def get_filtered(
            self,
            misdar_date: Optional[date] = None,
            misdar_type: Optional[int] = None, ) -> Sequence[MisdarAttendance]:
        pass

    @abstractmethod
    async def exists_for_soldier(self, soldier_id: int, misdar_date: date, misdar_type: int) -> bool:
        pass

    @abstractmethod
    async def get_absence_report(self) -> Sequence[MisdarAttendance]:
        pass

    @abstractmethod
    async def get_misdar_attendances_for_month(self, soldier_id: int, date: date) -> Sequence[MisdarAttendance]:
        pass

    @abstractmethod
    async def get_misdar_days(self) -> Sequence[MisdarTypeDays]:
        pass
