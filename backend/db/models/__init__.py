"""Re-export models and enums for the Rasar system.

Other parts of the app can import from `backend.db.models`, e.g.:
`from backend.db.models import Soldier, RankEnum`.
"""

from db.models.base import Base
from db.models.enums import (
    BeardStatementTypeEnum,
    BirorResultEnum,
    BirorTypeEnum,
    Doh1ValueEnum,
    GuardingTypeEnum,
    IndicationDescriptionEnum,
    MisdarNameEnum,
    RankEnum,
    RoleNameEnum,
    ServiceTypeEnum,
)
from db.models.duties import Guarding, GuardingType, Task, TaskType
from db.models.exemptions import (
    BeardStatement,
    BeardStatementType,
    MedicalPtor,
    MedicalPtorType,
)
from db.models.indications import Indication, IndicationType
from db.models.misdars import Misdar, MisdarAttendanceRecord, MisdarType
from db.models.organization import Branch, Department, Unit
from db.models.soldier import Doh1, Soldier
from db.models.biror import Biror, BirorResult, BirorType
from db.models.system import SystemVariable
from db.models.users import Role, User

__all__ = [
    # Base
    "Base",
    # Enums
    "RankEnum",
    "ServiceTypeEnum",
    "Doh1ValueEnum",
    "MisdarNameEnum",
    "IndicationDescriptionEnum",
    "BirorTypeEnum",
    "BirorResultEnum",
    "BeardStatementTypeEnum",
    "GuardingTypeEnum",
    "RoleNameEnum",
    # Organization
    "Unit",
    "Branch",
    "Department",
    # Soldier + Doh1
    "Soldier",
    "Doh1",
    # Exemptions
    "MedicalPtorType",
    "MedicalPtor",
    "BeardStatementType",
    "BeardStatement",
    # Misdars
    "MisdarType",
    "Misdar",
    "MisdarAttendanceRecord",
    # Biror
    "BirorType",
    "BirorResult",
    "Biror",
    # Indications
    "IndicationType",
    "Indication",
    # Duties
    "GuardingType",
    "Guarding",
    "TaskType",
    "Task",
    # System
    "SystemVariable",
    # Users
    "Role",
    "User",
]

