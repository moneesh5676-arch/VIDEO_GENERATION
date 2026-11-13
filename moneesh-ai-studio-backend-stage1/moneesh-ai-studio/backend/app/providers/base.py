"""
The provider interface.

A "provider" is the thing that really creates the video: a cloud API (Replicate, fal.ai, ...)
or your own remote GPU server. Heavy AI work NEVER runs on your laptop.

To add a new provider, make a class that inherits BaseVideoProvider, implement generate(),
and register it in providers/__init__.py. The rest of the app does not change.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from ..config import Settings


@dataclass
class GenerationRequest:
    prompt: str
    duration: int
    aspect_ratio: str
    resolution: str
    image_path: Optional[Path] = None  # set for image-to-video


class ProviderError(Exception):
    """The provider failed. The message is shown to the user, so keep it clear and secret-free."""


class ProviderNotConfigured(ProviderError):
    """No provider selected, or its API key is missing."""


class BaseVideoProvider(ABC):
    name: str = "base"
    display_name: str = "Base provider"
    requires_api_key: bool = True
    supports_text_to_video: bool = True
    supports_image_to_video: bool = True

    def __init__(self, settings: Settings):
        self.settings = settings

    def is_configured(self) -> bool:
        """True when everything needed (usually the API key) is present."""
        return bool(self.settings.video_provider_api_key)

    @abstractmethod
    def generate(self, request: GenerationRequest, output_path: Path) -> None:
        """
        Create the video and save it to output_path as an MP4 file.

        This function may block (submit job, wait, download). It runs in a background thread,
        not inside the web request. Raise ProviderError if anything fails.
        """
