"""Models API."""
from fastapi import APIRouter, HTTPException, Query

from app.services.db_service import get_models, get_model_by_id

router = APIRouter()


@router.get("/models")
async def list_models(
    provider: str | None = Query(None, description="Filter by provider id"),
    capability: str | None = Query(None, description="Filter by capability"),
    type: str | None = Query(None, alias="type", description="Filter by model type"),
    include_deprecated: bool = Query(False, description="Include deprecated models"),
    sort_by: str = Query("provider", description="Sort by: input, output, cache, context, name, provider"),
    sort_order: str = Query("asc", description="Sort order: asc, desc"),
):
    """List models with optional filters and sorting."""
    return await get_models(
        provider_id=provider,
        capability=capability,
        model_type=type,
        include_deprecated=include_deprecated,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get("/models/{model_id}")
async def get_model(model_id: str):
    """Get single model by id."""
    model = await get_model_by_id(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model
