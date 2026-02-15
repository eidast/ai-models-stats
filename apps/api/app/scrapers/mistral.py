"""
Mistral AI pricing scraper.
Sources:
  - https://mistral.ai/pricing#api
  - https://docs.mistral.ai/deployment/ai-studio/pricing
  - pricepertoken.com (reference for full model list)
Note: Using static data from pricing docs (Feb 2026). Add Playwright for live scraping.
"""
from datetime import datetime, timezone

from app.scrapers.base import BaseScraper

PRICING_URL = "https://mistral.ai/pricing#api"
API_DOCS_URL = "https://docs.mistral.ai"


def _model(
    api_id: str,
    name: str,
    inp: float,
    out: float,
    context: int,
    model_type: str = "text",
    modalities: list[str] | None = None,
    capabilities: list[str] | None = None,
    cache: float | None = None,
    deprecated: bool = False,
) -> dict:
    """Build model dict."""
    return {
        "id": f"mistral-{api_id}",
        "providerId": "mistral",
        "name": name,
        "apiId": api_id,
        "type": model_type,
        "modalities": modalities or ["text"],
        "capabilities": capabilities or ["coding", "document_summaries", "translation", "rag"],
        "contextLength": context,
        "maxOutputTokens": 16384,
        "deprecated": deprecated,
        "pricing": {
            "inputPerMillionTokens": inp,
            "outputPerMillionTokens": out,
            **({"cacheInputPerMillionTokens": cache} if cache else {}),
        },
        "sourceUrl": PRICING_URL,
        "lastUpdated": datetime.now(timezone.utc).isoformat(),
    }


class MistralScraper(BaseScraper):
    provider_id = "mistral"
    provider_name = "Mistral AI"
    pricing_url = PRICING_URL

    async def scrape(self):
        """Mistral API models — full ecosystem (27 models)."""
        provider = self._provider()
        provider["apiDocsUrl"] = API_DOCS_URL
        now = datetime.now(timezone.utc).isoformat()

        # (api_id, name, input, output, context, type, modalities, capabilities, cache)
        models_data = [
            # Budget
            ("mistral-nemo", "Mistral Nemo", 0.02, 0.04, 131072, "text", None, None, None),
            ("mistral-small-3.1-24b-instruct", "Mistral Small 3.1 24B", 0.03, 0.11, 131072, "text", None, None, 0.015),
            ("devstral-2512", "Devstral 2", 0.05, 0.22, 262144, "text", None, ["coding", "document_summaries", "rag"], 0.025),
            ("mistral-small-24b-instruct-2501", "Mistral Small 3", 0.05, 0.08, 32768, "text", None, None, None),
            ("mistral-small-3.2-24b-instruct", "Mistral Small 3.2 24B", 0.06, 0.18, 131072, "text", None, None, 0.03),
            # Mid
            ("mistral-small-creative", "Mistral Small Creative", 0.10, 0.30, 32768, "text", None, ["story_generation"], None),
            ("ministral-3b-2512", "Ministral 3 3B", 0.10, 0.10, 131072, "text", None, None, None),
            ("voxtral-small-24b-2507", "Voxtral Small 24B", 0.10, 0.30, 32000, "audio", ["text", "audio"], ["audio_generation"], None),
            ("devstral-small", "Devstral Small 1.1", 0.10, 0.30, 131072, "text", None, ["coding", "document_summaries"], None),
            ("mistral-7b-instruct-v0.1", "Mistral 7B Instruct v0.1", 0.11, 0.19, 2824, "text", None, None, None),
            ("ministral-8b-2512", "Ministral 3 8B", 0.15, 0.15, 262144, "text", None, None, None),
            ("ministral-14b-2512", "Ministral 3 14B", 0.20, 0.20, 262144, "text", None, None, None),
            ("mistral-saba", "Saba", 0.20, 0.60, 32768, "text", None, None, None),
            ("mistral-7b-instruct", "Mistral 7B Instruct", 0.20, 0.20, 32768, "text", None, None, None),
            ("mistral-7b-instruct-v0.3", "Mistral 7B Instruct v0.3", 0.20, 0.20, 32768, "text", None, None, None),
            ("mistral-7b-instruct-v0.2", "Mistral 7B Instruct v0.2", 0.20, 0.20, 32768, "text", None, None, None),
            ("codestral-2508", "Codestral 2508", 0.30, 0.90, 256000, "text", None, ["coding"], None),
            # Premium
            ("mistral-medium-3.1", "Mistral Medium 3.1", 0.40, 2.00, 131072, "text", None, None, None),
            ("devstral-medium", "Devstral Medium", 0.40, 2.00, 131072, "text", None, ["coding", "document_summaries"], None),
            ("mistral-medium-3", "Mistral Medium 3", 0.40, 2.00, 131072, "text", None, None, None),
            ("mistral-large-2512", "Mistral Large 3", 0.50, 1.50, 262144, "text", None, None, None),
            ("mixtral-8x7b-instruct", "Mixtral 8x7B Instruct", 0.54, 0.54, 32768, "text", None, None, None),
            ("mistral-large-2411", "Mistral Large 24-11", 2.00, 6.00, 131072, "text", None, None, None),
            ("mistral-large-2407", "Mistral Large 24-07", 2.00, 6.00, 131072, "text", None, None, None),
            ("pixtral-large-2411", "Pixtral Large", 2.00, 6.00, 131072, "multimodal", ["text", "image"], ["image_generation", "document_analysis", "rag"], None),
            ("mixtral-8x22b-instruct", "Mixtral 8x22B Instruct", 2.00, 6.00, 65536, "text", None, None, None),
            ("mistral-large", "Mistral Large", 2.00, 6.00, 128000, "text", None, None, None),
        ]

        models = []
        for row in models_data:
            api_id, name, inp, out, ctx = row[0], row[1], row[2], row[3], row[4]
            model_type = row[5] if len(row) > 5 else "text"
            modalities = row[6] if len(row) > 6 else ["text"]
            capabilities = row[7] if len(row) > 7 else ["coding", "document_summaries", "translation", "rag"]
            cache = row[8] if len(row) > 8 else None
            models.append(_model(api_id, name, inp, out, ctx, model_type, modalities, capabilities, cache))

        for m in models:
            m["lastUpdated"] = now

        return provider, models
