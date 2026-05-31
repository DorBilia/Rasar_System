from datetime import date
from typing import Optional, Annotated

from pydantic import BaseModel, ConfigDict
from pydantic.dataclasses import dataclass


class DashboardFilterRequest(BaseModel):
    branch: Optional[int]
    section: Optional[int]
    target_month: date


class SoldierSummary(BaseModel):
    """A soldier's summary on the dashboard"""
    soldier_id: str
    full_name: str
    total_weighted_score: float

    model_config = ConfigDict(from_attributes=True)


class CreateDutyRequest(BaseModel):
    soldier_id: int
    duty_type: int
    start_date: date
    end_date: date

    model_config = ConfigDict(from_attributes=True)


class DutyResponse(CreateDutyRequest):
    uuid: str


class DutyWithScore(DutyResponse):
    weighted_score: float


@dataclass
class ValueRange:
    lo: int
    hi: int


class DutyTypeRequest(BaseModel):
    description: str
    difficulty: Annotated[int, ValueRange(1, 10)]


class DutyTypeResponse(DutyTypeRequest):
    id: int


class DutyHistoryRequest(BaseModel):
    soldier_id: int
    start_date: date
    end_date: date
