from datetime import date
from typing import Sequence

from API.schemas.misdar import LateScanRequest, ScanResponse, ScanRequest, MisdarRequest, SearchMisdarRequest, \
    MisdarOverviewResponse
from Repositories.Interfaces.misdar import IMisdarAttendanceRepo
from Services.Interfaces.misdar import IMisdarService
from Repositories.Interfaces.baseRepo import IBaseRepo
from db.models.misdar import MisdarType


class MisdarAttendanceService(IMisdarService):
    def __init__(self, repository: IMisdarAttendanceRepo, type_repository: IBaseRepo[MisdarType]):
        self._repository = repository
        self.type_repository = type_repository

    async def search(self, request: SearchMisdarRequest) -> Sequence[MisdarOverviewResponse]:
        pass

    async def get_absence_report(self, request: MisdarRequest):
        pass

    async def get_summary_report(self, request: MisdarRequest):
        pass

    async def try_scan_start(self, misdar_type: int) -> bool:
        pass

    async def scan_active(self, request: ScanRequest) -> ScanResponse:
        pass

    async def scan_late(self, request: LateScanRequest) -> ScanResponse:
        pass

    async def get_types(self) -> Sequence[MisdarType]:
        pass
