"""
Rate limiter — SlowAPI. Configurable via RATE_LIMIT env (e.g. 100/minute).
"""
import os

from slowapi import Limiter
from slowapi.util import get_remote_address

_rate_limit = os.getenv("RATE_LIMIT", "100/minute").strip()
_default_limits = [_rate_limit] if _rate_limit else []

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=_default_limits,
    enabled=bool(_rate_limit),
)
