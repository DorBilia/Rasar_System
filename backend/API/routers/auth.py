from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_restful.cbv import cbv
from sqlalchemy.exc import IntegrityError
from starlette.authentication import AuthenticationError

from API.schemas.auth import *
from Services.Interfaces.user import IUserService
from core.dependencies import get_user_service
from security import sign_token
from settings import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer(auto_error=False)

REFRESH_KEY = "refresh_token"
REFRESH_AGE = settings.REFRESH_TOKEN_EXPIRES_SECONDS

CSRF_KEY = "signed_csrf_token"
CSRF_AGE = settings.CSRF_TOKEN_EXPIRES_SECONDS


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
    async def login(self, request: AuthRequest, response: Response):
        tokens = await self.service.login(request)
        if tokens is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        signed_csrf = sign_token(tokens.csrf_token)

        response.set_cookie(
            key=REFRESH_KEY,
            value=tokens.refreshToken,
            httponly=True,
            secure=True, 
            samesite="lax",
            max_age=REFRESH_AGE
        )

        response.set_cookie(
            key=CSRF_KEY,
            value=signed_csrf,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=CSRF_AGE
        )

        return tokens

    @router.post("/refresh", response_model=TokenResponse)
    async def refresh(self, response: Response, refresh_token: str | None = Cookie(default=None),
                      signed_csrf: str | None = Cookie(default=None, alias=CSRF_KEY),  # Read cookie
                      csrf_token: str | None = Header(default=None)):

        if not signed_csrf or not csrf_token:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="CSRF credentials missing")

        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token missing from cookies")
        try:
            new_tokens = await self.service.refresh(refresh_token, signed_csrf)
            new_signed_csrf = sign_token(new_tokens.csrf_token)

            response.set_cookie(
                key=REFRESH_KEY,
                value=new_tokens.refreshToken,
                httponly=True,
                secure=True,
                samesite="lax",
                max_age=REFRESH_AGE
            )

            response.set_cookie(
                key=CSRF_KEY,
                value=new_signed_csrf,
                httponly=True,
                secure=True,
                samesite="lax",
                max_age=CSRF_AGE
            )
            return new_tokens

        except ValueError as e:
            if str(e) == "invalid_refresh":
                response.delete_cookie(key=REFRESH_KEY)
                response.delete_cookie(key=CSRF_KEY)
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired refresh/csrf token",
                )
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    @router.post("/revoke")
    async def revoke(self, response: Response, refresh_token: str | None = Cookie(default=None)):  # Read from cookie
        if refresh_token:
            await self.service.revoke(refresh_token)

        response.delete_cookie(key=REFRESH_KEY)
        return {"detail": "Logged out successfully"}

    @router.get("/me", response_model=UserResponse)
    async def me(self, creds: HTTPAuthorizationCredentials = Depends(security)):
        try:

            user = await self.service.authenticate_user(
                AuthCredentials(scheme=creds.scheme.lower(), credentials=creds.credentials))
            return user

        except AuthenticationError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )
