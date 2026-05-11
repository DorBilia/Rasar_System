# from sqlalchemy import select, update, delete
# from typing import Optional, Sequence
# from db.models.Soldier import Soldier
# from Repositories import abstract_repo
# from sqlalchemy.ext.asyncio import AsyncSession

#
# class SoldierRepository(AbstractRepo):
#
#     async def create(self, **kwargs) -> Soldier:
#         new_soldier = Soldier(
#             **kwargs
#         )
#         self.db.add(new_soldier)
#         await self.db.commit()
#         await self.db.refresh(new_soldier)
#         return new_soldier
#
#     async def get_by_id(self, soldier_id: int) -> Optional[Soldier]:
#         result = await self.db.execute(select(Soldier).where(Soldier.id == soldier_id))
#         return result.scalar_one_or_none()
#
#     async def update(self, soldier_id: int, **updates) -> Optional[Soldier]:
#         query = (
#             update(Soldier)
#             .where(Soldier.id == soldier_id)
#             .values(**updates)
#             .execution_options(synchronize_session="fetch")
#         )
#         await self.db.execute(query)
#         await self.db.commit()
#         return await self.get_by_id(soldier_id)
#
#     async def delete(self, soldier_id: int) -> bool:
#         query = delete(Soldier).where(Soldier.id == soldier_id)
#         result = await self.db.execute(query)
#         await self.db.commit()
#         return result.rowcount > 0
#
