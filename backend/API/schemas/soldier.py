from datetime import date
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from core.enums import RankEnum, ServiceTypeEnum, Doh1ValueEnum


class MinimalSoldier(BaseModel):
    id: int
    first_name: str
    last_name: str
    rank: RankEnum
    picture: Optional[str] = None
    branch: Optional[int] = None
    section: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class FullSoldier(MinimalSoldier):
    unit: Optional[int] = None
    discharge_date: Optional[date] = None
    service_type: Optional[ServiceTypeEnum] = None
    other_allocations: Optional[str] = None
    phone_number: Optional[str] = None


class BaseSoldierRequest(BaseModel):
    unit: Optional[int] = None
    branch: Optional[int] = None
    section: Optional[int] = None
    rank: Optional[RankEnum] = None
    discharge_date: Optional[date] = None
    service_type: Optional[ServiceTypeEnum] = None
    phone_number: Optional[str] = None


class FilterSoldiersRequest(BaseSoldierRequest):
    indication_type: Optional[int] = None
    search_term: Optional[str] = None
    next_cursor_id: Optional[int] = None
    limit: int = 50


class FilterSoldiersResponse(BaseModel):
    soldiers: Optional[List[MinimalSoldier]] = None
    next_cursor_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class UpdateSoldierRequest(BaseSoldierRequest):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    picture: Optional[str] = None
    other_allocations: Optional[str] = None


class Doh1Request(BaseModel):
    soldier_id: int
    doh1_date: Optional[date] = date.today()
    doh1_value: Doh1ValueEnum
