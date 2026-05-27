from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Repositories.ptor import BeardStatementRepo, MedicalPtorRepo, MedicalPtorTypeRepo, BeardStatementTypeRepo
from Repositories.Interfaces.ptor import IBeardStatementRepo, IMedicalPtorRepo
from Services.ptor import BeardStatementService, MedicalPtorService
from Services.Interfaces.ptor import IBeardStatementService, IMedicalPtorService

from db.db import get_db


async def get_beard_statement_repository(db: AsyncSession = Depends(get_db)) -> IBeardStatementRepo:
    return BeardStatementRepo(db)


async def get_medical_ptor_repository(db: AsyncSession = Depends(get_db)) -> IMedicalPtorRepo:
    return MedicalPtorRepo(db)


async def get_medical_ptor_type_repository(db: AsyncSession = Depends(get_db)) -> MedicalPtorTypeRepo:
    return MedicalPtorTypeRepo(db)


async def get_beard_statement_type_repository(db: AsyncSession = Depends(get_db)) -> BeardStatementTypeRepo:
    return BeardStatementTypeRepo(db)


async def get_beard_statement_service(
        repository: IBeardStatementRepo = Depends(get_beard_statement_repository), ) -> IBeardStatementService:
    return BeardStatementService(repository)


async def get_medical_ptor_service(
        repository: IMedicalPtorRepo = Depends(get_medical_ptor_repository), ) -> IMedicalPtorService:
    return MedicalPtorService(repository)
