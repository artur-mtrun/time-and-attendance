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
            processed_count = 0    
            added_count = 0        
            duplicate_count = 0    
            no_employee_count = 0  
            
            # Sprawdź czy są jakiekolwiek rekordy do synchronizacji
            records_exist = db.query(AttendanceAll).filter(
                AttendanceAll.is_sync == False
            ).first() is not None

            if not records_exist:
                return {
                    "message": "Brak rekordów do synchronizacji",
                    "statystyki": {
                        "przetworzone_rekordy": 0,
                        "dodane_nowe": 0,
                        "już_istniejące": 0,
                        "bez_pracownika": 0
                    }
                }
            
            while True:
                records_to_sync = db.query(AttendanceAll).filter(
                    AttendanceAll.is_sync == False
                ).limit(batch_size).all()

                if not records_to_sync:
                    break

                for record in records_to_sync:
                    try:
                        exists_query = db.query(exists().where(
                            and_(
                                AttendanceLog.enroll_number == record.enroll_number,
                                AttendanceLog.terminal_number == record.terminal_number,
                                AttendanceLog.event_timestamp == record.event_timestamp,
                                AttendanceLog.verify_mode == record.verify_mode
                            )
                        )).scalar()

                        if exists_query:
                            duplicate_count += 1
                        else:
                            employee = db.query(Employee).filter(
                                Employee.enroll_number == record.enroll_number
                            ).first()
                            
                            if employee:
                                new_log = AttendanceLog(
                                    enroll_number=record.enroll_number,
                                    terminal_number=record.terminal_number,
                                    event_timestamp=record.event_timestamp,
                                    in_out_mode=record.in_out_mode,
                                    verify_mode=record.verify_mode,
                                    work_code=record.work_code
                                )
                                db.add(new_log)
                                added_count += 1
                            else:
                                no_employee_count += 1

                        record.is_sync = True
                        processed_count += 1
                        
                    except Exception as e:
                        logger.error(f"Błąd podczas przetwarzania rekordu {record.id}: {str(e)}")
                        continue

                db.commit()
                
            return {
                "message": f"Zakończono synchronizację pomyślnie",
                "statystyki": {
                    "przetworzone_rekordy": processed_count,
                    "dodane_nowe": added_count,
                    "już_istniejące": duplicate_count,
                    "bez_pracownika": no_employee_count
                }
            }

        except Exception as e:
            db.rollback()
            logger.error(f"Błąd podczas synchronizacji: {str(e)}")
            raise 