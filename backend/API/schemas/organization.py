from typing import Optional

from pydantic import BaseModel, ConfigDict


class CreateUnitRequest(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class UnitSchema(CreateUnitRequest):
    id: int


class UpdateUnitRequest(BaseModel):
    name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CreateBranchRequest(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class BranchSchema(CreateBranchRequest):
    id: int


class UpdateBranchRequest(BaseModel):
    name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CreateSectionRequest(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class SectionSchema(CreateSectionRequest):
    id: int


class UpdateSectionRequest(BaseModel):
    name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
