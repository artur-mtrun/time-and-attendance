from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AttendanceBase(BaseModel):
    employee_id: int
    terminal_id: int
    event_timestamp: datetime
    in_out_mode: int
    verify_mode: int
    work_code: int

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceResponse(AttendanceBase):
    id: int
    created_at: datetime
    updated_at: datetime
    employee_name: str  # Dodane pole dla wygody frontendu
    terminal_name: str  # Dodane pole dla wygody frontendu

    class Config:
        from_attributes = True 