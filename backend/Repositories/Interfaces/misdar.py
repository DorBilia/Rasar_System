from base_repo import IBaseRepo
from db.models.misdar import MisdarAttendance
from typing import Sequence
from abc import abstractmethod
from datetime import date


class IMisdarAttendanceRepo(IBaseRepo[MisdarAttendance]):

    @abstractmethod
    def get_by_date_range(self, start_date: date, end_date: date) -> Sequence[MisdarAttendance]:
        pass

    @abstractmethod
    def get_by_misdar_type(self, misdar_type: str) -> Sequence[MisdarAttendance]:
        pass

    @abstractmethod
    def get_absence_report(self) -> Sequence[MisdarAttendance]:
        pass

