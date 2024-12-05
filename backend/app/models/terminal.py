from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .base import Base, TimestampMixin

class Terminal(Base, TimestampMixin):
    __tablename__ = "terminals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    ip_address = Column(String(15), nullable=False)
    port = Column(Integer, default=4370)
    is_active = Column(Boolean, default=True)
    last_sync_at = Column(DateTime, nullable=True) 