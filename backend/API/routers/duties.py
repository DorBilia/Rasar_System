from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi_restful.cbv import cbv
from API.schemas.duties import *

router = APIRouter(prefix="/duties", tags=["Duties"])
types_router = APIRouter(prefix="/duties/types", tags=["DutiesTypes"])


@cbv(router)
class DutiesRouter:

    @router.post("/", status_code=status.HTTP_201_CREATED, response_model=DutyResponse)
    async def create_duty(self, request: CreateDutyRequest):
        pass

    @router.post("/dashboard", response_model=List[SoldierSummary])
    async def get_dashboard(self, request: DashboardFilterRequest):
        pass

    @router.post("/history", response_model=List[DutyWithScore])
    async def get_soldier_history(self, request: DutyHistoryRequest):
        pass

    @router.put("/{duty_uuid}", response_model=DutyResponse)
    async def update_duty(self, duty_uuid: str):
        pass

    @router.delete("/{duty_uuid}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_duty(self, duty_uuid: str):
        pass


@cbv(types_router)
class DutyTypeRouter:

    @types_router.post("/", response_model=DutyTypeResponse)
    async def create_duty_type(self, request: DutyTypeRequest):
        pass

    @types_router.put("/{type_id}", response_model=DutyTypeResponse)
    async def update_duty_type(self, type_id: str, updates: DutyTypeRequest):
        pass

    @types_router.delete("/{type_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_duty_type(self, type_id: str):
        pass

    @types_router.get("/", response_model=List[DutyResponse])
    async def get_duty_types(self, request: DutyTypeRequest):
        pass