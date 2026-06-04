from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from core.enums import RoleNameEnum


class AdminCreateUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: RoleNameEnum = RoleNameEnum.VIEWER
    is_active: bool = True


class AdminUpdateUserRequest(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=8, max_length=128)
    role: Optional[RoleNameEnum] = None
    is_active: Optional[bool] = None


class AdminUserResponse(BaseModel):
    uuid: str
    email: str
    role: RoleNameEnum
    is_active: bool
    created_at: date

    model_config = ConfigDict(from_attributes=True)
