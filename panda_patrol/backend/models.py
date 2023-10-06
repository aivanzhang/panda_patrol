from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: str


class PatrolRunCreate(BaseModel):
    user_id: int
    patrol_group: str
    patrol: str
    status: str
    severity: str
    patrol_code: str
    logs: str
    return_value: str
    start_time: datetime
    end_time: datetime
    exception: str


class SuccessResponse(BaseModel):
    success: bool
