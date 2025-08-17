from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./banking.db"
    
    # JWT
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Application
    debug: bool = True
    api_v1_str: str = "/api/v1"
    project_name: str = "Banking REST API"
    
    # Security
    bcrypt_rounds: int = 12
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
