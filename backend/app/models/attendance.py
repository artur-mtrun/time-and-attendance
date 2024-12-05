from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from .base import Base, TimestampMixin

class AttendanceLog(Base, TimestampMixin):
    __tablename__ = "attendance_logs"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    terminal_id = Column(Integer, ForeignKey("terminals.id"))
    timestamp = Column(DateTime, nullable=False)
    event_type = Column(String(10), nullable=False)  # 'IN' lub 'OUT' 