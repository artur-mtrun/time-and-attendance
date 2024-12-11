from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from .base import Base, TimestampMixin

class AttendanceLog(Base, TimestampMixin):
    __tablename__ = "attendance_logs"

    id = Column(Integer, primary_key=True, index=True)
    enroll_number = Column(String, ForeignKey("employees.enroll_number"))
    terminal_number = Column(Integer, ForeignKey("terminals.number"))
    event_timestamp = Column(DateTime, nullable=False)
    in_out_mode = Column(Integer, nullable=False)
    verify_mode = Column(Integer, nullable=False)
    work_code = Column(Integer, nullable=False)
    is_sync = Column(Boolean, default=False)