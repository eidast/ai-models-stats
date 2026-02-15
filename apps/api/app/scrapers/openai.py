"""
OpenAI pricing scraper.
Sources:
  - https://developers.openai.com/api/docs/pricing (canonical API docs)
  - https://openai.com/api/pricing/ (marketing)
Note: Using static data from pricing docs (Feb 2026). Add Playwright for live scraping.
"""
from datetime import datetime, timezone

from app.scrapers.base import BaseScraper

PRICING_URL = "https://developers.openai.com/api/docs/pricing"
API_DOCS_URL = "https://platform.openai.com/docs"


def _model(api_id: str, name: str, model_type: str, modalities: list[str], pricing: dict, **kw) -> dict:
    """Build model dict with common defaults."""
    return {
        "id": f"openai-{api_id}",
        "providerId": "openai",
        "name": name,
        "apiId": api_id,
        "type": model_type,
        "modalities": modalities,
        "capabilities": kw.get("capabilities", ["coding", "document_summaries", "translation"]),
        "contextLength": kw.get("contextLength", 128000),
        "maxOutputTokens": kw.get("maxOutputTokens", 16384),
        "deprecated": kw.get("deprecated", False),
        "pricing": pricing,
        "sourceUrl": PRICING_URL,
        "lastUpdated": datetime.now(timezone.utc).isoformat(),
        **{k: v for k, v in kw.items() if k not in ("capabilities", "contextLength", "maxOutputTokens", "deprecated")},
    }


