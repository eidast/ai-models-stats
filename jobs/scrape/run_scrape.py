#!/usr/bin/env python3
"""
Scrape job — run all scrapers and upsert to PostgreSQL.
Usage: DATABASE_URL=... python -m jobs.scrape.run_scrape
"""
import asyncio
import json
import os
import sys
from pathlib import Path

# Add project root and apps/api to path
root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / "apps" / "api"))

from dotenv import load_dotenv

load_dotenv(root / ".env")

# Import after path setup
from app.db import get_pool, close_pool
from app.scrapers.registry import SCRAPERS
from app.services.upsert_service import upsert_provider, upsert_model


async def run():
    """Run all scrapers and upsert to DB."""
    if not os.getenv("DATABASE_URL"):
        print("ERROR: DATABASE_URL not set")
        sys.exit(1)

    total_models = 0
    for ScraperClass in SCRAPERS:
        scraper = ScraperClass()
        try:
            provider, models = await scraper.scrape()
            await upsert_provider(provider)
            for m in models:
                await upsert_model(m)
                total_models += 1
            print(f"  {scraper.provider_id}: {len(models)} models")
        except Exception as e:
            print(f"  {scraper.provider_id}: ERROR - {e}")

    await close_pool()
    print(f"Scrape completed: {total_models} models upserted")


if __name__ == "__main__":
    asyncio.run(run())
