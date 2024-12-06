from pydantic import BaseModel, IPvAnyAddress
from typing import Optional
from datetime import datetime

class TerminalBase(BaseModel):
    number: int
    name: str
    ip_address: str
    port: int = 4370
    is_active: bool = True
    is_main: bool = False

class TerminalCreate(TerminalBase):
    pass

class TerminalUpdate(BaseModel):
    number: Optional[int] = None
    name: Optional[str] = None
    ip_address: Optional[str] = None
    port: Optional[int] = None
    is_active: Optional[bool] = None
    is_main: Optional[bool] = None

class TerminalResponse(TerminalBase):
    id: int
    last_sync_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 