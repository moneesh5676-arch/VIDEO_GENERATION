from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from ..config import get_settings
from ..database import get_db
from ..models import Project, ProjectStatus, ProjectType
from ..providers import get_provider
from ..providers.base import ProviderError, ProviderNotConfigured
from ..schemas import (
    MAX_DURATION_SECONDS,
    AspectRatio,
    ProjectOut,
    Resolution,
    TextToImageOut,
    TextToImageRequest,
    TextToVideoRequest,
)
from ..services.generation import run_generation
from ..services.storage import save_reference_image

router = APIRouter(prefix="/api/generate", tags=["Generate"])


def _create_project(db: Session, **fields) -> Project:
    project = Project(
        status=ProjectStatus.QUEUED.value,
        provider=get_settings().video_provider,
        **fields,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.post(
    "/text-to-video",
    response_model=ProjectOut,
    status_code=202,
    summary="Start a text-to-video generation (needs an AI provider API key)",
)
def text_to_video(
    payload: TextToVideoRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    project = _create_project(
        db,
        project_type=ProjectType.TEXT_TO_VIDEO.value,
        prompt=payload.prompt,
        duration=payload.duration,
        aspect_ratio=payload.aspect_ratio,
        resolution=payload.resolution,
    )
    background_tasks.add_task(run_generation, project.id)  # runs after this response is sent
    return ProjectOut.from_project(project)


@router.post(
    "/text-to-image",
    response_model=TextToImageOut,
    summary="Generate an image from a text prompt (requires fal.ai)",
)
def text_to_image(payload: TextToImageRequest):
    try:
        provider = get_provider(get_settings())
        if not provider.is_configured():
            raise ProviderNotConfigured("Configure VIDEO_PROVIDER=fal and VIDEO_PROVIDER_API_KEY in backend/.env.")
        if not provider.supports_text_to_image:
            raise ProviderNotConfigured(f"Provider '{provider.name}' does not support text-to-image.")
        return TextToImageOut(image_url=provider.generate_image(payload.prompt))
    except ProviderNotConfigured as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ProviderError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post(
    "/image-to-video",
    response_model=ProjectOut,
    status_code=202,
    summary="Start an image-to-video generation (needs an AI provider API key)",
)
def image_to_video(
    background_tasks: BackgroundTasks,
    image: UploadFile = File(..., description="PNG, JPG or WEBP reference image."),
    prompt: str = Form("", max_length=500, description="Animation instructions (optional)."),
    duration: int = Form(5, ge=1, le=MAX_DURATION_SECONDS),
    aspect_ratio: AspectRatio = Form("16:9"),
    resolution: Resolution = Form("720p"),
    db: Session = Depends(get_db),
):
    image_file = save_reference_image(image)  # validates type, size and content
    project = _create_project(
        db,
        project_type=ProjectType.IMAGE_TO_VIDEO.value,
        prompt=prompt.strip(),
        duration=duration,
        aspect_ratio=aspect_ratio,
        resolution=resolution,
        image_file=image_file,
    )
    background_tasks.add_task(run_generation, project.id)
    return ProjectOut.from_project(project)
