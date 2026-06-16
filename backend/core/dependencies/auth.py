from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.authentication import AuthenticationError

from API.schemas.auth import AuthCredentials
from Services.Interfaces.user import IUserService
from dependencies import get_user_service

security = HTTPBearer()

__all__ = [
    "get_current_user",
    "require_admin",
]


async def get_current_user(user_service: IUserService = Depends(get_user_service),
                           creds: HTTPAuthorizationCredentials = Depends(security)):
    try:
        auth_creds = AuthCredentials(
            scheme=creds.scheme.lower(),
            credentials=creds.credentials
        )
        return await user_service.authenticate_user(auth_creds)

    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials")


async def require_admin(user_service: IUserService = Depends(get_user_service),
                        creds: HTTPAuthorizationCredentials = Depends(security)):
    try:
        auth_creds = AuthCredentials(
            scheme=creds.scheme.lower(),
            credentials=creds.credentials
        )
        is_admin = await user_service.verify_admin(auth_creds)

        if not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )

        return True

    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials")
