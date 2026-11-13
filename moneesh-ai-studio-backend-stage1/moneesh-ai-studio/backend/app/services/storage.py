"""File handling: saving reference images and deleting project files."""
import io
import uuid
from typing import Optional

from fastapi import HTTPException, UploadFile
from PIL import Image

from ..config import get_settings
from ..models import Project

ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "image/webp"}
FORMAT_TO_EXT = {"PNG": ".png", "JPEG": ".jpg", "WEBP": ".webp"}


def save_reference_image(upload: UploadFile) -> str:
    """Validate an uploaded image and save it. Returns the saved file NAME."""
    settings = get_settings()

    if upload.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=415, detail="Only PNG, JPG or WEBP images are allowed.")

    max_bytes = settings.max_upload_mb * 1024 * 1024
    data = upload.file.read(max_bytes + 1)  # read one extra byte to detect "too big"
    if len(data) > max_bytes:
        raise HTTPException(status_code=413, detail=f"Image is larger than {settings.max_upload_mb} MB.")
    if not data:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")

    # Do not trust the browser: open the bytes with Pillow to prove it is really an image.
    try:
        with Image.open(io.BytesIO(data)) as img:
            img.verify()
            fmt = img.format
    except Exception:
        raise HTTPException(status_code=400, detail="The file is not a valid image.")

    ext = FORMAT_TO_EXT.get(fmt or "")
    if ext is None:
        raise HTTPException(status_code=415, detail="Only PNG, JPG or WEBP images are allowed.")

    settings.ensure_dirs()
    filename = f"{uuid.uuid4().hex}{ext}"  # our own name, so user input never touches the file path
    (settings.uploads_dir / filename).write_bytes(data)
    return filename


def delete_project_files(project: Project) -> None:
    """Remove every file that belongs to a project (ignores files that are already gone)."""
    settings = get_settings()
    targets = [
        (settings.uploads_dir, project.image_file),
        (settings.videos_dir, project.video_file),
        (settings.thumbnails_dir, project.thumbnail_file),
    ]
    for folder, name in targets:
        if name:
            try:
                (folder / name).unlink(missing_ok=True)
            except OSError:
                pass  # file in use or permission problem: do not block deleting the project


def remove_reference_image(filename: Optional[str]) -> None:
    if filename:
        try:
            (get_settings().uploads_dir / filename).unlink(missing_ok=True)
        except OSError:
            pass
