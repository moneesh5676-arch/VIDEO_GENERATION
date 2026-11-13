"""
Runs one generation job in the background.

Flow: queued -> processing -> (provider makes video) -> FFmpeg format + thumbnail -> completed
Any problem ends as status "failed" with a readable error_message.
"""
import logging
import uuid
from pathlib import Path
from typing import Optional

from sqlalchemy import select

from ..config import get_settings
from ..database import SessionLocal
from ..models import Project, ProjectStatus
from ..providers import get_provider
from ..providers.base import GenerationRequest, ProviderError, ProviderNotConfigured
from . import video as video_tools

logger = logging.getLogger(__name__)


def _load(db, project_id: int) -> Optional[Project]:
    return db.execute(select(Project).where(Project.id == project_id)).scalar_one_or_none()


def _fail(db, project_id: int, message: str) -> None:
    db.rollback()
    project = _load(db, project_id)
    if project is None:  # user deleted it meanwhile
        return
    project.status = ProjectStatus.FAILED.value
    project.error_message = message[:500]
    db.commit()


def run_generation(project_id: int) -> None:
    settings = get_settings()
    db = SessionLocal()
    raw_path: Optional[Path] = None
    try:
        project = _load(db, project_id)
        if project is None:
            return

        project.status = ProjectStatus.PROCESSING.value
        project.error_message = None
        db.commit()

        provider = get_provider(settings)
        if not provider.is_configured():
            if provider.name == "none":
                raise ProviderNotConfigured(
                    "No AI video provider is configured. Set VIDEO_PROVIDER=fal and "
                    "VIDEO_PROVIDER_API_KEY in backend/.env, then restart the server."
                )
            raise ProviderNotConfigured(
                f"Provider '{provider.name}' is selected but VIDEO_PROVIDER_API_KEY is missing from backend/.env."
            )

        image_path = settings.uploads_dir / project.image_file if project.image_file else None
        if image_path is not None and not provider.supports_image_to_video:
            raise ProviderError(f"Provider '{provider.name}' does not support image-to-video.")
        if image_path is None and not provider.supports_text_to_video:
            raise ProviderError(f"Provider '{provider.name}' does not support text-to-video.")

        request = GenerationRequest(
            prompt=project.prompt,
            duration=project.duration,
            aspect_ratio=project.aspect_ratio,
            resolution=project.resolution,
            image_path=image_path,
        )

        settings.ensure_dirs()
        raw_path = settings.videos_dir / f"raw_{project_id}_{uuid.uuid4().hex[:8]}.mp4"
        provider.generate(request, raw_path)  # <- the real AI work happens in the provider

        if not raw_path.exists() or raw_path.stat().st_size == 0:
            raise ProviderError("The provider finished but did not return a video file.")

        project = _load(db, project_id)
        if project is None:  # deleted while generating: throw the result away
            return

        final_name = f"{project_id}_{uuid.uuid4().hex[:8]}.mp4"
        final_path = settings.videos_dir / final_name

        if video_tools.ffmpeg_available():
            video_tools.normalize_video(raw_path, final_path, project.aspect_ratio, project.resolution)
            raw_path.unlink(missing_ok=True)
            raw_path = None
            try:
                thumb_name = f"{project_id}_{uuid.uuid4().hex[:8]}.jpg"
                video_tools.make_thumbnail(final_path, settings.thumbnails_dir / thumb_name)
                project.thumbnail_file = thumb_name
            except video_tools.VideoProcessingError:
                logger.warning("Thumbnail failed for project %s", project_id)
        else:
            logger.warning("FFmpeg not found: saving the provider's video as it is (no resize, no thumbnail).")
            raw_path.rename(final_path)
            raw_path = None

        project.video_file = final_name
        project.status = ProjectStatus.COMPLETED.value
        db.commit()

    except ProviderError as e:
        _fail(db, project_id, str(e))
    except video_tools.VideoProcessingError as e:
        _fail(db, project_id, f"Video processing failed: {e}")
    except Exception:
        logger.exception("Unexpected error in generation job %s", project_id)
        _fail(db, project_id, "Unexpected error while generating the video. Check the server logs.")
    finally:
        if raw_path is not None:
            try:
                raw_path.unlink(missing_ok=True)
            except OSError:
                pass
        db.close()


def recover_interrupted_projects() -> int:
    """If the server stopped mid-generation, those projects can never finish. Mark them failed."""
    db = SessionLocal()
    try:
        stuck = db.execute(
            select(Project).where(
                Project.status.in_([ProjectStatus.QUEUED.value, ProjectStatus.PROCESSING.value])
            )
        ).scalars().all()
        for p in stuck:
            p.status = ProjectStatus.FAILED.value
            p.error_message = "The server restarted before this video finished. Please generate it again."
        db.commit()
        return len(stuck)
    finally:
        db.close()
