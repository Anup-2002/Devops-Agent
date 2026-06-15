from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "AutoOps AI"
    app_env: Literal["development", "staging", "production"] = "development"
    app_debug: bool = True
    api_v1_prefix: str = "/api/v1"

    host: str = "0.0.0.0"
    port: int = 8000

    database_url: str = Field(default="postgresql+asyncpg://postgres@localhost:5432/autoops")
    sync_database_url: str = Field(default="postgresql+psycopg://postgres@localhost:5432/autoops")
    redis_url: str = Field(default="redis://localhost:6379/0")

    jwt_secret_key: str = Field(min_length=16, default="change-this-secret")
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = Field(default=60, ge=1)

    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
