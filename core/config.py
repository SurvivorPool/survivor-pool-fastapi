import pathlib
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Extra
from typing import Optional, Any, Dict, List

# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra=Extra.ignore)
    SQLALCHEMY_DATABASE_URI: Optional[str]
    SECRET_KEY: str
    COGNITO_URL: str
    COGNITO_CLIENT_ID: str
    ADMIN_EMAILS: str


    def get_database_url(self):
        return self.SQLALCHEMY_DATABASE_URI


settings = Settings()
