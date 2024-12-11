from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import logging
from app.database import get_db
from app.schemas.attendance_all import AttendanceAllResponse
from app.services.attendance_all import attendance_all_service
from app.services.zkteco_service import ZKTecoService
from app.models.terminal import Terminal
from app.models.attendance_all import AttendanceAll
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(tags=["attendance_all"])

class TerminalIdsRequest(BaseModel):
    terminal_ids: List[int]

@router.get("/attendance-all", response_model=List[AttendanceAllResponse])
def get_attendance_all(
    start_date: str = Query(None),
    end_date: str = Query(None),
    db: Session = Depends(get_db)
):
    logger.debug(f"Otrzymano żądanie z parametrami: start_date={start_date}, end_date={end_date}")
    return attendance_all_service.get_all(db, start_date, end_date)

@router.post("/attendance-all/fetch-from-terminals")
async def fetch_from_terminals(
    request: TerminalIdsRequest,
    db: Session = Depends(get_db)
):
    try:
        zkteco_service = ZKTecoService(db)
        results = []
        total_records = 0
        
        for terminal_id in request.terminal_ids:
            terminal = db.query(Terminal).filter(Terminal.id == terminal_id).first()
            if not terminal:
                continue
                
            try:
                attendance_data = zkteco_service.get_attendance_from_terminal(terminal)
                valid_records = 0
                
                # Zapisz dane do bazy
                for record in attendance_data:
                    try:
                        new_record = AttendanceAll(
                            enroll_number=record['enrollNumber'],
                            terminal_id=terminal.id,
                            event_timestamp=record['timestamp'] or None,
                            in_out_mode=int(record['inOutMode'] or 0),
                            verify_mode=int(record['verifyMode'] or 0),
                            work_code=int(record.get('workCode', 0) or 0),
                            is_sync=True
                        )
                        db.add(new_record)
                        valid_records += 1
                        
                        # Commit co 100 rekordów
                        if valid_records % 100 == 0:
                            db.commit()
                            
                    except Exception as e:
                        logger.error(f"Błąd podczas przetwarzania rekordu: {str(e)}, record: {record}")
                        continue
                
                # Końcowy commit dla pozostałych rekordów
                if valid_records % 100 != 0:
                    db.commit()
                
                results.append({
                    'terminal_id': terminal.id,
                    'terminal_name': terminal.name,
                    'status': 'success',
                    'message': f'Zapisano {valid_records} zdarzeń'
                })
                total_records += valid_records
                
            except Exception as e:
                logger.error(f"Błąd dla terminala {terminal.name} (ID: {terminal.id}): {str(e)}")
                results.append({
                    'terminal_id': terminal.id,
                    'terminal_name': terminal.name,
                    'status': 'error',
                    'message': str(e)
                })
        
        return {
            'message': f'Zapisano łącznie {total_records} zdarzeń',
            'details': results
        }
        
    except Exception as e:
        logger.error(f"Błąd podczas pobierania zdarzeń: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )