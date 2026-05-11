import asyncio
from contextlib import asynccontextmanager
from db.db import get_db
from fastapi import FastAPI
from core.enums import BirorResultEnum
from Repositories.biror import BirorResultRepository
from db.db import create_tables


async def main():
    await create_tables()

    async with get_db() as db:
        repository = BirorResultRepository(db)
        res = await (repository.create(**{"id": 5, "biror_result_description": "עונש"}))
        print(res.biror_result_description.value)


if __name__ == "__main__":
    asyncio.run(main())

