"""Default provider: does nothing, and says so honestly. No fake videos are ever produced."""
from pathlib import Path

from .base import BaseVideoProvider, GenerationRequest, ProviderNotConfigured


class NoProvider(BaseVideoProvider):
    name = "none"
    display_name = "No provider (not configured)"
    requires_api_key = False
    supports_text_to_video = False
    supports_image_to_video = False

    def is_configured(self) -> bool:
        return False

    def generate(self, request: GenerationRequest, output_path: Path) -> None:
        raise ProviderNotConfigured(
            "No AI video provider is configured. Set VIDEO_PROVIDER and VIDEO_PROVIDER_API_KEY "
            "in backend/.env, then restart the server."
        )
