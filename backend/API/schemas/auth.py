from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class RegisterRequest(BaseModel):
    soldier_id: int
    password: str = Field(min_length=8, max_length=128)


class TokenRequest(BaseModel):
    soldier_id: int
    password: str = Field(min_length=8, max_length=128)


class RefreshRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    refresh_token: str = Field(validation_alias="refreshToken")


class UserResponse(BaseModel):
    uuid: str
    soldier_id: int
    role: str
    created_at: date


class TokenResponse(BaseModel):
    accessToken: str
    refreshToken: str
    tokenType: str = "Bearer"
    expiresIn: int


class AuthCredentials(BaseModel):
    scheme: str
    credentials: str
