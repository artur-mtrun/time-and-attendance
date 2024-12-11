from datetime import datetime
from sqlalchemy.orm import Session
from ..models.attendance_all import AttendanceAll
from ..models.employee import Employee
from ..schemas.attendance_all import AttendanceAllCreate
from sqlalchemy import and_

class AttendanceAllService:
    @staticmethod
    def get_all(db: Session, start_date: str = None, end_date: str = None):
        query = db.query(
            AttendanceAll,
            Employee.name.label('employee_name')
        ).outerjoin(
            Employee,
            AttendanceAll.enroll_number == Employee.enroll_number
        )
        
        if start_date and end_date:
            try:
                start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
                end_datetime = datetime.strptime(end_date, '%Y-%m-%d').replace(
                    hour=23, minute=59, second=59
                )
                
                query = query.filter(and_(
                    AttendanceAll.event_timestamp >= start_datetime,
                    AttendanceAll.event_timestamp <= end_datetime
                ))
            except ValueError as e:
                print(f"Błąd parsowania daty: {e}")
                pass
        
        results = query.order_by(AttendanceAll.event_timestamp.desc()).all()
        
        return [
            {
                **row[0].__dict__,
                'employee_name': row[1],
                '_sa_instance_state': None
            } for row in results
        ]

    @staticmethod
    def create(db: Session, attendance: AttendanceAllCreate):
        db_attendance = AttendanceAll(**attendance.model_dump())
        db.add(db_attendance)
        db.commit()
        db.refresh(db_attendance)
        return db_attendance

    @staticmethod
    def get_by_id(db: Session, attendance_id: int):
        return db.query(AttendanceAll).filter(AttendanceAll.id == attendance_id).first()

    @staticmethod
    def update_sync_status(db: Session, attendance_id: int, is_sync: bool):
        attendance = db.query(AttendanceAll).filter(AttendanceAll.id == attendance_id).first()
        if attendance:
            attendance.is_sync = is_sync
            db.commit()
            db.refresh(attendance)
        return attendance


attendance_all_service = AttendanceAllService() 