"""
Google (Gemini, Imagen, Veo) pricing scraper.
Source: https://ai.google.dev/gemini-api/docs/pricing
Note: Using static data from pricing docs (Jan 2026). Add Playwright for live scraping.
"""
from datetime import datetime, timezone

from app.scrapers.base import BaseScraper

PRICING_URL = "https://ai.google.dev/gemini-api/docs/pricing"
API_DOCS_URL = "https://ai.google.dev"


def _model(
    api_id: str,
    name: str,
    model_type: str,
    modalities: list[str],
    pricing: dict,
    context: int = 1000000,
    capabilities: list[str] | None = None,
    **kw,
) -> dict:
    """Build model dict."""
    return {
        "id": f"google-{api_id}",
        "providerId": "google",
        "name": name,
        "apiId": api_id,
        "type": model_type,
        "modalities": modalities,
        "capabilities": capabilities or ["coding", "document_summaries", "translation", "rag"],
        "contextLength": context,
        "maxOutputTokens": 8192,
        "deprecated": kw.get("deprecated", False),
        "pricing": pricing,
        "sourceUrl": PRICING_URL,
        "lastUpdated": datetime.now(timezone.utc).isoformat(),
        **{k: v for k, v in kw.items() if k != "deprecated"},
    }


class GoogleScraper(BaseScraper):
    provider_id = "google"
    provider_name = "Google"
    pricing_url = PRICING_URL

    async def scrape(self):
        """Google Gemini, Imagen, Veo models — full ecosystem (Jan 2026)."""
        provider = self._provider()
        provider["apiDocsUrl"] = API_DOCS_URL
        now = datetime.now(timezone.utc).isoformat()

        models = []

        # --- Text / Multimodal (Gemini) ---
        gemini = [
            ("gemini-3-pro-preview", "Gemini 3 Pro Preview", 2.0, 12.0, 0.20, 1.0, 6.0),
            ("gemini-3-flash-preview", "Gemini 3 Flash Preview", 0.50, 3.0, 0.05, 0.25, 1.50),
            ("gemini-2.5-pro", "Gemini 2.5 Pro", 1.25, 10.0, 0.125, 0.625, 5.0),
            ("gemini-2.5-flash", "Gemini 2.5 Flash", 0.30, 2.50, 0.03, 0.15, 1.25),
            ("gemini-2.5-flash-lite", "Gemini 2.5 Flash-Lite", 0.10, 0.40, 0.01, 0.05, 0.20),
            ("gemini-2.0-flash", "Gemini 2.0 Flash", 0.10, 0.40, None, 0.05, 0.20),
            ("gemini-2.0-flash-lite", "Gemini 2.0 Flash-Lite", 0.075, 0.30, None, 0.0375, 0.15),
        ]
        for api_id, name, inp, out, cache, batch_in, batch_out in gemini:
            p = {
                "inputPerMillionTokens": inp,
                "outputPerMillionTokens": out,
                "batchInputPerMillionTokens": batch_in,
                "batchOutputPerMillionTokens": batch_out,
            }
            if cache:
                p["cacheInputPerMillionTokens"] = cache
            models.append(_model(
                api_id, name, "multimodal",
                ["text", "image", "video", "audio"],
                p,
                capabilities=["coding", "document_summaries", "image_generation", "rag", "document_analysis"],
            ))

        # --- Image Generation (Imagen) ---
        imagen = [
            ("imagen-4-ultra", "Imagen 4 Ultra", 0.06),
            ("imagen-4-standard", "Imagen 4 Standard", 0.04),
            ("imagen-4-fast", "Imagen 4 Fast", 0.02),
            ("imagen-3", "Imagen 3", 0.03),
        ]
        for api_id, name, price in imagen:
            models.append(_model(
                api_id, name, "image", ["image"],
                {"imageOutputPerImage": price},
                capabilities=["image_generation"],
                contextLength=None,
                maxOutputTokens=None,
            ))

        # --- Video (Veo) ---
        veo = [
            ("veo-3.1-standard", "Veo 3.1 Standard", 0.40),
            ("veo-3.1-fast", "Veo 3.1 Fast", 0.15),
            ("veo-3-standard", "Veo 3 Standard", 0.40),
            ("veo-3-fast", "Veo 3 Fast", 0.15),
            ("veo-2", "Veo 2", 0.35),
        ]
        for api_id, name, price in veo:
            models.append(_model(
                api_id, name, "video", ["video"],
                {"videoPerSecond": price},
                capabilities=["video_generation"],
                contextLength=None,
                maxOutputTokens=None,
            ))

        # --- Embeddings ---
        models.append(_model(
            "gemini-embedding-001", "Gemini Embedding 001", "embedding", ["text"],
            {
                "inputPerMillionTokens": 0.15,
                "batchInputPerMillionTokens": 0.075,
                "notes": "Embeddings; no output tokens",
            },
            capabilities=["rag"],
            contextLength=None,
            maxOutputTokens=None,
        ))

        for m in models:
            m["lastUpdated"] = now

        return provider, models
