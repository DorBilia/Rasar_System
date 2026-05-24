from abc import ABC, abstractmethod
from typing import Sequence
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
    async def get_types(self) -> Sequence[MisdarType]:
        pass
