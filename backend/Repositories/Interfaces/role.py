from abc import ABC, abstractmethod
from typing import Optional

from db.models.users import Role
from core.enums import RoleNameEnum


class IRoleRepo(ABC):

    @abstractmethod
    async def get_by_role_name(self, role_name: RoleNameEnum) -> Optional[Role]:
        pass
