"""
Configuration from environment variables (12-factor).
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from functools import lru_cache
from urllib.parse import urlparse, parse_qs, unquote

# Load .env from repo root when present (local dev). In containers/Cloud Run there is no .env.
try:
    load_dotenv(Path(__file__).resolve().parents[3] / ".env")
except Exception:
    # Avoid crashing in minimal container layouts.
    pass


@lru_cache
def get_database_url() -> str:
    """Return DATABASE_URL (best-effort) for tooling.

    NOTE: For asyncpg we prefer get_database_connect_kwargs(), because asyncpg
    does not reliably support libpq-style unix socket URLs.
    """
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    host = os.getenv("DATABASE_HOST", "localhost")
    port = os.getenv("DATABASE_PORT", "5432")
    name = os.getenv("DATABASE_NAME", "ai_models_stats")
    user = os.getenv("DATABASE_USER", "postgres")
    password = os.getenv("DATABASE_PASSWORD", "")
    return f"postgresql://{user}:{password}@{host}:{port}/{name}"


@lru_cache
def get_database_connect_kwargs() -> dict:
    """Build asyncpg connection kwargs.

    Supports Cloud SQL unix sockets when DATABASE_URL is of the form:
      postgresql://USER:PASSWORD@/DB?host=/cloudsql/<INSTANCE>

    asyncpg expects unix socket directory via the `host` kwarg (not a DSN).
    """
    url = os.getenv("DATABASE_URL")
    if not url:
        return {
            "host": os.getenv("DATABASE_HOST", "localhost"),
            "port": int(os.getenv("DATABASE_PORT", "5432")),
            "database": os.getenv("DATABASE_NAME", "ai_models_stats"),
            "user": os.getenv("DATABASE_USER", "postgres"),
            "password": os.getenv("DATABASE_PASSWORD", ""),
        }

    p = urlparse(url)

    # query params like host=/cloudsql/...
    q = parse_qs(p.query)
    q_host = q.get("host", [None])[0]
    q_port = q.get("port", [None])[0]

    # Path is like /dbname
    dbname = (p.path or "").lstrip("/")

    # If URL has no hostname but query host points to a unix socket dir, use it.
    host = p.hostname or (unquote(q_host) if q_host else None)

    kwargs = {
        "user": unquote(p.username) if p.username else None,
        "password": unquote(p.password) if p.password else None,
        "database": dbname or None,
        "host": host,
    }

    if p.port:
        kwargs["port"] = int(p.port)
    elif q_port:
        kwargs["port"] = int(q_port)

    # Remove Nones
    return {k: v for k, v in kwargs.items() if v is not None}
