"""
Base scraper interface.
Provider-specific scrapers inherit and implement scrape().
"""
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any


class BaseScraper(ABC):
    """Abstract base for provider scrapers."""

    provider_id: str
    provider_name: str
    pricing_url: str

    @abstractmethod
    async def scrape(self) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        """
        Scrape provider and models.
        Returns (provider_dict, list of model_dicts).
        """
        pass

    def _provider(self) -> dict[str, Any]:
        """Build provider record."""
        return {
            "id": self.provider_id,
            "name": self.provider_name,
            "pricingUrl": self.pricing_url,
            "lastUpdated": datetime.now(timezone.utc).isoformat(),
        }
