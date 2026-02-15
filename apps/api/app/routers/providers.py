"""Providers API."""
from fastapi import APIRouter

from app.services.db_service import get_providers

router = APIRouter()


@router.get("/providers")
async def list_providers():
    """List all providers."""
    return await get_providers()
