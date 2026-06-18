import uuid
from typing import List, Optional

from fastapi import UploadFile

from API.schemas.indication import SoldierIndicationRequest
from db.models import Doh1, Indication

MAX_FILE_SIZE = 1024 * 1024 * 10 # 10Mb

class ExcelCols:
    ID = "מס. אישי"
    DATE = "ת.ת. סטטוס"
    STATUS = "סטטוס ראשי"


async def excel_to_doh1(records: List[dict]) -> List[Doh1]:
    return [Doh1(
        soldier_id=record[ExcelCols.ID],
        doh1_date=record[ExcelCols.DATE],
        doh1_value=record[ExcelCols.STATUS]
    ) for record in records]


async def to_Indication_list(requests: List[SoldierIndicationRequest], org_id: Optional[int]) -> List[Indication]:
    result = []
    for request in requests:

        indication = Indication(
            soldier_id=request.soldier_id, indication_type=request.indication_type, start_date=request.start_date,
            end_date=request.end_date, uuid=str(uuid.uuid4()))

        if org_id is not None:
            indication.organization_id = org_id

        result.append(indication)

    return result

async def enforce_size_limit(file: UploadFile):
    file_size = 0
    # Read in 8KB chunks
    for chunk in file.file:
        file_size += len(chunk)
        if file_size > MAX_FILE_SIZE:
            return False
    return True