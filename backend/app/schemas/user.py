from pydantic import BaseModel
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    username: str
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 