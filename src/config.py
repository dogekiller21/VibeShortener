import os
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Database
    database_url: str = "postgresql://postgres:15643@localhost:5432/shortener"

    # Application
    app_name: str = "Vibe Shortener"
    debug: bool = False
    environment: str = "development"

    # URL Generation
    short_code_length: int = 8
    domain: str = "localhost:8000"

    model_config = ConfigDict(
        env_file="infrastructure/env/backend.env" if os.path.exists("infrastructure/env/backend.env") else None,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()
