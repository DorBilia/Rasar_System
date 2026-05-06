from typing import Sequence
from db.models.biror import Biror, BirorType
from abstract_repo import AbstractRepo
from Interfaces.biror import IBirorRepo


class BirorRepository(AbstractRepo[Biror], IBirorRepo):

    def __init__(self):
        super().__init__(Biror)

    async def get_for_soldier(self, soldier_id: int) -> Sequence[Biror]:
        # implementation here
        pass


class BirorTypeRepository(AbstractRepo[BirorType]):
    # This doesn't have any unique functions... yet
    def __init__(self):
        super().__init__(BirorType)
