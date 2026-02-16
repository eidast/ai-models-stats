"""
xAI (Grok) pricing scraper.
Source: https://docs.x.ai/developers/models
Note: Using static data from pricing docs (Feb 2026). Add Playwright for live scraping.
"""
from datetime import datetime, timezone

from app.scrapers.base import BaseScraper

PRICING_URL = "https://docs.x.ai/developers/models"
API_DOCS_URL = "https://docs.x.ai"


def _model(
    api_id: str,
    name: str,
    model_type: str,
    modalities: list[str],
    pricing: dict,
    context: int | None = 128000,
    capabilities: list[str] | None = None,
    **kw,
) -> dict:
    """Build model dict."""
    return {
        "id": f"xai-{api_id}",
        "providerId": "xai",
        "name": name,
        "apiId": api_id,
        "type": model_type,
        "modalities": modalities,
        "capabilities": capabilities or ["coding", "document_summaries", "translation"],
        "contextLength": context,
        "maxOutputTokens": kw.get("maxOutputTokens", 8192),
        "deprecated": kw.get("deprecated", False),
        "pricing": pricing,
        "sourceUrl": PRICING_URL,
        "lastUpdated": datetime.now(timezone.utc).isoformat(),
        **{k: v for k, v in kw.items() if k not in ("maxOutputTokens", "deprecated")},
    }


class XAIScraper(BaseScraper):
    provider_id = "xai"
    provider_name = "xAI (Grok)"
    pricing_url = PRICING_URL

    async def scrape(self):
        """xAI Grok models — text, multimodal, image, video (Feb 2026)."""
        provider = self._provider()
        provider["apiDocsUrl"] = API_DOCS_URL
        now = datetime.now(timezone.utc).isoformat()

        models = []

        # --- Text / Multimodal (Grok) — per 1M tokens: input / output / cache ---
        grok_text = [
            ("grok-4-1-fast-reasoning", "Grok 4.1 Fast Reasoning", 0.20, 0.50, 0.05, 2_000_000, True),
            ("grok-4-1-fast-non-reasoning", "Grok 4.1 Fast Non-Reasoning", 0.20, 0.50, 0.05, 2_000_000, False),
            ("grok-4-fast-reasoning", "Grok 4 Fast Reasoning", 0.20, 0.50, 0.05, 2_000_000, True),
            ("grok-4-fast-non-reasoning", "Grok 4 Fast Non-Reasoning", 0.20, 0.50, 0.05, 2_000_000, False),
            ("grok-code-fast-1", "Grok Code Fast 1", 0.20, 1.50, 0.02, 256_000, True),
            ("grok-4-0709", "Grok 4 0709", 3.00, 15.00, 0.75, 256_000, True),
            ("grok-3", "Grok 3", 3.00, 15.00, 0.75, 131_072, False),
            ("grok-3-mini", "Grok 3 Mini", 0.30, 0.50, 0.07, 131_072, True),
            ("grok-2-vision-1212", "Grok 2 Vision 1212", 2.00, 10.00, 0.00, 32_768, False),
        ]
        for api_id, name, inp, out, cache, ctx, reasoning in grok_text:
            caps = ["coding", "document_summaries", "translation", "reasoning"] if reasoning else ["coding", "document_summaries", "translation"]
            if "vision" in api_id or "fast" in api_id:
                caps.append("image_understanding")
            p = {
                "inputPerMillionTokens": inp,
                "outputPerMillionTokens": out,
                "cacheInputPerMillionTokens": cache,
            }
            mods = ["text", "image"] if "vision" in api_id or "fast" in api_id else ["text"]
            models.append(_model(api_id, name, "multimodal" if "image" in str(mods) else "text", mods, p, context=ctx, capabilities=caps))

        # --- Image Generation ---
        imagen = [
            ("grok-2-image-1212", "Grok 2 Image 1212", 0.07),
            ("grok-imagine-image", "Grok Imagine Image", 0.02),
            ("grok-imagine-image-pro", "Grok Imagine Image Pro", 0.07),
        ]
        for api_id, name, price in imagen:
            models.append(_model(
                api_id, name, "image", ["image"],
                {"imageOutputPerImage": price},
                context=None,
                capabilities=["image_generation"],
                maxOutputTokens=None,
            ))

        # --- Video ---
        models.append(_model(
            "grok-imagine-video", "Grok Imagine Video", "video", ["video"],
            {"videoPerSecond": 0.05},
            context=None,
            capabilities=["video_generation"],
            maxOutputTokens=None,
        ))

        for m in models:
            m["lastUpdated"] = now

        return provider, models
