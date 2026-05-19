from datetime import date

from pydantic import BaseModel, Field


class Register(BaseModel):
    soldier_id: int
    password: str = Field(min_length=8)
    role_id: int


class UserResponse(BaseModel):
    uuid: str
    soldier_id: int
    role_id: int
    created_at: date


class Login(BaseModel):
    soldier_id: int
    password: str
