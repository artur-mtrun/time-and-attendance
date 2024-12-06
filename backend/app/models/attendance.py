from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from .base import Base, TimestampMixin

class AttendanceLog(Base, TimestampMixin):
    __tablename__ = "attendance_logs"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    terminal_id = Column(Integer, ForeignKey("terminals.id"))
    event_timestamp = Column(DateTime, nullable=False)
    in_out_mode = Column(Integer, nullable=False)
    verify_mode = Column(Integer, nullable=False)
    work_code = Column(Integer, nullable=False)