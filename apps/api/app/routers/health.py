"""Health check endpoint for Cloud Run."""
from fastapi import APIRouter, Request

from app.limiter import limiter

router = APIRouter()


@router.get("/health")
@limiter.exempt
async def health(request: Request):
    """Liveness/readiness probe. Exempt from rate limiting."""
    return {"status": "ok"}
