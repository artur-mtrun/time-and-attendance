from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AttendanceAllBase(BaseModel):
    enroll_number: str
    terminal_id: int
    event_timestamp: datetime
    in_out_mode: Optional[int] = None
    verify_mode: Optional[int] = None
    work_code: Optional[int] = None
    is_sync: bool = False

class AttendanceAllCreate(AttendanceAllBase):
    pass

class AttendanceAllResponse(AttendanceAllBase):
    id: int
    employee_name: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "enroll_number": "60000",
                "terminal_id": 1,
                "event_timestamp": "2024-12-11T10:55:20",
                "in_out_mode": 2,
                "verify_mode": 1,
                "work_code": 0,
                "is_sync": True
            }
        }