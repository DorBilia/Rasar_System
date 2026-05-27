from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi_restful.cbv import cbv
from starlette import status
from sqlalchemy.exc import IntegrityError

from API.schemas.misdar import *
from Services.Interfaces.misdar import IMisdarService
from Services.misdar import DuplicateMisdarScanError, MisdarTypeNotFoundError
from core.dependencies.misdar import get_misdar_attendance_service

router = APIRouter(prefix="/misdars", tags=["Misdars"])


@cbv(router)
class Misdars:
    service: IMisdarService = Depends(get_misdar_attendance_service)

    @router.post("/search", response_model=List[MisdarOverviewResponse])
    async def get_misdars(self, request: SearchMisdarRequest):
        return await self.service.search(request)

    @router.post("/start_scan/{misdar_type}")
    async def start_scan(self, misdar_type: int):
        can_start = await self.service.try_scan_start(misdar_type)
        if can_start:
            return Response(status_code=status.HTTP_202_ACCEPTED)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    @router.post("/scan", response_model=ScanResponse)
    async def scan(self, request: ScanRequest):
        try:
            return await self.service.scan_active(request)
        except MisdarTypeNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="misdar type not found")
        except DuplicateMisdarScanError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="soldier already scanned for this misdar")

    @router.post("/scan/late", response_model=ScanResponse)
    async def scan_late(self, request: LateScanRequest):
        try:
            return await self.service.scan_late(request)
        except MisdarTypeNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="misdar type not found")
        except DuplicateMisdarScanError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="soldier already scanned for this misdar")

    @router.post("/absence_report")
    async def get_absence_report(self, request: MisdarRequest):
        return await self.service.get_absence_report(request)

    @router.post("/summary_report")
    async def get_summary_report(self, request: MisdarRequest):
        return await self.service.get_summary_report(request)

    @router.get("/types", response_model=List[MisdarTypeSchema])
    async def get_types(self):
        return await self.service.get_types()

    @router.post("/types", response_model=MisdarTypeSchema, status_code=status.HTTP_201_CREATED)
    async def create_type(self, request: CreateMisdarTypeRequest):
        try:
            return await self.service.create_type(request)
        except IntegrityError:
            # Covers duplicate/invalid enum combos at DB level.
            raise HTTPException(status_code=409, detail="misdar type already exists or invalid")

    @router.get("/types/{misdar_type_id}", response_model=MisdarTypeSchema)
    async def get_type(self, misdar_type_id: int):
        row = await self.service.get_type_by_id(misdar_type_id)
        if row is None:
            raise HTTPException(status_code=404, detail="misdar type not found")
        return row

    @router.put("/types/{misdar_type_id}", response_model=MisdarTypeSchema)
    async def update_type(self, misdar_type_id: int, request: UpdateMisdarTypeRequest):
        row = await self.service.update_type(misdar_type_id, request)
        if row is None:
            raise HTTPException(status_code=404, detail="misdar type not found")
        return row

    @router.delete("/types/{misdar_type_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_type(self, misdar_type_id: int):
        try:
            success = await self.service.delete_type(misdar_type_id)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="misdar type is referenced and cannot be deleted")

        if not success:
            raise HTTPException(status_code=404, detail="misdar type not found")
        return None

    @router.delete("/{scan_uuid}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_soldier(self, scan_uuid: str):
        success = await self.service.delete_scan(scan_uuid)
        if not success:
            raise HTTPException(status_code=404, detail="Scan not found")
        return None

    @router.get("/{soldier_id}/{date}/calender", response_model=List[AttendanceDay])
    async def get_calender(self, soldier_id: int, date: date):
        return await self.service.get_soldier_attendances_for_month(soldier_id, date)
