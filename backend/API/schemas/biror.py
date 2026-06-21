from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


# Biror Types
class CreateBirorTypeRequest(BaseModel):
    biror_type_description: str

    model_config = ConfigDict(from_attributes=True)


class BirorTypeSchema(CreateBirorTypeRequest):
    id: int


class UpdateBirorTypeRequest(BaseModel):
    biror_type_description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# Biror
class CreateBirorRequest(BaseModel):
    soldier_id: int
    biror_type: int
    biror_date: date
    biror_description: Optional[str] = None
    comments: Optional[str] = None
    biror_result: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class BirorSchema(CreateBirorRequest):
    uuid: str


class UpdateBirorRequest(BaseModel):
    soldier_id: Optional[int] = None
    biror_type: Optional[int] = None
    biror_date: Optional[date] = None
    biror_description: Optional[str] = None
    comments: Optional[str] = None
    biror_result: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
