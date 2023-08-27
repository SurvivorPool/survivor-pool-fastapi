import pathlib
import os
from pydantic_settings import BaseSettings
from pydantic import Extra
from typing import Optional

# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: Optional[str]
    SECRET_KEY: str
    COGNITO_URL: str

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = Extra.ignore


    def get_database_url(self):
        return self.SQLALCHEMY_DATABASE_URI


settings = Settings()
