from datetime import date

from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    soldier_id: int
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    uuid: str
    soldier_id: int
    role_id: int
    created_at: date
