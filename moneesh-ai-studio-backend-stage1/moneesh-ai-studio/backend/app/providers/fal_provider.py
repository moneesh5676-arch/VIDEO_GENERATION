"""fal.ai-backed video and image generation."""
import shutil
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import urlopen

from fal_client import SyncClient
from fal_client.client import FalClientError, FalClientHTTPError, FalClientTimeoutError

from .base import BaseVideoProvider, GenerationRequest, ProviderError, ProviderNotConfigured

_VIDEO_TIMEOUT_SECONDS = 900


class FalProvider(BaseVideoProvider):
    name = "fal"
    display_name = "fal.ai"
    supports_text_to_image = True

    def is_configured(self) -> bool:
        return bool(self.settings.video_provider_api_key.strip())

    def _client(self) -> SyncClient:
        key = self.settings.video_provider_api_key.strip()
        if not key:
            raise ProviderNotConfigured(
                "fal.ai is selected but VIDEO_PROVIDER_API_KEY is missing from backend/.env."
            )
        return SyncClient(key=key)

    @staticmethod
    def _provider_error(exc: FalClientError) -> ProviderError:
        if isinstance(exc, FalClientHTTPError):
            if exc.status_code in (401, 403):
                return ProviderError("fal.ai rejected the API key or this model is not enabled for the account.")
            if exc.status_code == 402:
                return ProviderError("fal.ai requires an active payment method or available account credits.")
            if exc.status_code == 429:
                return ProviderError("fal.ai rate limit reached. Wait briefly, then try again.")
            return ProviderError(f"fal.ai returned HTTP {exc.status_code}. Check the model settings and account.")
        if isinstance(exc, FalClientTimeoutError):
            return ProviderError("fal.ai generation timed out. Check the fal.ai request history before retrying.")
        return ProviderError("fal.ai could not complete the request. Check the API key, model access, and backend logs.")

    def _run(self, model: str, arguments: dict[str, Any]) -> dict[str, Any]:
        try:
            result = self._client().subscribe(
                model,
                arguments=arguments,
                interval=2.0,
                client_timeout=_VIDEO_TIMEOUT_SECONDS,
            )
        except FalClientError as exc:
            raise self._provider_error(exc) from exc

        if not isinstance(result, dict):
            raise ProviderError("fal.ai returned an unexpected response.")
        return result

    @staticmethod
    def _download(url: str, output_path: Path) -> None:
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.hostname:
            raise ProviderError("fal.ai returned an invalid media URL.")

        partial_path = output_path.with_name(f"{output_path.name}.partial")
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with urlopen(url, timeout=120) as response, partial_path.open("wb") as target:
                shutil.copyfileobj(response, target)
            partial_path.replace(output_path)
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            partial_path.unlink(missing_ok=True)
            raise ProviderError("Could not download the generated media from fal.ai.") from exc

    def generate(self, request: GenerationRequest, output_path: Path) -> None:
        if request.image_path is None:
            arguments = {
                "prompt": request.prompt,
                "aspect_ratio": request.aspect_ratio if request.aspect_ratio in ("16:9", "9:16") else "16:9",
                "duration": str(request.duration),
                "generate_audio": False,
            }
            model = self.settings.video_provider_model
        else:
            try:
                image_url = self._client().upload_file(request.image_path)
            except FalClientError as exc:
                raise self._provider_error(exc) from exc
            arguments = {
                "start_image_url": image_url,
                "prompt": request.prompt or "Animate the image with natural, subtle motion.",
                "duration": str(request.duration),
            }
            model = self.settings.video_provider_image_model

        result = self._run(model, arguments)
        video = result.get("video")
        video_url = video.get("url") if isinstance(video, dict) else None
        if not isinstance(video_url, str):
            raise ProviderError("fal.ai completed the request without returning a video.")
        self._download(video_url, output_path)

    def generate_image(self, prompt: str) -> str:
        result = self._run(
            self.settings.video_provider_text_image_model,
            {"prompt": prompt},
        )
        images = result.get("images")
        if not isinstance(images, list) or not images or not isinstance(images[0], dict):
            raise ProviderError("fal.ai completed the request without returning an image.")
        image_url = images[0].get("url")
        if not isinstance(image_url, str) or urlparse(image_url).scheme != "https":
            raise ProviderError("fal.ai returned an invalid image URL.")
        return image_url
