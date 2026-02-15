#!/usr/bin/env python3
"""
Run database migrations.
Usage: DATABASE_URL=... python -m jobs.scrape.run_migrate
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "apps", "api"))

import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/ai_models_stats")
MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "apps", "api", "migrations")


async def migrate():
    conn = await asyncpg.connect(DATABASE_URL)
    for name in sorted(os.listdir(MIGRATIONS_DIR)):
        if name.endswith(".sql"):
            path = os.path.join(MIGRATIONS_DIR, name)
            with open(path) as f:
                sql = f.read()
            print(f"Running {name}...")
            await conn.execute(sql)
    await conn.close()
    print("Migrations completed.")


if __name__ == "__main__":
    asyncio.run(migrate())
