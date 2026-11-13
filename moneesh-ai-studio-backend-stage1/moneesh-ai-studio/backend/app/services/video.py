"""FFmpeg helpers: resize/crop to the requested format, and make thumbnails."""
import logging
import shutil
import subprocess
from pathlib import Path
from typing import Tuple

logger = logging.getLogger(__name__)

SHORT_SIDE = {"480p": 480, "720p": 720, "1080p": 1080}


class VideoProcessingError(Exception):
    pass


def ffmpeg_path() -> str:
    return shutil.which("ffmpeg") or ""


def ffmpeg_available() -> bool:
    return bool(ffmpeg_path())


def output_size(aspect_ratio: str, resolution: str) -> Tuple[int, int]:
    """Width and height (always even numbers, as H.264 needs) for a format."""
    s = SHORT_SIDE[resolution]
    if aspect_ratio == "16:9":
        return round(s * 16 / 9 / 2) * 2, s
    if aspect_ratio == "9:16":
        return s, round(s * 16 / 9 / 2) * 2
    if aspect_ratio == "1:1":
        return s, s
    raise VideoProcessingError(f"Unsupported aspect ratio: {aspect_ratio}")


def _run(cmd: list) -> None:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        raise VideoProcessingError("FFmpeg took too long and was stopped.")
    if result.returncode != 0:
        tail = "\n".join(result.stderr.strip().splitlines()[-5:])
        logger.error("ffmpeg failed: %s", tail)
        raise VideoProcessingError("FFmpeg could not process the video.")


def normalize_video(src: Path, dst: Path, aspect_ratio: str, resolution: str) -> None:
    """Scale + center-crop the video to the exact aspect ratio and resolution, as web-friendly MP4."""
    w, h = output_size(aspect_ratio, resolution)
    vf = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1"
    _run([
        ffmpeg_path(), "-y", "-i", str(src),
        "-vf", vf,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-movflags", "+faststart",  # lets the browser start playing before the file fully downloads
        str(dst),
    ])


def make_thumbnail(video: Path, thumb: Path) -> None:
    """Save one frame of the video as a JPG."""
    last_error = None
    for start in ("0.5", "0"):  # very short clips may not have a frame at 0.5s
        try:
            _run([
                ffmpeg_path(), "-y", "-ss", start, "-i", str(video),
                "-frames:v", "1", "-vf", "scale=480:-2", str(thumb),
            ])
            if thumb.exists():
                return
        except VideoProcessingError as e:
            last_error = e
    raise last_error or VideoProcessingError("Could not create a thumbnail.")
