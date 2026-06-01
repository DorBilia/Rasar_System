import asyncio
from fastapi import FastAPI
import uvicorn
from settings import settings
from db.db import create_tables
from API.routers import soldier, indication, auth, misdar, biror

app = FastAPI(
    title="Rasar System API",
    description="api to manage rasar system backend",
    docs_url="/docs",
    redoc_url="/redoc")

app.include_router(soldier.soldiers_router, prefix=settings.API_PREFIX)
app.include_router(soldier.doh1_router, prefix=settings.API_PREFIX)

app.include_router(indication.indication_router, prefix=settings.API_PREFIX)
app.include_router(indication.soldier_router, prefix=settings.API_PREFIX)
app.include_router(indication.organization_router, prefix=settings.API_PREFIX)

app.include_router(auth.router, prefix=settings.API_PREFIX)

app.include_router(misdar.router, prefix=settings.API_PREFIX)

app.include_router(biror.biror_router, prefix=settings.API_PREFIX)
app.include_router(biror.biror_type_router, prefix=settings.API_PREFIX)
app.include_router(biror.biror_result_router, prefix=settings.API_PREFIX)


async def main():
    await create_tables()

    config = uvicorn.Config(app, host="localhost", port=8000, reload=True)

    server = uvicorn.Server(config)

    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
