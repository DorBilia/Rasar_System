from datetime import date, time
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from core.enums import DayOfWeek


class MisdarTypeSchema(BaseModel):
    id: int
    misdar_name: str
    misdar_time: time
    misdar_length: float
    misdar_days: List[DayOfWeek]

    model_config = ConfigDict(from_attributes=True)

class CreateMisdarTypeRequest(BaseModel):
    misdar_name: str
    misdar_time: time
    misdar_length: float
    misdar_days: List[DayOfWeek]

    model_config = ConfigDict(from_attributes=True)


class UpdateMisdarTypeRequest(BaseModel):
    misdar_name: Optional[str] = None
    misdar_time: Optional[time] = None
    misdar_length: Optional[float] = None
    misdar_days: Optional[List[DayOfWeek]] = None

    model_config = ConfigDict(from_attributes=True)


class ScanRequest(BaseModel):
    misdar_type: int
    soldier_id: int

    model_config = ConfigDict(from_attributes=True)


class ScanResponse(BaseModel):
    soldier_id: int
    scan_note: str
    uuid: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class LateScanRequest(ScanRequest):
    """Also includes misdar date and scan time for late scanning
    add the original misdar date and current/custom scan time"""
    misdar_date: date
    scan_time: time


class SearchMisdarRequest(BaseModel):
    misdar_type: Optional[int] = None
    misdar_date: Optional[date] = None


class MisdarRequest(BaseModel):
    misdar_type: int
    misdar_date: date


class MisdarOverviewResponse(BaseModel):
    """misdar_date, misdar_type, scan_count"""
    misdar_date: date
    misdar_type: int
    scan_count: int

    model_config = ConfigDict(from_attributes=True)


class MisdarAttendanceStatus(BaseModel):
    misdar_type: int
    status: str


class AttendanceDay(BaseModel):
    date: date
    base_status: str

    misdar_statuses: Optional[List[MisdarAttendanceStatus]] = None


class MisdarDay(BaseModel):
    day: DayOfWeek
    misdar_type: int
