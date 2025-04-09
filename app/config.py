import logging
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).parent.parent
SERVICE_NAME = "LIBRARY_MANAGEMENT_API_"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
LOGGING_FORMAT = "%(asctime)s %(levelname)s %(message)s"


class SystemConfig(BaseSettings):
    log_level: str = logging.getLevelName(logging.INFO)

    model_config = SettingsConfigDict(
        env_prefix=SERVICE_NAME + "SYSTEM_",
        env_file=ROOT_DIR / Path(".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


class AuthConfig(BaseSettings):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    refresh_token_secret_key: str

    model_config = SettingsConfigDict(
        env_prefix=SERVICE_NAME + "AUTH_",
        env_file=ROOT_DIR / Path(".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


system_config = SystemConfig()
auth_config = AuthConfig()
