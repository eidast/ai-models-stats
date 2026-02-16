#!/usr/bin/env python3
"""
Seed script — insert sample providers and models for development.
Run: DATABASE_URL=... python -m jobs.scrape.run_seed
"""
import asyncio
import json
import os
import sys
from datetime import datetime, timezone

# Add apps/api to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "apps", "api"))

import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/ai_models_stats")


async def seed():
    conn = await asyncpg.connect(DATABASE_URL)

    # Providers
    await conn.execute(
        """
        INSERT INTO providers (id, name, pricing_url, api_docs_url, last_updated)
        VALUES
            ('openai', 'OpenAI', 'https://openai.com/api/pricing/', 'https://platform.openai.com/docs', $1),
            ('anthropic', 'Anthropic', 'https://platform.claude.com/docs/en/about-claude/pricing', 'https://docs.anthropic.com', $1),
            ('google', 'Google', 'https://ai.google.dev/gemini-api/docs/pricing', 'https://ai.google.dev', $1),
            ('mistral', 'Mistral AI', 'https://mistral.ai/pricing#api', 'https://docs.mistral.ai', $1),
            ('deepseek', 'DeepSeek', 'https://api-docs.deepseek.com/quick_start/pricing', 'https://api-docs.deepseek.com', $1),
            ('xai', 'xAI (Grok)', 'https://docs.x.ai/developers/models', 'https://docs.x.ai', $1)
        ON CONFLICT (id) DO UPDATE SET
            name = EXCLUDED.name,
            pricing_url = EXCLUDED.pricing_url,
            last_updated = EXCLUDED.last_updated
        """,
        datetime.now(timezone.utc),
    )

    # Sample models
    now = datetime.now(timezone.utc)
    models = [
        {
            "id": "openai-gpt-5-mini",
            "provider_id": "openai",
            "name": "GPT-5 mini",
            "api_id": "gpt-5-mini",
            "type": "text",
            "modalities": ["text"],
            "capabilities": ["coding", "document_summaries", "translation"],
            "context_length": 128000,
            "max_output_tokens": 16384,
            "deprecated": False,
            "pricing": {
                "inputPerMillionTokens": 0.25,
                "outputPerMillionTokens": 2.0,
                "cacheInputPerMillionTokens": 0.025,
            },
            "source_url": "https://openai.com/api/pricing/",
        },
        {
            "id": "deepseek-deepseek-chat",
            "provider_id": "deepseek",
            "name": "DeepSeek Chat",
            "api_id": "deepseek-chat",
            "type": "text",
            "modalities": ["text"],
            "capabilities": ["coding", "document_summaries", "rag"],
            "context_length": 128000,
            "max_output_tokens": 8192,
            "deprecated": False,
            "pricing": {
                "inputPerMillionTokens": 0.28,
                "outputPerMillionTokens": 0.42,
                "cacheInputPerMillionTokens": 0.028,
            },
            "source_url": "https://api-docs.deepseek.com/quick_start/pricing",
        },
        {
            "id": "google-gemini-2.5-flash",
            "provider_id": "google",
            "name": "Gemini 2.5 Flash",
            "api_id": "gemini-2.5-flash",
            "type": "multimodal",
            "modalities": ["text", "image", "video", "audio"],
            "capabilities": ["coding", "document_summaries", "image_generation", "rag"],
            "context_length": 1000000,
            "max_output_tokens": 8192,
            "deprecated": False,
            "pricing": {
                "inputPerMillionTokens": 0.30,
                "outputPerMillionTokens": 2.50,
                "cacheInputPerMillionTokens": 0.03,
            },
            "source_url": "https://ai.google.dev/gemini-api/docs/pricing",
        },
    ]

    for m in models:
        await conn.execute(
            """
            INSERT INTO models (
                id, provider_id, name, api_id, type, modalities, capabilities,
                context_length, max_output_tokens, deprecated, pricing, source_url, last_updated
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                pricing = EXCLUDED.pricing,
                last_updated = EXCLUDED.last_updated
            """,
            m["id"],
            m["provider_id"],
            m["name"],
            m.get("api_id"),
            m["type"],
            m["modalities"],
            m["capabilities"],
            m.get("context_length"),
            m.get("max_output_tokens"),
            m.get("deprecated", False),
            json.dumps(m["pricing"]),
            m["source_url"],
            now,
        )

    await conn.close()
    print("Seed completed: 6 providers, 3 models")


if __name__ == "__main__":
    asyncio.run(seed())
