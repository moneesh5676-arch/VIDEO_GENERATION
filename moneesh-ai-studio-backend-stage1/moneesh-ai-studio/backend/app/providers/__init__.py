"""Provider registry: maps the VIDEO_PROVIDER setting to a provider class."""
from typing import Dict, List, Type

from ..config import Settings
from .base import BaseVideoProvider, ProviderNotConfigured
from .fal_provider import FalProvider
from .none_provider import NoProvider

# To add a provider later: import its class and add it here.
PROVIDERS: Dict[str, Type[BaseVideoProvider]] = {
    NoProvider.name: NoProvider,
    FalProvider.name: FalProvider,
}


def available_provider_classes() -> List[Type[BaseVideoProvider]]:
    return list(PROVIDERS.values())


def get_provider(settings: Settings) -> BaseVideoProvider:
    name = (settings.video_provider or "none").strip().lower()
    cls = PROVIDERS.get(name)
    if cls is None:
        raise ProviderNotConfigured(
            f"Unknown VIDEO_PROVIDER '{name}'. Available: {', '.join(PROVIDERS)}."
        )
    return cls(settings)
