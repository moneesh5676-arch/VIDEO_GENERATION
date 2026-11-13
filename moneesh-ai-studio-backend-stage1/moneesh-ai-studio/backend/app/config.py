"""
Central configuration.

All settings come from environment variables or the ".env" file in the backend folder.
Nothing secret is written in the code.
"""
from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/ folder (parent of "app")
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "MONEESH AI STUDIO"
    app_version: str = "0.1.0"

    # SQLite file lives inside backend/ by default. as_posix() keeps Windows paths valid.
    database_url: str = f"sqlite:///{(BASE_DIR / 'moneesh.db').as_posix()}"

    # Where uploads, videos and thumbnails are stored.
    storage_dir: str = "storage"

    # Comma-separated list of frontend URLs allowed by CORS.
    cors_origins: str = (
        "http://localhost:5173,http://127.0.0.1:5173,"
        "http://localhost:5174,http://127.0.0.1:5174"
    )

    max_upload_mb: int = 10

    # AI provider settings (see app/providers/)
    video_provider: str = "none"
    video_provider_api_key: str = ""
    video_provider_model: str = ""

    # ---------- helpers ----------
    @property
    def cors_origin_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def storage_path(self) -> Path:
        p = Path(self.storage_dir)
        return p if p.is_absolute() else BASE_DIR / p

    @property
    def uploads_dir(self) -> Path:
        return self.storage_path / "uploads"

    @property
    def videos_dir(self) -> Path:
        return self.storage_path / "videos"

    @property
    def thumbnails_dir(self) -> Path:
        return self.storage_path / "thumbnails"

    def ensure_dirs(self) -> None:
        for d in (self.uploads_dir, self.videos_dir, self.thumbnails_dir):
            d.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    return Settings()
