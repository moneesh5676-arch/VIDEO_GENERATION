from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..config import get_settings
from ..database import get_db
from ..models import Project, ProjectStatus
from ..schemas import ProjectOut, StatusOut
from ..services.storage import delete_project_files

router = APIRouter(prefix="/api/projects", tags=["Projects"])


def _get_or_404(db: Session, project_id: int) -> Project:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found.")
    return project


@router.get("", response_model=List[ProjectOut], summary="Project history (newest first)")
def list_projects(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    rows = db.execute(
        select(Project).order_by(Project.created_at.desc(), Project.id.desc()).limit(limit).offset(offset)
    ).scalars().all()
    return [ProjectOut.from_project(p) for p in rows]


@router.get("/{project_id}", response_model=ProjectOut, summary="Get one project")
def get_project(project_id: int, db: Session = Depends(get_db)):
    return ProjectOut.from_project(_get_or_404(db, project_id))


@router.get("/{project_id}/status", response_model=StatusOut, summary="Video generation status")
def get_status(project_id: int, db: Session = Depends(get_db)):
    p = _get_or_404(db, project_id)
    return StatusOut(
        id=p.id,
        status=p.status,
        error_message=p.error_message,
        video_ready=p.status == ProjectStatus.COMPLETED.value and bool(p.video_file),
    )


@router.get("/{project_id}/download", summary="Download the finished video (MP4)")
def download_video(project_id: int, db: Session = Depends(get_db)):
    p = _get_or_404(db, project_id)
    if p.status != ProjectStatus.COMPLETED.value or not p.video_file:
        raise HTTPException(status_code=409, detail=f"Video is not ready yet (status: {p.status}).")

    path = get_settings().videos_dir / p.video_file
    if not path.is_file():
        raise HTTPException(status_code=404, detail="The video file is missing on the server.")

    return FileResponse(path, media_type="video/mp4", filename=f"moneesh-video-{p.id}.mp4")


@router.delete("/{project_id}", status_code=204, summary="Delete a project and its files")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    p = _get_or_404(db, project_id)
    delete_project_files(p)
    db.delete(p)
    db.commit()
    return Response(status_code=204)
