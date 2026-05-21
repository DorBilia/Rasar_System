from datetime import date
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from core.enums import RankEnum, ServiceTypeEnum


class BaseSoldier(BaseModel):
    id: int
    first_name: str
    last_name: str
    rank: RankEnum
    picture: Optional[str] = None
    branch: int
    section: int

    model_config = ConfigDict(from_attributes=True)


class CreateSoldierRequest(BaseSoldier):
    unit: int
    discharge_date: Optional[date] = None
    service_type: Optional[ServiceTypeEnum] = None
    other_allocations: Optional[str] = None
    phone_number: Optional[str] = None


class MinimalSoldier(BaseSoldier):
    uuid: str


class FullSoldier(CreateSoldierRequest):
    uuid: str


class BaseSoldierRequest(BaseModel):
    unit: Optional[int] = None
    branch: Optional[int] = None
    section: Optional[int] = None
    rank: Optional[RankEnum] = None
    discharge_date: Optional[date] = None
    service_type: Optional[ServiceTypeEnum] = None
    phone_number: Optional[str] = None


class FilterSoldiersRequest(BaseSoldierRequest):
    indication_type: Optional[str] = None
    search_term: Optional[str] = None
    limit: int = 50


class UpdateSoldierRequest(BaseSoldierRequest):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    picture: Optional[str] = None
    other_allocations: Optional[str] = None
