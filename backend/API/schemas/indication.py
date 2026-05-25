from datetime import date
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from core.enums import IndicationDescriptionEnum


class IndicationType(BaseModel):
    id: int
    indication_description: IndicationDescriptionEnum
    model_config = ConfigDict(from_attributes=True)


class SoldierIndicationRequest(BaseModel):
    soldier_id: int
    indication_type: int
    start_date: date
    end_date: date
    organization_uuid: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class SoldierIndicationResponse(SoldierIndicationRequest):
    uuid: str


class SoldierIndicationWithDescription(SoldierIndicationResponse):
    indication_description: IndicationDescriptionEnum


class OrganizationIndicationMinimal(BaseModel):
    """uuid, type,start/end dates and list of additional soldiers ids"""
    uuid: str
    indication_type: int
    start_date: date
    end_date: date
    additional_soldiers: Optional[List[int]] = None

    model_config = ConfigDict(from_attributes=True)


class OrganizationIndicationRequest(BaseModel):
    section_id: Optional[int] = None
    branch_id: Optional[int] = None
    indication_type: int
    start_date: date
    end_date: date
    additional_soldiers: Optional[List[int]] = None

    model_config = ConfigDict(from_attributes=True)


class OrganizationIndicationResponse(OrganizationIndicationRequest):
    uuid: str
