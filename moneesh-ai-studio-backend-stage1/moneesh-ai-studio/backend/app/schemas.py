"""Pydantic schemas: what the API accepts and returns (with validation)."""
from datetime import datetime, timezone
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .models import Project, ProjectStatus

AspectRatio = Literal["9:16", "16:9", "1:1"]
Resolution = Literal["480p", "720p", "1080p"]

MAX_DURATION_SECONDS = 10


class TextToVideoRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    prompt: str = Field(min_length=3, max_length=1000, description="Describe the video scene.")
    duration: int = Field(default=5, ge=1, le=MAX_DURATION_SECONDS, description="Length in seconds.")
    aspect_ratio: AspectRatio = "16:9"
    resolution: Resolution = "720p"


class ProjectOut(BaseModel):
    """Project as the frontend sees it."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    project_type: str
    status: str
    prompt: str
    duration: int
    aspect_ratio: str
    resolution: str
    provider: Optional[str] = None
    error_message: Optional[str] = None

    # Relative URLs. The frontend adds the backend address in front.
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    download_url: Optional[str] = None

    created_at: datetime
    updated_at: datetime

    @field_validator("created_at", "updated_at")
    @classmethod
    def _mark_as_utc(cls, value: datetime) -> datetime:
        # SQLite returns naive datetimes. Mark them UTC so the browser converts to local time correctly.
        return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value

    @classmethod
    def from_project(cls, p: Project) -> "ProjectOut":
        ready = p.status == ProjectStatus.COMPLETED.value and bool(p.video_file)
        return cls(
            id=p.id,
            project_type=p.project_type,
            status=p.status,
            prompt=p.prompt or "",
            duration=p.duration,
            aspect_ratio=p.aspect_ratio,
            resolution=p.resolution,
            provider=p.provider,
            error_message=p.error_message,
            video_url=f"/media/videos/{p.video_file}" if ready else None,
            thumbnail_url=f"/media/thumbnails/{p.thumbnail_file}" if p.thumbnail_file else None,
            download_url=f"/api/projects/{p.id}/download" if ready else None,
            created_at=p.created_at,
            updated_at=p.updated_at,
        )


class StatusOut(BaseModel):
    id: int
    status: str
    error_message: Optional[str] = None
    video_ready: bool


class HealthOut(BaseModel):
    status: str
    app: str
    version: str
    database: bool
    ffmpeg: bool
    provider: str
    provider_configured: bool


class ProviderInfo(BaseModel):
    name: str
    display_name: str
    requires_api_key: bool
    active: bool
    configured: Optional[bool] = None  # only known for the active provider


class ProvidersOut(BaseModel):
    active: str
    providers: List[ProviderInfo]
