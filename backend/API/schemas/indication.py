from datetime import date
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from core.enums import IndicationDescriptionEnum


class IndicationType(BaseModel):
    id: int
    description: IndicationDescriptionEnum


class SoldierIndicationRequest(BaseModel):
    soldier_id: str
    type_id: int
    start_date: date
    end_date: date

    model_config = ConfigDict(from_attributes=True)


class SoldierIndicationResponse(SoldierIndicationRequest):
    id: int


class OrganizationIndicationMinimal(BaseModel):
    id: int
    type: str
    start_date: date
    end_date: date
    soldiers_affected: int

    model_config = ConfigDict(from_attributes=True)


class OrganizationIndicationRequest(BaseModel):
    section_id: Optional[int] = None
    branch_id: Optional[int] = None
    type_id: int
    start_date: date
    end_date: date
    additional_soldiers: Optional[List[int]] = None

    model_config = ConfigDict(from_attributes=True)


class OrganizationIndicationResponse(OrganizationIndicationRequest):
    id: int
