from pydantic_settings import BaseSettings
from typing import List, Union
import json


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/movie_catalog"
    
    # JWT
    JWT_SECRET_KEY: str = "your-super-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # API
    API_V1_PREFIX: str = "/api"
    PROJECT_NAME: str = "MovieCatalog.API"
    DEBUG: bool = True
    ROOT_PATH: str = ""
    
    # CORS
    BACKEND_CORS_ORIGINS: Union[List[str], str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name == 'BACKEND_CORS_ORIGINS':
                try:
                    # Try to parse as JSON
                    return json.loads(raw_val)
                except json.JSONDecodeError:
                    # If not valid JSON, treat as single value
                    return [raw_val]
            return raw_val
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure BACKEND_CORS_ORIGINS is always a list
        if isinstance(self.BACKEND_CORS_ORIGINS, str):
            try:
                self.BACKEND_CORS_ORIGINS = json.loads(self.BACKEND_CORS_ORIGINS)
            except json.JSONDecodeError:
                self.BACKEND_CORS_ORIGINS = [self.BACKEND_CORS_ORIGINS]


settings = Settings()

