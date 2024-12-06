from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .base import Base, TimestampMixin

class Terminal(Base, TimestampMixin):
    __tablename__ = "terminals"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    ip_address = Column(String(15), nullable=False)
    port = Column(Integer, default=4370)
    is_active = Column(Boolean, default=True)
    is_main = Column(Boolean, default=False)
    last_sync_at = Column(DateTime, nullable=True) 