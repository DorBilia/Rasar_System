from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict

from core.enums import RankEnum, ServiceTypeEnum


class FilterSoldiersRequest(BaseModel):
    unit: Optional[int] = None
    branch: Optional[int] = None
    department: Optional[int] = None
    rank: Optional[str] = None
    discharge_date: Optional[str] = None
    service_type: Optional[str] = None
    phone_number: Optional[str] = None
    indication_type: Optional[str] = None
    search_term: Optional[str] = None
    limit: int = 50


class BaseSoldier(BaseModel):
    id: int
    first_name: str
    last_name: str
    rank: RankEnum
    picture: Optional[str] = None
    branch: str
    department: str

    model_config = ConfigDict(from_attributes=True)


class FullSoldier(BaseSoldier):
    unit: str
    discharge_date: Optional[date] = None
    service_type: Optional[ServiceTypeEnum] = None
    other_allocations: Optional[str] = None
    phone_number: Optional[str] = None


class UpdateSoldierRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    rank: Optional[RankEnum] = None
    picture: Optional[str] = None
    branch: Optional[str] = None
    department: Optional[str] = None
    unit: Optional[str] = None
    discharge_date: Optional[date] = None
    service_type: Optional[ServiceTypeEnum] = None
    other_allocations: Optional[str] = None
    phone_number: Optional[str] = None
