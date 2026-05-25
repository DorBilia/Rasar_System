from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from core.enums import RoleNameEnum


class AuthRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class RefreshRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    refresh_token: str = Field(validation_alias="refreshToken")


class UserResponse(BaseModel):
    uuid: str
    email: str
    role: RoleNameEnum
    created_at: date

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    accessToken: str
    refreshToken: str
    tokenType: str = "Bearer"
    expiresIn: int

    model_config = ConfigDict(from_attributes=True)


class AuthCredentials(BaseModel):
    scheme: str
    credentials: str
