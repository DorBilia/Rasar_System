from fastapi import APIRouter, Depends,HTTPException
from fastapi_restful.cbv import cbv
from API.schemas.user import *
from Services.Interfaces.user import IUserService
from core.dependecies.user import get_user_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@cbv(router)
class AuthRouter:
    service: IUserService = Depends(get_user_service)

    @router.post('/register', response_model=UserResponse)
    async def register(self, request: UserRequest):
        try:
            return await self.service.register(request)
        except ValueError as e:
            raise HTTPException(status_code=400, detail="user with this soldier id already exists")

    # TODO: create a schema for a JWT token and handle login in a service
    @router.post("/login")
    async def login(self, soldier_id: int, password: str):
        pass
