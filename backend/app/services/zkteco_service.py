from typing import List, Dict, Any
import requests
import logging
from app.core.config import settings
from app.services.terminal import TerminalService
from sqlalchemy.orm import Session
from requests.exceptions import Timeout, ConnectionError
from fastapi import HTTPException

# Konfiguracja loggera
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class ZKTecoService:
    def __init__(self, db: Session):
        self.base_url = settings.ZKTECO_API_URL
        self.db = db
        self.timeout = 5  # 5 sekund timeoutu
        logger.debug(f"Inicjalizacja ZKTecoService z URL: {self.base_url}")
        
    def get_all_employees(self) -> List[Dict[Any, Any]]:
        """Pobiera wszystkich pracowników z API ZKTeco"""
        try:
            master_terminal = TerminalService.get_master_terminal(self.db)
            if not master_terminal:
                logger.error("Nie znaleziono czytnika wzorcowego w bazie")
                raise Exception("Nie znaleziono czytnika wzorcowego")
            
            logger.info(f"Znaleziono czytnik wzorcowy: IP={master_terminal.ip_address}, Port={master_terminal.port}")
            
            device_request = {
                "ipAddress": master_terminal.ip_address,
                "port": master_terminal.port,
                "deviceNumber": master_terminal.number
            }
            
            logger.debug(f"Wysyłam request do API ZKTeco: {device_request}")
            
            response = requests.post(
                f"{self.base_url}/api/Employee/get-all",
                json=device_request,
                timeout=self.timeout  # dodajemy timeout
            )
            
            logger.debug(f"Status odpowiedzi: {response.status_code}")
            logger.debug(f"Treść odpowiedzi: {response.text}")
            
            response_data = response.json()
            
            # Sprawdź strukturę odpowiedzi
            if isinstance(response_data, dict) and 'data' in response_data:
                employees_data = response_data['data']
                logger.info(f"Pobrano {len(employees_data)} pracowników z czytnika")
                return employees_data
            else:
                logger.error("Nieoczekiwana struktura odpowiedzi API")
                raise Exception("Nieoczekiwana struktura odpowiedzi API")
            
        except Timeout:
            raise HTTPException(
                status_code=504,
                detail="Timeout podczas połączenia z czytnikiem"
            )
        except ConnectionError:
            raise HTTPException(
                status_code=503,
                detail="Nie można połączyć się z czytnikiem"
            )
        except Exception as e:
            logger.error(f"Nieoczekiwany błąd: {str(e)}")
            raise 