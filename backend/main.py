import asyncio
from fastapi import FastAPI
import uvicorn
from settings import settings
from db.db import create_tables
from API.routers import soldier, indication

app = FastAPI(
    title="Rasar System API",
    description="api to manage rasar system backend",
    docs_url="/docs",
    redoc_url="/redoc",
)


async def main():
    await create_tables()

    app.include_router(soldier.router, prefix=settings.API_PREFIX)
    app.include_router(indication.indication_router, prefix=settings.API_PREFIX)
    app.include_router(indication.soldier_router, prefix=settings.API_PREFIX)
    app.include_router(indication.organization_router, prefix=settings.API_PREFIX)

    config = uvicorn.Config(app, host="localhost", port=8000, reload=True)

    server = uvicorn.Server(config)

    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
