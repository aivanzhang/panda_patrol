from pydantic import BaseModel
from datetime import datetime


class PatrolRunCreate(BaseModel):
    patrol_group: str
    patrol: str
    status: str
    severity: str
    start_time: datetime
    end_time: datetime
    patrol_code: str
    logs: str
    return_value: str
    duration: float
    exception: str


class SuccessResponse(BaseModel):
    success: bool
