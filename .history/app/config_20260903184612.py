from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "POS System"
    API_V1_STR: str = "/api/v1"
    
   
    SECRET_KEY: str = "your-secret-key-here" 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080 
    
    
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/pos"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()