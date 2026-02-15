"""Upsert providers and models to PostgreSQL."""
import json
from datetime import datetime
from typing import Any

from app.db import get_pool


def _parse_ts(value: str | datetime) -> datetime:
    """Parse lastUpdated to datetime for asyncpg."""
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


async def upsert_provider(provider: dict[str, Any]) -> None:
    """Upsert provider."""
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO providers (id, name, pricing_url, api_docs_url, last_updated)
            VALUES ($1, $2, $3, $4, $5::timestamptz)
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                pricing_url = EXCLUDED.pricing_url,
                api_docs_url = EXCLUDED.api_docs_url,
                last_updated = EXCLUDED.last_updated
            """,
            provider["id"],
            provider["name"],
            provider["pricingUrl"],
            provider.get("apiDocsUrl"),
            _parse_ts(provider["lastUpdated"]),
        )


async def upsert_model(model: dict[str, Any]) -> None:
    """Upsert model."""
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO models (
                id, provider_id, name, api_id, type, modalities, capabilities,
                context_length, max_output_tokens, deprecated, deprecation_date,
                pricing, self_hosted, source_url, last_updated
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11::date, $12, $13, $14, $15::timestamptz)
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                api_id = EXCLUDED.api_id,
                type = EXCLUDED.type,
                modalities = EXCLUDED.modalities,
                capabilities = EXCLUDED.capabilities,
                context_length = EXCLUDED.context_length,
                max_output_tokens = EXCLUDED.max_output_tokens,
                deprecated = EXCLUDED.deprecated,
                deprecation_date = EXCLUDED.deprecation_date,
                pricing = EXCLUDED.pricing,
                self_hosted = EXCLUDED.self_hosted,
                source_url = EXCLUDED.source_url,
                last_updated = EXCLUDED.last_updated
            """,
            model["id"],
            model["providerId"],
            model["name"],
            model.get("apiId"),
            model["type"],
            model["modalities"],
            model["capabilities"],
            model.get("contextLength"),
            model.get("maxOutputTokens"),
            model.get("deprecated", False),
            model.get("deprecationDate"),
            json.dumps(model["pricing"]),
            json.dumps(model["selfHosted"]) if model.get("selfHosted") else None,
            model["sourceUrl"],
            _parse_ts(model["lastUpdated"]),
        )
