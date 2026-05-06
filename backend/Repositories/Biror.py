from typing import Sequence
from db.models.biror import Biror, BirorType
from AbstractRepo import AbstractRepoI
from Interfaces.biror import IBirorRepoI


class BirorRepository(AbstractRepoI[Biror], IBirorRepoI):

    def __init__(self):
        super().__init__(Biror)

    async def get_for_soldier(self, soldier_id: int) -> Sequence[Biror]:
        # implementation here
        pass


class BirorTypeRepository(AbstractRepoI[BirorType]):
    # This doesn't have any unique functions... yet
    def __init__(self):
        super().__init__(BirorType)
