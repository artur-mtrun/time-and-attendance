from pydantic_settings import BaseSettings
from datetime import timedelta

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str = "your-secret-key-here"  # W produkcji użyj bezpiecznego klucza!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ZKTECO_API_URL: str = "http://10.0.1.38:5000"  # Poprawiony URL do API ZKTeco

    class Config:
        env_file = ".env"

settings = Settings() 