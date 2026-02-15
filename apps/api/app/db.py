"""
Database connection pool — asyncpg.
Uses DATABASE_URL from environment.
"""
import asyncpg
from app.config import get_database_connect_kwargs

_pool: asyncpg.Pool | None = None


async def get_pool() -> asyncpg.Pool:
    """Get or create connection pool."""
    global _pool
    if _pool is None:
        connect_kwargs = get_database_connect_kwargs()
        _pool = await asyncpg.create_pool(
            **connect_kwargs,
            min_size=1,
            max_size=10,
            command_timeout=60,
        )
    return _pool


async def close_pool() -> None:
    """Close pool on shutdown."""
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
