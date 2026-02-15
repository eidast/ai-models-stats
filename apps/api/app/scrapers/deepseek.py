"""
DeepSeek pricing scraper.
Source: https://api-docs.deepseek.com/quick_start/pricing
"""
from app.scrapers.base import BaseScraper


class DeepSeekScraper(BaseScraper):
    provider_id = "deepseek"
    provider_name = "DeepSeek"
    pricing_url = "https://api-docs.deepseek.com/quick_start/pricing"

    async def scrape(self):
        """DeepSeek has simple pricing - deepseek-chat and deepseek-reasoner."""
        provider = self._provider()
        now = "2025-02-14T00:00:00Z"  # TODO: use datetime
        models = [
            {
                "id": "deepseek-deepseek-chat",
                "providerId": self.provider_id,
                "name": "DeepSeek Chat (V3.2)",
                "apiId": "deepseek-chat",
                "type": "text",
                "modalities": ["text"],
                "capabilities": ["coding", "document_summaries", "rag"],
                "contextLength": 128000,
                "maxOutputTokens": 8192,
                "deprecated": False,
                "pricing": {
                    "inputPerMillionTokens": 0.28,
                    "outputPerMillionTokens": 0.42,
                    "cacheInputPerMillionTokens": 0.028,
                },
                "sourceUrl": self.pricing_url,
                "lastUpdated": now,
            },
            {
                "id": "deepseek-deepseek-reasoner",
                "providerId": self.provider_id,
                "name": "DeepSeek Reasoner (V3.2)",
                "apiId": "deepseek-reasoner",
                "type": "text",
                "modalities": ["text"],
                "capabilities": ["coding", "document_summaries", "rag"],
                "contextLength": 128000,
                "maxOutputTokens": 64000,
                "deprecated": False,
                "pricing": {
                    "inputPerMillionTokens": 0.28,
                    "outputPerMillionTokens": 0.42,
                    "cacheInputPerMillionTokens": 0.028,
                },
                "sourceUrl": self.pricing_url,
                "lastUpdated": now,
            },
        ]
        return provider, models
