"""
Database service — models and providers CRUD.
"""
import json
from typing import Any

import asyncpg

from app.db import get_pool


def _parse_jsonb(val: Any) -> Any:
    """Parse JSONB from DB — may be dict or JSON string."""
    if val is None:
        return None
    if isinstance(val, dict):
        return val
    if isinstance(val, str):
        return json.loads(val)
    return val


def _row_to_provider(row: asyncpg.Record) -> dict[str, Any]:
    return {
        "id": row["id"],
        "name": row["name"],
        "pricingUrl": row["pricing_url"],
        "apiDocsUrl": row["api_docs_url"],
        "lastUpdated": row["last_updated"].isoformat() if row["last_updated"] else None,
    }


def _row_to_model(row: asyncpg.Record) -> dict[str, Any]:
    return {
        "id": row["id"],
        "providerId": row["provider_id"],
        "name": row["name"],
        "apiId": row["api_id"],
        "type": row["type"],
        "modalities": list(row["modalities"]) if row["modalities"] else [],
        "capabilities": list(row["capabilities"]) if row["capabilities"] else [],
        "contextLength": row["context_length"],
        "maxOutputTokens": row["max_output_tokens"],
        "deprecated": row["deprecated"],
        "deprecationDate": row["deprecation_date"].isoformat() if row["deprecation_date"] else None,
        "pricing": _parse_jsonb(row["pricing"]),
        "selfHosted": _parse_jsonb(row["self_hosted"]),
        "sourceUrl": row["source_url"],
        "lastUpdated": row["last_updated"].isoformat() if row["last_updated"] else None,
    }


async def get_providers() -> list[dict[str, Any]]:
    """Fetch all providers."""
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM providers ORDER BY name")
    return [_row_to_provider(r) for r in rows]


# Valid sort columns: input/output/cache from JSONB, context from column
SORT_COLUMNS = {"input", "output", "cache", "context", "name", "provider"}


def _order_clause(sort_by: str, sort_order: str) -> str:
    """Build ORDER BY clause. sort_order: asc|desc."""
    asc = "ASC" if sort_order.lower() == "asc" else "DESC"
    nulls = "NULLS LAST"
    # NULLIF avoids cast error on empty string
    if sort_by == "input":
        return f"(NULLIF(pricing->>'inputPerMillionTokens', '')::numeric) {asc} {nulls}"
    if sort_by == "output":
        return f"(NULLIF(pricing->>'outputPerMillionTokens', '')::numeric) {asc} {nulls}"
    if sort_by == "cache":
        return f"(NULLIF(pricing->>'cacheInputPerMillionTokens', '')::numeric) {asc} {nulls}"
    if sort_by == "context":
        return f"context_length {asc} {nulls}"
    if sort_by == "name":
        return f"name {asc}"
    if sort_by == "provider":
        return f"provider_id {asc}, name {asc}"
    return "provider_id, name"


async def get_models(
    provider_id: str | None = None,
    capability: str | None = None,
    model_type: str | None = None,
    include_deprecated: bool = False,
    sort_by: str = "provider",
    sort_order: str = "asc",
) -> list[dict[str, Any]]:
    """Fetch models with optional filters and sorting."""
    pool = await get_pool()
    conditions = []
    args: list[Any] = []
    n = 0

    if provider_id:
        n += 1
        conditions.append(f"provider_id = ${n}")
        args.append(provider_id)
    if capability:
        n += 1
        conditions.append(f"${n} = ANY(capabilities)")
        args.append(capability)
    if model_type:
        n += 1
        conditions.append(f"type = ${n}")
        args.append(model_type)
    if not include_deprecated:
        conditions.append("deprecated = false")

    where = " AND ".join(conditions) if conditions else "1=1"
    order_col = sort_by if sort_by in SORT_COLUMNS else "provider"
    order_clause = _order_clause(order_col, sort_order)
    query = f"SELECT * FROM models WHERE {where} ORDER BY {order_clause}"

    async with pool.acquire() as conn:
        rows = await conn.fetch(query, *args)
    return [_row_to_model(r) for r in rows]


async def get_model_by_id(model_id: str) -> dict[str, Any] | None:
    """Fetch single model by id."""
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM models WHERE id = $1", model_id)
    if not row:
        return None
    return _row_to_model(row)


async def get_models_by_ids(ids: list[str]) -> list[dict[str, Any]]:
    """Fetch models by list of ids."""
    if not ids:
        return []
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT * FROM models WHERE id = ANY($1::varchar[]) ORDER BY provider_id, name",
            ids,
        )
    return [_row_to_model(r) for r in rows]
