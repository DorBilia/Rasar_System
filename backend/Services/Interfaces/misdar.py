from abc import ABC, abstractmethod
from datetime import date
from typing import Sequence

from db.models.misdar import MisdarAttendance


class IMisdarAttendanceService(ABC):
    @abstractmethod
    async def get_by_date_range(self, start_date: date, end_date: date) -> Sequence[MisdarAttendance]:
        pass

    @abstractmethod
    async def get_by_misdar_type(self, misdar_type: str) -> Sequence[MisdarAttendance]:
        pass

    @abstractmethod
    def get_absence_report(self) -> Sequence[MisdarAttendance]:
        pass
