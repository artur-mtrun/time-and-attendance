from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from sqlalchemy import and_
from app.models.attendance import AttendanceLog
from app.models.employee import Employee
from app.models.terminal import Terminal
from app.schemas.attendance import AttendanceCreate

class AttendanceService:
    @staticmethod
    def get_attendance_logs(db: Session, start_date: datetime = None, end_date: datetime = None):
        query = (
            db.query(
                AttendanceLog,
                Employee.name.label('employee_name'),
                Terminal.name.label('terminal_name')
            )
            .join(Employee, AttendanceLog.employee_id == Employee.id)
            .join(Terminal, AttendanceLog.terminal_id == Terminal.id)
        )

        if start_date and end_date:
            query = query.filter(
                and_(
                    AttendanceLog.event_timestamp >= start_date,
                    AttendanceLog.event_timestamp <= end_date
                )
            )

        return query.order_by(AttendanceLog.event_timestamp.desc()).all()

    @staticmethod
    def create_attendance_log(db: Session, attendance: AttendanceCreate):
        db_attendance = AttendanceLog(**attendance.model_dump())
        db.add(db_attendance)
        db.commit()
        db.refresh(db_attendance)
        return db_attendance

    @staticmethod
    def get_employee_attendance(db: Session, employee_id: int, start_date: datetime, end_date: datetime):
        return (
            db.query(AttendanceLog)
            .filter(
                and_(
                    AttendanceLog.employee_id == employee_id,
                    AttendanceLog.event_timestamp >= start_date,
                    AttendanceLog.event_timestamp <= end_date
                )
            )
            .order_by(AttendanceLog.event_timestamp)
            .all()
        ) 