import asyncio
from db.db import get_db
from db.db import create_tables
from core.enums import RankEnum, ServiceTypeEnum
from datetime import date
from Repositories.soldier import SoldierRepository
from Repositories.biror import BirorResultRepository, BirorRepository, BirorTypeRepository


async def main():
    await create_tables()

    async with get_db() as db:
        # Create Soldier

        soldier_repo = SoldierRepository(db)
        soldier = await soldier_repo.create(
            first_name="David",
            last_name="Levi",
            rank=RankEnum.TORAI,
            picture=None,
            discharge_date=date(2027, 5, 12),
            service_type=ServiceTypeEnum.MANDATORY,
            unit="Unit1",
            branch="Branch1",
            department="Dept1",
            other_allocations="",
            phone_number="0501234567"
        )
        print("Soldier:", soldier)

        # Create BirorResult
        biror_result_repo = BirorResultRepository(db)
        biror_result = await biror_result_repo.create(
            biror_result_description="עונש"
        )
        print("BirorResult:", biror_result)

        # Create Biror for that soldier
        biror_repo = BirorRepository(db)
        # For BirorType, get or create one using the repository
        biror_type_repo = BirorTypeRepository(db)
        biror_types = await biror_type_repo.get_all()
        biror_type_obj = None
        for bt in biror_types:
            if bt.biror_type_description == "הופעה ולבוש":
                biror_type_obj = bt
                break
        if not biror_type_obj:
            biror_type_obj = await biror_type_repo.create(biror_type_description="הופעה ולבוש")

        biror = await biror_repo.create(
            soldier_id=soldier.id,
            biror_type=biror_type_obj.id,
            biror_date=date.today(),
            biror_description="Test Biror",
            comments=None,
            biror_result=biror_result.id
        )
        print("Biror:", biror)


if __name__ == "__main__":
    asyncio.run(main())
