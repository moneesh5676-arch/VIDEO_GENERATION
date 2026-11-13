"""
MONEESH AI STUDIO - FastAPI backend entry point.

Run:  uvicorn app.main:app --reload --port 8000
Docs: http://localhost:8000/docs
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from . import models  # noqa: F401  (importing registers the tables)
from .config import get_settings
from .database import Base, engine
from .routes import generate, health, projects
from .services.generation import recover_interrupted_projects
from .services.video import ffmpeg_available

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(name)s: %(message)s")
logger = logging.getLogger("moneesh")

settings = get_settings()
settings.ensure_dirs()  # folders must exist before we mount them below


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)  # creates moneesh.db and tables on first run
    fixed = recover_interrupted_projects()
    if fixed:
        logger.warning("Marked %s interrupted project(s) as failed.", fixed)
    if not ffmpeg_available():
        logger.warning("FFmpeg was NOT found. Install it and add it to PATH (see README).")
    if settings.video_provider == "none":
        logger.warning("VIDEO_PROVIDER=none: generation requests will fail until a provider is configured.")
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend for MONEESH AI STUDIO: AI video generation through a configurable cloud provider.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(generate.router)
app.include_router(projects.router)

# Finished videos and thumbnails are served as static files. Uploaded images stay private.
app.mount("/media/videos", StaticFiles(directory=settings.videos_dir), name="videos")
app.mount("/media/thumbnails", StaticFiles(directory=settings.thumbnails_dir), name="thumbnails")


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")
