from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi_restful.cbv import cbv
from sqlalchemy.exc import IntegrityError

from API.schemas.admin import AdminCreateUserRequest, AdminUpdateUserRequest, AdminUserResponse
from API.schemas.auth import UserResponse
from Services.Interfaces.user import IUserService
from dependencies import get_user_service
from core.dependencies import get_current_user, require_admin


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_admin)]
)


@cbv(router)
class AdminUserRouter:
    service: IUserService = Depends(get_user_service)

    @router.get("/", response_model=List[AdminUserResponse])
    async def get_users(self):
        return await self.service.get_users()

    @router.post("/", response_model=AdminUserResponse, status_code=status.HTTP_201_CREATED)
    async def create_user(self, request: AdminCreateUserRequest):
        try:
            return await self.service.create_user(request)
        except ValueError as e:
            code = str(e)
            if code == "user_exists":
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="An account with this email already exists",
                )
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=code)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists",
            )

    @router.get("/{email}", response_model=AdminUserResponse)
    async def get_user_by_email(self, email: str):
        user = await self.service.get_user_by_email(email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    @router.put("/{user_uuid}", response_model=AdminUserResponse)
    async def update_user(
        self,
        user_uuid: str,
        request: AdminUpdateUserRequest,
        current_user: UserResponse = Depends(get_current_user),
    ):
        try:
            return await self.service.update_user(user_uuid, request, current_user.uuid)
        except ValueError as e:
            code = str(e)
            if code == "user_not_found":
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            if code == "user_exists":
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="An account with this email already exists",
                )
            if code in ("cannot_change_own_role", "cannot_deactivate_self"):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=code)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=code)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists",
            )

    @router.delete("/{user_uuid}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_user(
        self,
        user_uuid: str,
        current_user: UserResponse = Depends(get_current_user),
    ):
        try:
            deleted = await self.service.delete_user(user_uuid, current_user.uuid)
        except ValueError as e:
            if str(e) == "cannot_delete_self":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="cannot_delete_self")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return None
