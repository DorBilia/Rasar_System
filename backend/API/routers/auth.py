from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_restful.cbv import cbv
from sqlalchemy.exc import IntegrityError
from starlette.authentication import AuthenticationError

from API.schemas.auth import RefreshRequest, AuthRequest, AuthRequest, TokenResponse, UserResponse, AuthCredentials
from Services.Interfaces.user import IUserService
from core.dependecies.user import get_user_service

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer(auto_error=False)


@cbv(router)
class AuthRouter:
    service: IUserService = Depends(get_user_service)

    @router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
    async def register(self, request: AuthRequest):
        try:
            return await self.service.register(request)
        except ValueError as e:
            code = str(e)
            if code == "user_exists":
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail="An account with this email already exists")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=code)
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="An account with this email already exists")
        except RuntimeError as e:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))

    @router.post("/token", response_model=TokenResponse)
    async def login(self, request: AuthRequest):
        tokens = await self.service.login(request)
        if tokens is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        return tokens

    @router.post("/refresh", response_model=TokenResponse)
    async def refresh(self, request: RefreshRequest):
        try:
            return await self.service.refresh(request.refresh_token)
        except ValueError as e:
            if str(e) == "invalid_refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired refresh token",
                )
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    @router.post("/revoke")
    async def revoke(self, request: RefreshRequest):
        await self.service.revoke(request.refresh_token)
        return {}

    @router.get("/me", response_model=UserResponse)
    async def me(self, creds: HTTPAuthorizationCredentials = Depends(security), ):
        try:

            user = await self.service.authenticate_user(
                AuthCredentials(scheme=creds.scheme.lower(), credentials=creds.credentials))
            return user

        except AuthenticationError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )
