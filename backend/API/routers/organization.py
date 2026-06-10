from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_restful.cbv import cbv
from sqlalchemy.exc import IntegrityError
from starlette import status

from API.schemas.organization import *
from core.dependencies.organization import get_branch_service, get_section_service, get_unit_service
from Services.Interfaces.organization import IBranchService, ISectionService, IUnitService

units_router = APIRouter(prefix="/units", tags=["Units"])
branches_router = APIRouter(prefix="/branches", tags=["Branches"])
sections_router = APIRouter(prefix="/sections", tags=["Sections"])


@cbv(units_router)
class UnitRouter:
    service: IUnitService = Depends(get_unit_service)

    @units_router.get("/", response_model=List[UnitSchema])
    async def get_all(self):
        return await self.service.get_all()

    @units_router.post("/", response_model=UnitSchema, status_code=status.HTTP_201_CREATED)
    async def create(self, request: CreateUnitRequest):
        return await self.service.create(request)

    @units_router.get("/{unit_id}", response_model=UnitSchema)
    async def get_by_id(self, unit_id: int):
        row = await self.service.get_by_id(unit_id)
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="unit not found")
        return row

    @units_router.put("/{unit_id}", response_model=UnitSchema)
    async def update(self, unit_id: int, request: UpdateUnitRequest):
        row = await self.service.update(unit_id, request)
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="unit not found")
        return row

    @units_router.delete("/{unit_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete(self, unit_id: int):
        try:
            success = await self.service.delete(unit_id)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="unit is referenced and cannot be deleted",
            )
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="unit not found")
        return None


@cbv(branches_router)
class BranchRouter:
    service: IBranchService = Depends(get_branch_service)

    @branches_router.get("/", response_model=List[BranchSchema])
    async def get_all(self):
        return await self.service.get_all()

    @branches_router.post("/", response_model=BranchSchema, status_code=status.HTTP_201_CREATED)
    async def create(self, request: CreateBranchRequest):
        return await self.service.create(request)

    @branches_router.get("/{branch_id}", response_model=BranchSchema)
    async def get_by_id(self, branch_id: int):
        row = await self.service.get_by_id(branch_id)
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="branch not found")
        return row

    @branches_router.put("/{branch_id}", response_model=BranchSchema)
    async def update(self, branch_id: int, request: UpdateBranchRequest):
        row = await self.service.update(branch_id, request)
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="branch not found")
        return row

    @branches_router.delete("/{branch_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete(self, branch_id: int):
        try:
            success = await self.service.delete(branch_id)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="branch is referenced and cannot be deleted",
            )
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="branch not found")
        return None


@cbv(sections_router)
class SectionRouter:
    service: ISectionService = Depends(get_section_service)

    @sections_router.get("/", response_model=List[SectionSchema])
    async def get_all(self):
        return await self.service.get_all()

    @sections_router.post("/", response_model=SectionSchema, status_code=status.HTTP_201_CREATED)
    async def create(self, request: CreateSectionRequest):
        return await self.service.create(request)

    @sections_router.get("/{section_id}", response_model=SectionSchema)
    async def get_by_id(self, section_id: int):
        row = await self.service.get_by_id(section_id)
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="section not found")
        return row

    @sections_router.put("/{section_id}", response_model=SectionSchema)
    async def update(self, section_id: int, request: UpdateSectionRequest):
        row = await self.service.update(section_id, request)
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="section not found")
        return row

    @sections_router.delete("/{section_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete(self, section_id: int):
        try:
            success = await self.service.delete(section_id)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="section is referenced and cannot be deleted",
            )
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="section not found")
        return None
