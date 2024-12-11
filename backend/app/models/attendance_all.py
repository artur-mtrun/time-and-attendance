from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from .base import Base, TimestampMixin

class AttendanceAll(Base, TimestampMixin):
    __tablename__ = "attendance_all"

    id = Column(Integer, primary_key=True, index=True)
    enroll_number = Column(String(50), nullable=False, index=True)
    terminal_number = Column(Integer, ForeignKey("terminals.number"), nullable=False)
    event_timestamp = Column(DateTime, nullable=False)
    in_out_mode = Column(Integer)
    verify_mode = Column(Integer)
    work_code = Column(Integer)
    is_sync = Column(Boolean, default=False) 