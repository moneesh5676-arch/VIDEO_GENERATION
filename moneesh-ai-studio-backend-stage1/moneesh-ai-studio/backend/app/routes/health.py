from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..config import get_settings
from ..database import get_db
from ..providers import available_provider_classes, get_provider
from ..providers.base import ProviderNotConfigured
from ..schemas import HealthOut, ProviderInfo, ProvidersOut
from ..services.video import ffmpeg_available

router = APIRouter(prefix="/api", tags=["Health"])


@router.get("/health", response_model=HealthOut, summary="Check that the backend is running")
def health(db: Session = Depends(get_db)):
    settings = get_settings()

    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False

    try:
        configured = get_provider(settings).is_configured()
    except ProviderNotConfigured:
        configured = False

    return HealthOut(
        status="ok" if db_ok else "degraded",
        app=settings.app_name,
        version=settings.app_version,
        database=db_ok,
        ffmpeg=ffmpeg_available(),
        provider=settings.video_provider,
        provider_configured=configured,
    )


@router.get("/providers", response_model=ProvidersOut, summary="List AI providers and which one is active")
def providers():
    settings = get_settings()
    active = (settings.video_provider or "none").strip().lower()

    items = []
    for cls in available_provider_classes():
        is_active = cls.name == active
        configured = None
        if is_active:
            configured = cls(settings).is_configured()
        items.append(
            ProviderInfo(
                name=cls.name,
                display_name=cls.display_name,
                requires_api_key=cls.requires_api_key,
                active=is_active,
                configured=configured,
            )
        )
    return ProvidersOut(active=active, providers=items)
