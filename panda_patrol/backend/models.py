from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PersonRequest(BaseModel):
    name: str
    email: str


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
    exception: str


class PatrolProfileCreate(BaseModel):
    patrol_group: str
    patrol: str
    report: str
    time: datetime
    format: str


class SuccessResponse(BaseModel):
    success: bool


class PatrolParameterRequest(BaseModel):
    patrol_group: str
    patrol: str
    parameter_id: str
    value: str
    type: str
    is_active: bool = True


class PatrolSettingRequest(BaseModel):
    patrol_group: str
    patrol: str
    assigned_to_person: Optional[int] = Field(None)
    alerting: bool
    silenced_until: Optional[datetime] = Field(None)


class PatrolResetParametersRequest(BaseModel):
    patrol_group: str
    patrol: str


class PatrolGroupResetParametersRequest(BaseModel):
    patrol_group: str
