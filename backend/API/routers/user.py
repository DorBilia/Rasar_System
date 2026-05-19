from fastapi import APIRouter
from fastapi_restful.cbv import cbv
from API.schemas.user import *

router = APIRouter(prefix="/auth", tags=["Authentication"])


@cbv(router)
class AuthRouter:
    # TODO: create a service for users and create dependency for the service

    @router.post('/register', response_model=UserResponse)
    async def register(self, soldier_id: int, password: str):
        pass

    # TODO: create a schema for a JWT token and handle login in a service
    @router.post("/login")
    async def login(self, soldier_id: int, password: str):
        pass
