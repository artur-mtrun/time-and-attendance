from pydantic import BaseModel
from typing import Optional

class EmployeeBase(BaseModel):
    enroll_number: str
    name: str
    password: Optional[str] = None
    card_number: Optional[str] = None
    privileges: int = 0
    is_active: bool = True

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    card_number: Optional[str] = None
    privileges: Optional[int] = None
    is_active: Optional[bool] = None

class EmployeeResponse(EmployeeBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True 