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


class MisdarNameEnum(str, Enum):
    MORNING = "בוקר"
    LATE = "מאחרים"
    MOKED = "מוקד"


class IndicationDescriptionEnum(str, Enum):
    EXEMPT = "פטור"
    PUNISHMENT = "עונש"
    MOKED = "מוקד"
    LATE_ARRIVAL = "מאחרים"
    HONOR_MONTH = "חודש כבוד"
    RECRUITMENT = "גיוס"


class BirorTypeEnum(str, Enum):
    DISCIPLINE = "הופעה ולבוש"
    PERFORMANCE = "אי הגעה למסדרים"
    BEARD = "אירוע משמעתי"


class BirorResultEnum(str, Enum):
    ACQUITTED = "זכאי"
    PUNISHMENT_MISDARS = "עונש"
    CANCEL_BEARD = "ביטול הצהרת זקן"
    REPRIMAND = "נזיפה"
    RAMAD_JUDGEMENT = "שיפוט רמ\"ד"
    RAAN_JUDGEMENT = "שיפוט רע\"ן"
    EDUCATIONAL_PUNISHMENT = "עונש חינוכי"


class BeardStatementTypeEnum(str, Enum):
    FULL_BEARD = "זקן מלא"
    FREANCH_BEARD = "זקן צרפתי"
    MOUSTACHE = "שפם"


class GuardingTypeEnum(str, Enum):
    GUARD = "לילה"
    STANDBY = "שבת"
    DUTY = "תורנות"


class TaskAssignedByEnum(str, Enum):
    RASAR = 'רס"ר'
    MISDARI_TASK = "משימה מדורית"
    OTHER = "אחר"


class RoleNameEnum(str, Enum):
    ADMIN = "admin"
    RAMAD = "רמ\"ד"
    RAAN = "רע\"ן"
    UNIT_COMMANDER = "מפקד יחידה"
    RASAR = "רס\"ר"
    VIEWER = "צופה"
