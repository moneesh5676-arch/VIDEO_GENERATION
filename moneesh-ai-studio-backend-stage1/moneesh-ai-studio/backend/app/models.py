"""Database tables."""
import enum
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class ProjectType(str, enum.Enum):
    TEXT_TO_VIDEO = "text_to_video"
    IMAGE_TO_VIDEO = "image_to_video"


class ProjectStatus(str, enum.Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


def utcnow() -> datetime:
    """Current UTC time (stored without tzinfo because SQLite has no timezone type)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Project(Base):
    """One generation request = one project row."""

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_type: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(20), default=ProjectStatus.QUEUED.value, index=True)

    prompt: Mapped[str] = mapped_column(Text, default="")
    duration: Mapped[int] = mapped_column(Integer)
    aspect_ratio: Mapped[str] = mapped_column(String(10))
    resolution: Mapped[str] = mapped_column(String(10))

    provider: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Only file NAMES are stored; the folders come from config.py.
    image_file: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    video_file: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    thumbnail_file: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, onupdate=utcnow)
