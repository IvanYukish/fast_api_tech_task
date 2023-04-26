import logging
import os
from pathlib import Path
from typing import Optional, Any

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import (
    BaseSettings, MongoDsn, validator,
)


class Settings(BaseSettings):
    BASE_DIR = Path(__file__).resolve().parent
    API_V1_STR: str = "/api/v1"
    SECRET_KEY = os.environ.get("SECRET_KEY") or ''
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES") or 60 * 24

    LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL", "INFO"))
    JSON_LOGS = True if os.environ.get("JSON_LOGS", "0") == "1" else False

    MONGO_USER: str = os.environ.get("MONGO_USER")
    MONGO_PASSWORD: str = os.environ.get("MONGO_PASSWORD")
    MONGO_HOST: str = os.environ.get("MONGO_HOST")
    MONGO_PORT: str = os.environ.get("MONGO_PORT")
    MONGO_DB: str = os.environ.get("MONGO_DB")
    DATABASE_URI: Optional[MongoDsn] = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        build = MongoDsn.build(
            scheme="mongodb",
            user=values.get("MONGO_USER"),
            password=values.get("MONGO_PASSWORD"),
            host=values.get("MONGO_HOST"),
            port=values.get("MONGO_PORT"),
            path=f"/{values.get('MONGO_DB')}",
        )
        return build

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/token")

    class Config:
        env_file = ".env"


settings = Settings()
