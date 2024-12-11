from sqlalchemy import and_, exists
from sqlalchemy.orm import Session
from ..models.attendance_all import AttendanceAll
from ..models.attendance import AttendanceLog
from ..models.employee import Employee
import logging

logger = logging.getLogger(__name__)

class SyncService:
    @staticmethod
    def sync_attendance_logs(db: Session, batch_size: int = 1000):
        try:
            # Licznik zsynchronizowanych rekordów
            synced_count = 0
            
            while True:
                # Pobierz partię niezsynchornizowanych rekordów
                records_to_sync = db.query(AttendanceAll).filter(
                    AttendanceAll.is_sync == False
                ).join(
                    Employee,
                    AttendanceAll.enroll_number == Employee.enroll_number
                ).limit(batch_size).all()

                if not records_to_sync:
                    break

                for record in records_to_sync:
                    # Sprawdź czy już istnieje taki wpis
                    exists_query = db.query(exists().where(
                        and_(
                            AttendanceLog.enroll_number== record.enroll_number,
                            AttendanceLog.terminal_id == record.terminal_id,
                            AttendanceLog.event_timestamp == record.event_timestamp,
                            AttendanceLog.verify_mode == record.verify_mode
                        )
                    )).scalar()

                    if not exists_query:
                        # Znajdź pracownika
                        employee = db.query(Employee).filter(
                            Employee.enroll_number == record.enroll_number
                        ).first()
                        
                        if employee:
                            # Dodaj nowy wpis do attendance_logs
                            new_log = AttendanceLog(
                                employee_id=employee.id,
                                terminal_id=record.terminal_id,
                                event_timestamp=record.event_timestamp,
                                in_out_mode=record.in_out_mode,
                                verify_mode=record.verify_mode,
                                work_code=record.work_code
                            )
                            db.add(new_log)

                    # Oznacz rekord jako zsynchronizowany
                    record.is_sync = True
                    synced_count += 1

                # Commit dla każdej partii
                db.commit()
                
            return {"message": f"Zsynchronizowano {synced_count} rekordów"}

        except Exception as e:
            db.rollback()
            logger.error(f"Błąd podczas synchronizacji: {str(e)}")
            raise 