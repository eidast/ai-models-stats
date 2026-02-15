"""Compare models API."""
from fastapi import APIRouter, Query

from app.services.db_service import get_models_by_ids

router = APIRouter()


@router.get("/compare")
async def compare_models(
    ids: str = Query(..., description="Comma-separated model ids (e.g. id1,id2,id3)"),
):
    """Compare multiple models side by side."""
    model_ids = [i.strip() for i in ids.split(",") if i.strip()][:10]
    models = await get_models_by_ids(model_ids)
    return {"models": models}
