from datetime import date, time
from typing import Optional

from pydantic import BaseModel, ConfigDict

from core.enums import MisdarNameEnum


class MisdarType(BaseModel):
    id: int
    misdar_name: MisdarNameEnum


class ScanRequest(BaseModel):
    misdar_type: int
    soldier_id: int

    model_config = ConfigDict(from_attributes=True)


class ScanResponse(BaseModel):
    soldier_id: int
    scan_note: str

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