class OpenAIScraper(BaseScraper):
    provider_id = "openai"
    provider_name = "OpenAI"
    pricing_url = PRICING_URL

    async def scrape(self):
        """OpenAI models — text, image, audio, video, embeddings (Standard tier where applicable)."""
        provider = self._provider()
        provider["apiDocsUrl"] = API_DOCS_URL
        now = datetime.now(timezone.utc).isoformat()

        models = []

        # --- Text models (Standard tier) ---
        text_models = [
            ("gpt-5.2", "GPT-5.2", 1.75, 0.175, 14.0),
            ("gpt-5.1", "GPT-5.1", 1.25, 0.125, 10.0),
            ("gpt-5", "GPT-5", 1.25, 0.125, 10.0),
            ("gpt-5-mini", "GPT-5 mini", 0.25, 0.025, 2.0),
            ("gpt-5-nano", "GPT-5 nano", 0.05, 0.005, 0.40),
            ("gpt-5.2-pro", "GPT-5.2 Pro", 21.0, None, 168.0),
            ("gpt-5-pro", "GPT-5 Pro", 15.0, None, 120.0),
            ("gpt-4.1", "GPT-4.1", 2.0, 0.50, 8.0),
            ("gpt-4.1-mini", "GPT-4.1 mini", 0.40, 0.10, 1.60),
            ("gpt-4.1-nano", "GPT-4.1 nano", 0.10, 0.025, 0.40),
            ("gpt-4o", "GPT-4o", 2.50, 1.25, 10.0),
            ("gpt-4o-mini", "GPT-4o mini", 0.15, 0.075, 0.60),
            ("o1", "O1", 15.0, 7.50, 60.0, "reasoning"),
            ("o1-pro", "O1 Pro", 150.0, None, 600.0, "reasoning"),
            ("o3-pro", "O3 Pro", 20.0, None, 80.0, "reasoning"),
            ("o3", "O3", 2.0, 0.50, 8.0, "reasoning"),
            ("o4-mini", "O4 mini", 1.10, 0.275, 4.40, "reasoning"),
            ("o3-mini", "O3 mini", 1.10, 0.55, 4.40, "reasoning"),
            ("o1-mini", "O1 mini", 1.10, 0.55, 4.40, "reasoning"),
        ]
        for row in text_models:
            api_id, name, inp, cache, out = row[0], row[1], row[2], row[3], row[4]
            caps = (["coding", "document_summaries", "translation", "reasoning"] if len(row) > 5 and row[5] == "reasoning"
                    else ["coding", "document_summaries", "translation"])
            p = {"inputPerMillionTokens": inp, "outputPerMillionTokens": out, "tier": "standard"}
            if cache is not None:
                p["cacheInputPerMillionTokens"] = cache
            models.append(_model(api_id, name, "text", ["text"], p, capabilities=caps))

        # --- Multimodal (text + image) ---
        multimodal = [
            ("gpt-image-1.5", "GPT Image 1.5", 5.0, 1.25, 10.0),
            ("chatgpt-image-latest", "ChatGPT Image Latest", 5.0, 1.25, 10.0),
            ("gpt-image-1", "GPT Image 1", 5.0, 1.25, None),
            ("gpt-image-1-mini", "GPT Image 1 Mini", 2.0, 0.20, None),
        ]
        for api_id, name, inp, cache, out in multimodal:
            p = {"inputPerMillionTokens": inp, "tier": "standard"}
            if cache:
                p["cacheInputPerMillionTokens"] = cache
            if out:
                p["outputPerMillionTokens"] = out
            p["imageInputPerImage"] = 0.008  # Standard tier image tokens ~$8/1M
            models.append(_model(api_id, name, "multimodal", ["text", "image"], p,
                                 capabilities=["coding", "document_summaries", "image_generation", "rag"]))

        # --- Realtime / Audio ---
        audio_models = [
            ("gpt-realtime", "GPT Realtime", 4.0, 0.40, 16.0),
            ("gpt-realtime-mini", "GPT Realtime Mini", 0.60, 0.06, 2.40),
            ("gpt-audio", "GPT Audio", 2.50, None, 10.0),
            ("gpt-audio-mini", "GPT Audio Mini", 0.60, None, 2.40),
        ]
        for api_id, name, inp, cache, out in audio_models:
            p = {"inputPerMillionTokens": inp, "outputPerMillionTokens": out, "tier": "standard"}
            if cache:
                p["cacheInputPerMillionTokens"] = cache
            p["audioInputPerMillionTokens"] = inp
            p["audioOutputPerMillionTokens"] = out * 4  # audio tokens ~4x text
            models.append(_model(api_id, name, "audio", ["text", "audio"], p,
                                capabilities=["audio_generation", "coding", "document_summaries"]))

        # --- Video (Sora) ---
        models.append(_model("sora-2", "Sora 2", "video", ["video"], {
            "videoPerSecond": 0.10,
            "notes": "720x1280 portrait/landscape",
        }, capabilities=["video_generation"]))
        models.append(_model("sora-2-pro", "Sora 2 Pro", "video", ["video"], {
            "videoPerSecond": 0.30,
            "notes": "720x1280; $0.50 for 1024x1792",
        }, capabilities=["video_generation"]))

        # --- Image generation (per image) ---
        img_gen = [
            ("gpt-image-1.5-gen", "GPT Image 1.5 (generation)", 0.034),
            ("gpt-image-1-gen", "GPT Image 1 (generation)", 0.042),
            ("gpt-image-1-mini-gen", "GPT Image 1 Mini (generation)", 0.011),
            ("dall-e-3", "DALL·E 3", 0.04),
            ("dall-e-2", "DALL·E 2", 0.02),
        ]
        for api_id, name, price in img_gen:
            models.append(_model(api_id, name, "image", ["image"], {
                "imageOutputPerImage": price,
                "notes": "1024x1024 Standard quality",
            }, capabilities=["image_generation"]))

        # --- Embeddings ---
        embeddings = [
            ("text-embedding-3-small", "text-embedding-3-small", 0.02, 0.01),
            ("text-embedding-3-large", "text-embedding-3-large", 0.13, 0.065),
            ("text-embedding-ada-002", "text-embedding-ada-002", 0.10, 0.05),
        ]
        for api_id, name, cost, batch in embeddings:
            models.append(_model(api_id, name, "embedding", ["text"], {
                "inputPerMillionTokens": cost,
                "batchInputPerMillionTokens": batch,
                "notes": "Embeddings; no output tokens",
            }, capabilities=["rag"], maxOutputTokens=None))

        # --- Transcription / TTS ---
        models.append(_model("gpt-4o-mini-tts", "GPT-4o mini TTS", "audio", ["text", "audio"], {
            "inputPerMillionTokens": 0.60,
            "audioOutputPerMillionTokens": 12.0,
            "notes": "~$0.015/min",
        }, capabilities=["audio_generation"]))
        models.append(_model("gpt-4o-transcribe", "GPT-4o Transcribe", "audio", ["audio", "text"], {
            "inputPerMillionTokens": 2.50,
            "outputPerMillionTokens": 10.0,
            "audioInputPerMillionTokens": 6.0,
            "notes": "~$0.006/min",
        }, capabilities=["audio_generation"]))
        models.append(_model("whisper", "Whisper", "audio", ["audio"], {
            "inputPerMillionTokens": 4.0,
            "notes": "~$0.006/min (approximate token equivalent)",
        }, capabilities=["audio_generation"]))

        # Set lastUpdated on all
        for m in models:
            m["lastUpdated"] = now

        return provider, models
