from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, SessionLocal
from app.services.db_init import init_db
from app.scheduler import init_scheduler, scheduler
from app.routes import sync
from starlette.responses import JSONResponse
from app.dependencies.auth import oauth2_scheme
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

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

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_oauth2_redirect_url="/oauth2-redirect",
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
        "clientId": "swagger-ui",
    },
    swagger_ui_parameters={"persistAuthorization": True}
)

# Konfiguracja CORS - musi być pierwsza!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Inicjalizacja limitera
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],  # Lub konkretne nagłówki: ["Authorization", "Content-Type"]
    expose_headers=["*"]
)



@app.middleware("http")
async def authenticate_requests(request: Request, call_next):
    # Zawsze przepuszczaj OPTIONS dla CORS
    if request.method == "OPTIONS":
        response = await call_next(request)
        return response
        
    # Lista dozwolonych ścieżek bez autoryzacji
    allowed_paths = [
        "/api/auth/login",
        "/",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/oauth2-redirect"
    ]
    
    path = request.url.path
    logger.debug(f"Checking path: {path}")
    
    if path not in allowed_paths:
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Not authenticated"}
            )
    
    response = await call_next(request)
    return response

# Dodaj routery
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(terminals.router, prefix="/api")
app.include_router(employees.router, prefix="/api")
app.include_router(attendance.router, prefix="/api")
app.include_router(attendance_all.router, prefix="/api")
app.include_router(scheduler.router, prefix="/api")
app.include_router(sync.router)

# Inicjalizacja bazy danych
init_db(SessionLocal())

@app.get("/")
async def read_root():
    return {"Hello": "World"}