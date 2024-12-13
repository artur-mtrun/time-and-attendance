import requests
import json
import logging

# Konfiguracja logowania
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def sync_attendance():
    # Konfiguracja
    BASE_URL = "http://localhost:8000"
    LOGIN_URL = f"{BASE_URL}/api/login"
    SYNC_URL = f"{BASE_URL}/api/sync/dbsyncattendance"
    
    # Dane logowania - dostosuj do swoich danych
    login_data = {
        "username": "admin",
        "password": "admin"
    }
    
    try:
        # Logowanie i pobranie tokenu
        login_response = requests.post(LOGIN_URL, data=login_data)
        login_response.raise_for_status()
        
        token = login_response.json()["access_token"]
        logger.info("Zalogowano pomyślnie")
        
        # Wywołanie synchronizacji
        headers = {
            "Authorization": f"Bearer {token}",
            "accept": "application/json"
        }
        
        logger.debug(f"Wysyłanie żądania do: {SYNC_URL}")
        logger.debug(f"Headers: {headers}")
        
        sync_response = requests.post(SYNC_URL, headers=headers)
        sync_response.raise_for_status()
        
        result = sync_response.json()
        logger.debug(f"Otrzymana odpowiedź: {sync_response.status_code}")
        logger.debug(f"Treść odpowiedzi: {sync_response.text}")
        
        print(f"\nWynik synchronizacji: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Błąd podczas wykonywania requestu: {str(e)}")
    except Exception as e:
        logger.error(f"Wystąpił nieoczekiwany błąd: {str(e)}", exc_info=True)

if __name__ == "__main__":
    sync_attendance()