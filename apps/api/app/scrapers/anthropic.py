"""
Anthropic (Claude) pricing scraper.
Source: https://platform.claude.com/docs/en/about-claude/pricing
Note: Using static data from pricing docs. Add Playwright for live scraping.
"""
from datetime import datetime, timezone

from app.scrapers.base import BaseScraper

PRICING_URL = "https://platform.claude.com/docs/en/about-claude/pricing"
API_DOCS_URL = "https://docs.anthropic.com"


def _model(
    api_id: str,
    name: str,
    inp: float,
    out: float,
    context: int = 200000,
    cache: float | None = None,
    batch_inp: float | None = None,
    batch_out: float | None = None,
    deprecated: bool = False,
) -> dict:
    """Build model dict. Cache read = 0.1× base input."""
    pricing = {
        "inputPerMillionTokens": inp,
        "outputPerMillionTokens": out,
    }
    if cache is not None:
        pricing["cacheInputPerMillionTokens"] = cache
    if batch_inp is not None:
        pricing["batchInputPerMillionTokens"] = batch_inp
    if batch_out is not None:
        pricing["batchOutputPerMillionTokens"] = batch_out
    return {
        "id": f"anthropic-{api_id}",
        "providerId": "anthropic",
        "name": name,
        "apiId": api_id,
        "type": "text",
        "modalities": ["text"],
        "capabilities": ["coding", "document_summaries", "translation", "rag", "document_analysis"],
        "contextLength": context,
        "maxOutputTokens": 16384,
        "deprecated": deprecated,
        "pricing": pricing,
        "sourceUrl": PRICING_URL,
        "lastUpdated": datetime.now(timezone.utc).isoformat(),
    }


class AnthropicScraper(BaseScraper):
    provider_id = "anthropic"
    provider_name = "Anthropic"
    pricing_url = PRICING_URL

    async def scrape(self):
        """Anthropic Claude models — from platform.claude.com pricing (Feb 2026)."""
        provider = self._provider()
        provider["apiDocsUrl"] = API_DOCS_URL
        now = datetime.now(timezone.utc).isoformat()

        # (api_id, name, input, output, context, cache_read, batch_in, batch_out, deprecated)
        models_data = [
            ("claude-opus-4-6", "Claude Opus 4.6", 5.0, 25.0, 200000, 0.50, 2.50, 12.50, False),
            ("claude-opus-4-5", "Claude Opus 4.5", 5.0, 25.0, 200000, 0.50, 2.50, 12.50, False),
            ("claude-opus-4-1", "Claude Opus 4.1", 15.0, 75.0, 200000, 1.50, 7.50, 37.50, False),
            ("claude-opus-4", "Claude Opus 4", 15.0, 75.0, 200000, 1.50, 7.50, 37.50, False),
            ("claude-sonnet-4-5", "Claude Sonnet 4.5", 3.0, 15.0, 200000, 0.30, 1.50, 7.50, False),
            ("claude-sonnet-4", "Claude Sonnet 4", 3.0, 15.0, 200000, 0.30, 1.50, 7.50, False),
            ("claude-sonnet-3-7", "Claude Sonnet 3.7", 3.0, 15.0, 200000, 0.30, 1.50, 7.50, True),
            ("claude-haiku-4-5", "Claude Haiku 4.5", 1.0, 5.0, 200000, 0.10, 0.50, 2.50, False),
            ("claude-haiku-3-5", "Claude Haiku 3.5", 0.80, 4.0, 200000, 0.08, 0.40, 2.0, False),
            ("claude-opus-3", "Claude Opus 3", 15.0, 75.0, 200000, 1.50, 7.50, 37.50, True),
            ("claude-haiku-3", "Claude Haiku 3", 0.25, 1.25, 200000, 0.03, 0.125, 0.625, False),
        ]

        models = []
        for row in models_data:
            models.append(_model(
                api_id=row[0],
                name=row[1],
                inp=row[2],
                out=row[3],
                context=row[4],
                cache=row[5],
                batch_inp=row[6],
                batch_out=row[7],
                deprecated=row[8],
            ))

        for m in models:
            m["lastUpdated"] = now

        return provider, models
