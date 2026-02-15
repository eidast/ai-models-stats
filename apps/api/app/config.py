"""
Configuration from environment variables (12-factor).
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from functools import lru_cache

# Load .env from project root
load_dotenv(Path(__file__).resolve().parents[3] / ".env")


@lru_cache
def get_database_url() -> str:
    """Build DATABASE_URL from env or individual vars."""
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    host = os.getenv("DATABASE_HOST", "localhost")
    port = os.getenv("DATABASE_PORT", "5432")
    name = os.getenv("DATABASE_NAME", "ai_models_stats")
    user = os.getenv("DATABASE_USER", "postgres")
    password = os.getenv("DATABASE_PASSWORD", "")
    return f"postgresql://{user}:{password}@{host}:{port}/{name}"
