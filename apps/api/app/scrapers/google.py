"""
Google Gemini pricing scraper.
Source: https://ai.google.dev/gemini-api/docs/pricing
Note: Page is JS-rendered; using static data. Add Playwright for full scraping.
"""
from datetime import datetime, timezone

from app.scrapers.base import BaseScraper


class GoogleScraper(BaseScraper):
    provider_id = "google"
    provider_name = "Google"
    pricing_url = "https://ai.google.dev/gemini-api/docs/pricing"

    async def scrape(self):
        """Google Gemini models - from pricing docs."""
        provider = self._provider()
        now = datetime.now(timezone.utc).isoformat()
        models = [
            {
                "id": "google-gemini-2.5-flash",
                "providerId": self.provider_id,
                "name": "Gemini 2.5 Flash",
                "apiId": "gemini-2.5-flash",
                "type": "multimodal",
                "modalities": ["text", "image", "video", "audio"],
                "capabilities": ["coding", "document_summaries", "image_generation", "rag"],
                "contextLength": 1000000,
                "maxOutputTokens": 8192,
                "deprecated": False,
                "pricing": {
                    "inputPerMillionTokens": 0.30,
                    "outputPerMillionTokens": 2.50,
                    "cacheInputPerMillionTokens": 0.03,
                },
                "sourceUrl": self.pricing_url,
                "lastUpdated": now,
            },
            {
                "id": "google-gemini-2.5-flash-lite",
                "providerId": self.provider_id,
                "name": "Gemini 2.5 Flash-Lite",
                "apiId": "gemini-2.5-flash-lite",
                "type": "multimodal",
                "modalities": ["text", "image", "video", "audio"],
                "capabilities": ["coding", "document_summaries", "rag"],
                "contextLength": 1000000,
                "maxOutputTokens": 8192,
                "deprecated": False,
                "pricing": {
                    "inputPerMillionTokens": 0.10,
                    "outputPerMillionTokens": 0.40,
                    "cacheInputPerMillionTokens": 0.01,
                },
                "sourceUrl": self.pricing_url,
                "lastUpdated": now,
            },
            {
                "id": "google-gemini-2.5-pro",
                "providerId": self.provider_id,
                "name": "Gemini 2.5 Pro",
                "apiId": "gemini-2.5-pro",
                "type": "multimodal",
                "modalities": ["text", "image", "video", "audio"],
                "capabilities": ["coding", "document_summaries", "rag", "document_analysis"],
                "contextLength": 1000000,
                "maxOutputTokens": 8192,
                "deprecated": False,
                "pricing": {
                    "inputPerMillionTokens": 1.25,
                    "outputPerMillionTokens": 10.0,
                    "cacheInputPerMillionTokens": 0.125,
                },
                "sourceUrl": self.pricing_url,
                "lastUpdated": now,
            },
        ]
        return provider, models
