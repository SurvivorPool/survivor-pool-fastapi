import pathlib
import os
from pydantic import BaseSettings
from typing import Optional

# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: Optional[str]
    GOOGLE_APPLICATION_CREDENTIALS: str
    SECRET_KEY = "super-secret-secret-key"
    ALGORITHM = "HS256"
    class Config:
        case_sensitive = True
        env_file = ".env"
        fields = {
            "SQLALCHEMY_DATABASE_URI": {
                "env": "DATABASE_URL"
            }
        }

    def get_database_url(self):
        database_uri = self.SQLALCHEMY_DATABASE_URI
        if database_uri and database_uri.startswith("postgres://"):
            database_uri = database_uri.replace("postgres://", "postgresql://", 1)
            settings.SQLALCHEMY_DATABASE_URI = database_uri
        return self.SQLALCHEMY_DATABASE_URI
    


settings = Settings()
