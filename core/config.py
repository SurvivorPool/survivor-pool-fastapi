import pathlib
from pydantic import AnyHttpUrl, BaseSettings, validator, Field
from typing import List, Optional, Union

# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    # BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    #
    # @validator("BACKEND_CORS_ORIGINS", pre=True)
    # def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
    #     if isinstance(v, str) and not v.startswith("["):
    #         return [i.strip() for i in v.split(",")]
    #     elif isinstance(v, (list, str)):
    #         return v
    #     raise ValueError(v)

    SQLALCHEMY_DATABASE_URI: Optional[str]
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


settings = Settings()