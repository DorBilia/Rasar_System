from abc import ABC, abstractmethod
from typing import Optional, Sequence
from API.schemas.misdar import *


class IMisdarService(ABC):
    @abstractmethod
    async def search(self, request: SearchMisdarRequest) -> Sequence[MisdarOverviewResponse]:
        pass

    @abstractmethod
    async def get_absence_report(self, request: MisdarRequest):
        pass

    @abstractmethod
    async def get_summary_report(self, request: MisdarRequest):
        pass

    @abstractmethod
    async def try_scan_start(self, misdar_type: int) -> bool:
        pass

    @abstractmethod
    async def scan_active(self, request: ScanRequest) -> ScanResponse:
        pass

    @abstractmethod
    async def scan_late(self, request: LateScanRequest) -> ScanResponse:
        pass

    @abstractmethod
    async def get_types(self) -> Sequence[MisdarTypeSchema]:
        pass

    @abstractmethod
    async def create_type(self, request: CreateMisdarTypeRequest) -> MisdarTypeSchema:
        pass

    @abstractmethod
    async def get_type_by_id(self, misdar_type_id: int) -> Optional[MisdarTypeSchema]:
        pass

    @abstractmethod
    async def update_type(self, misdar_type_id: int, request: UpdateMisdarTypeRequest) -> Optional[MisdarTypeSchema]:
        pass

    @abstractmethod
    async def delete_type(self, misdar_type_id: int) -> bool:
        pass

    @abstractmethod
    async def delete_scan(self, scan_uuid: str) -> bool:
        pass

    @abstractmethod
    async def get_soldier_attendances_for_month(self, soldier_id: int, date: date) -> Sequence[AttendanceDay]:
        pass

    @abstractmethod
    async def get_misdar_days(self) -> Sequence[MisdarDay]:
        """Get all misdar types and their days"""
        pass
