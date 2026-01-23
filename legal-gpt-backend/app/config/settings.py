from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # App Info
    app_name: str = "Legal GPT Backend"
    debug: bool = True
    
    # Database
    database_url: str = "sqlite:///./legal_gpt.db"
    
    # JWT Authentication
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # AI Services
    openai_api_key: str
    openai_model: str = "gpt-3.5-turbo"
    
    # Google OAuth
    google_client_id: str = "not-needed-for-basic-functionality"
    google_client_secret: str = "not-needed-for-basic-functionality"
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000"]
    
    # Security
    secret_key: str
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
