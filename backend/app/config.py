"""Environment configuration using Pydantic Settings"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Configuration
    API_V1_PREFIX: str = "/api"
    PROJECT_NAME: str = "JobNova API"
    VERSION: str = "1.0.0"
    
    # CORS Configuration
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
    ]
    
    # Tavus Configuration
    TAVUS_API_KEY: Optional[str] = None
    TAVUS_PERSONA_ID: Optional[str] = None
    TAVUS_API_URL: str = "https://tavusapi.com"
    
    # LiveKit Configuration
    LIVEKIT_URL: Optional[str] = None
    LIVEKIT_API_KEY: Optional[str] = None
    LIVEKIT_API_SECRET: Optional[str] = None
    
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

