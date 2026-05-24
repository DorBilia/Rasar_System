from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_restful.cbv import cbv
from starlette import status

from Services.Interfaces.misdar import *
from core.dependecies.misdar import get_misdar_attendance_service
from API.schemas.misdar import *

router = APIRouter(prefix="/misdars", tags=["Misdars"])


@cbv(router)
class Misdars:
    service: IMisdarAttendanceService = Depends(get_misdar_attendance_service)

    @router.post("/search", response_model=List[MisdarOverviewResponse])
    async def get_misdars(self, request: SearchMisdarRequest):
        pass

    @router.post("/start_scan/{misdar_type}", status_code=status.HTTP_202_ACCEPTED | status.HTTP_409_CONFLICT)
    async def start_scan(self, misdar_type: int):
        pass

    @router.post("/scan", response_model=ScanResponse)
    async def scan(self, request: ScanRequest):
        pass

    @router.post("/scan/late", response_model=ScanResponse)
    async def scan_late(self, request: LateScanRequest):
        pass

    @router.post("/absence_report")
    async def get_absence_report(self, request: MisdarRequest):
        pass

    @router.post("/summary_report")
    async def get_summary_report(self, request: MisdarRequest):
        pass

    @router.get("/types", response_model=List[MisdarType])
    async def get_types(self):
        pass
