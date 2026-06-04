"""FastAPI dependency providers for repositories and services."""

from .biror import (
    get_biror_repository,
    get_biror_result_repository,
    get_biror_service,
    get_biror_type_repository,
    get_biror_type_service,
    get_biror_result_service,
)
from .misdar import (
    get_misdar_attendance_repository,
    get_misdar_attendance_service,
    get_misdar_type_repository,
)
from .indication import (
    get_indication_service,
    get_indication_type_repository,
    get_organization_indication_repository,
    get_organization_indication_service,
    get_soldier_indication_repository,
    get_soldier_indication_service,
)
from .ptor import (
    get_beard_statement_repository,
    get_beard_statement_service,
    get_beard_statement_type_repository,
    get_medical_ptor_repository,
    get_medical_ptor_service,
    get_medical_ptor_type_repository,
)
from .refresh_token import get_refresh_token_repository
from .soldier import (
    get_doh1_repository,
    get_soldier_repository,
    get_soldier_service,
)
from .user import get_user_repository, get_user_service

from .auth import require_admin, get_current_user

__all__ = [
    # biror
    "get_biror_repository",
    "get_biror_type_repository",
    "get_biror_result_repository",
    "get_biror_service",
    "get_biror_type_service",
    "get_biror_result_service",
    # indication
    "get_soldier_indication_repository",
    "get_indication_type_repository",
    "get_organization_indication_repository",
    "get_indication_service",
    "get_soldier_indication_service",
    "get_organization_indication_service",
    # misdar
    "get_misdar_attendance_repository",
    "get_misdar_type_repository",
    "get_misdar_attendance_service",
    # ptor
    "get_beard_statement_repository",
    "get_medical_ptor_repository",
    "get_medical_ptor_type_repository",
    "get_beard_statement_type_repository",
    "get_beard_statement_service",
    "get_medical_ptor_service",
    # refresh_token
    "get_refresh_token_repository",
    # soldier
    "get_soldier_repository",
    "get_doh1_repository",
    "get_soldier_service",
    # user
    "get_user_repository",
    "get_user_service",
    # auth
    "require_admin",
    "get_current_user"
]
