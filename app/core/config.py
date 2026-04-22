from functools import lru_cache
from pathlib import Path
import tempfile

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_DATABASE_PATH = Path(tempfile.gettempdir()) / "vr-spatial-sound-exercises" / "app.db"


class Settings(BaseSettings):
    app_name: str = "VR Spatial Sound Exercises Backend"
    debug: bool = False
    api_prefix: str = "/api"
    database_url: str = Field(default=f"sqlite:///{DEFAULT_DATABASE_PATH.as_posix()}")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug_value(cls, value: object) -> object:
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"release", "prod", "production"}:
                return False
            if normalized in {"dev", "development"}:
                return True
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
