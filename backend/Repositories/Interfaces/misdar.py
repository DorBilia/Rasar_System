from datetime import date, time
from typing import Optional, Sequence
from abc import abstractmethod

from Repositories.Interfaces.baseRepo import IBaseRepo
from db.models.misdar import MisdarAttendance, MisdarType, MisdarTypeDays
from core.enums import DayOfWeek


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


class IMisdarTypeRepo(IBaseRepo[MisdarType]):
    @abstractmethod
    async def get_all_with_days(self) -> Sequence[MisdarType]:
        pass

    @abstractmethod
    async def get_by_id_with_days(self, entity_id: int) -> Optional[MisdarType]:
        pass

    @abstractmethod
    async def create_with_days(
        self,
        *,
        misdar_name: str,
        misdar_time: time,
        misdar_length: float,
        misdar_days: list[DayOfWeek],
    ) -> MisdarType:
        pass

    @abstractmethod
    async def update_with_days(
        self,
        entity_id: int,
        misdar_name: Optional[str] = None,
        misdar_time: Optional[time] = None,
        misdar_length: Optional[float] = None,
        misdar_days: Optional[list[DayOfWeek]] = None) -> Optional[MisdarType]:
        pass
