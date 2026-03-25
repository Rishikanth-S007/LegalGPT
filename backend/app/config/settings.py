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
    jwt_secret: str = "505df0dba1c285384ea8c65b9706b2eec5b80a34f462c909140f6d86abf852aa"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # AI Services
    openai_api_key: str = "sk-default-key-for-development"
    openai_model: str = "gpt-3.5-turbo"
    
    # Google OAuth
    google_client_id: str = "457325539713-as07rmv14vodsovqnht0qn4b1f4k9oiu.apps.googleusercontent.com"
    google_client_secret: str = "not-needed-for-basic-functionality"
    
    # CORS
    cors_origins: List[str] = [
        "http://localhost:3000", 
        "https://localhost:3000",
        "https://legalgpt-backend.onrender.com",
        "https://*.onrender.com",
        "https://legal-gpt.vercel.app",
        "https://*.vercel.app",
    ]
    
    # Security
    secret_key: str = "505df0dba1c285384ea8c65b9706b2eec5b80a34f462c909140f6d86abf852aa"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
