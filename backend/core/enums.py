"""Domain enums for the Rasar military attendance system.

These enums are used by SQLAlchemy models and are stored as VARCHAR in the DB
via `sqlalchemy.Enum(..., native_enum=False)`.
"""

from __future__ import annotations

from enum import Enum


class RankEnum(str, Enum):
    TORAI = "טוראי"
    RABAT = "רב\"ט"
    SAMAL = "סמל"
    SAMAR = "סמ\"ר"
    RASAL = "רס\"ל"
    RASAR = "רס\"ר"
    RASAM = "רס\"מ"
    RASAB = "רס\"מ"
    RANAM = "רנ\"מ"
    RANAG = "רנ\"ג"
    SAGAM = "סג\"מ"
    SEGEN = "סגן"
    SEREN = "סרן"
    RASAN = "רס\"ן"
    SAAL = "סא\"ל"
    ALAM = "אל\"מ"
    TAAL = "תא\"ל"
    ALOF = "אלוף"
    RAAL = "רא\"ל"


class ServiceTypeEnum(str, Enum):
    MANDATORY = "חובה"
    CAREER = "קבע"
    RESERVE = "מילואים"
    CITIZEN = "אע\"ץ"


class Doh1ValueEnum(str, Enum):
    PRESENT = "נוכח ביחידה"
    VACATION = "חופשה שנתית"
    SICK = "חופשת מחלה"
    OUTSIDE_SERVICE = "בתפקיד מחוץ ליחידה"
    COURSE = "קורס/הכשרה"
    HOSPITALIZED = "אשפוז"
    AFTER_SERVICE = "לאחר תורנות/משמרת"


class ScanNote(str, Enum):
    SUCCESS = "successful"
    CONFLICT = "conflict with indication"
    SOLDIER_NOT_FOUND = "soldier does not exist"
    SOLDIER_INACTIVE = "soldier inactive"
    DOH1_NOT_PRESENT = "doh1 not present"


class RoleNameEnum(str, Enum):
    ADMIN = "admin"
    RAMAD = "רמ\"ד"
    RAAN = "רע\"ן"
    UNIT_COMMANDER = "מפקד יחידה"
    RASAR = "רס\"ר"
    VIEWER = "צופה"


class DayOfWeek(int, Enum):
    SUNDAY = 1
    MONDAY = 2
    TUESDAY = 3
    WEDNESDAY = 4
    THURSDAY = 5
    FRIDAY = 6
    SATURDAY = 7
