from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, SessionLocal
from app.services.db_init import init_db
from app.scheduler import init_scheduler, scheduler

import logging
import sys

# Konfiguracja logowania
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Inicjalizacja schedulera przed routerami
init_scheduler()

# Importy routerów po inicjalizacji schedulera
from app.routes import auth, users, terminals, employees, attendance, attendance_all, scheduler

app = FastAPI()

# Middleware do logowania requestów
@app.middleware("http")
async def log_requests(request: Request, call_next):
    try:
        logger.debug(f"Przychodzący request: {request.method} {request.url}")
        logger.debug(f"Headers: {request.headers}")
        logger.debug(f"Client host: {request.client.host}")
        
        response = await call_next(request)
        
        logger.debug(f"Status odpowiedzi: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Błąd podczas przetwarzania requestu: {str(e)}", exc_info=True)
        raise

# Konfiguracja CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dodaj routery
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(terminals.router, prefix="/api")
app.include_router(employees.router, prefix="/api")
app.include_router(attendance.router, prefix="/api")
app.include_router(attendance_all.router, prefix="/api")
app.include_router(scheduler.router, prefix="/api")

# Inicjalizacja bazy danych
init_db(SessionLocal())

@app.get("/")
async def read_root():
    return {"Hello": "World"}