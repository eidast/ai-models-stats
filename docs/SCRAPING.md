# Scraping Strategy — Real Data Collection

**Purpose:** How to fetch real pricing data from provider websites and load it into PostgreSQL.

---

## Current State

| Component | Status |
|-----------|--------|
| `run_seed.py` | Static seed data (no HTTP). Use for dev only. |
| `run_scrape.py` | Runs all scrapers → upserts to DB. **Pipeline ready.** |
| Scrapers | Return **static data** (placeholders). No real fetch yet. |

---

## How to Run Scrape (and Upload to DB)

```bash
# From project root (loads .env automatically)
pnpm db:scrape

# Or directly
DATABASE_URL=postgresql://user:pass@host:5432/dbname python -m jobs.scrape.run_scrape
```

**Requirements:**
- `DATABASE_URL` in `.env` or environment
- Migrations applied (`pnpm db:migrate`)

---

## Implementing Real Scrapers

Each scraper must:
1. **Fetch** the pricing page (HTTP or Playwright)
2. **Parse** HTML/JSON
3. **Return** `(provider_dict, list[model_dict])` matching the schema

### Provider-Specific Approaches

| Provider | URL | Approach | Notes |
|----------|-----|----------|-------|
| **OpenAI** | https://developers.openai.com/api/docs/pricing | Playwright | JS-rendered; see [OPENAI_PRICING](OPENAI_PRICING.md) |
| **Anthropic** | https://platform.claude.com/docs/en/about-claude/pricing | Playwright or httpx | See [ANTHROPIC_PRICING](ANTHROPIC_PRICING.md) |
| **Google** | https://ai.google.dev/gemini-api/docs/pricing | Playwright or httpx | Docs page; may have JSON in page |
| **Mistral** | https://mistral.ai/pricing#api | httpx + BeautifulSoup | See [MISTRAL_PRICING](MISTRAL_PRICING.md) |
| **DeepSeek** | https://api-docs.deepseek.com/quick_start/pricing | httpx + BeautifulSoup | Docs; often simple tables |

### Base Scraper Helpers (to add in `base.py`)

```python
# For static HTML
import httpx
from bs4 import BeautifulSoup

async def fetch_html(url: str) -> str:
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.text

# For JS-rendered pages
# pip install playwright && playwright install chromium
from playwright.async_api import async_playwright

async def fetch_rendered(url: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        html = await page.content()
        await browser.close()
        return html
```

### Example: DeepSeek (simplest — static HTML)

```python
# apps/api/app/scrapers/deepseek.py
import httpx
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper

class DeepSeekScraper(BaseScraper):
    async def scrape(self):
        async with httpx.AsyncClient() as client:
            r = await client.get(self.pricing_url)
            r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        # Parse tables/sections → build models list
        models = [...]  # from parsed data
        return self._provider(), models
```

---

## Automation

| Method | When | Config |
|--------|------|--------|
| **Local** | Manual | `pnpm db:scrape` |
| **GitHub Actions** | Daily 00:00 UTC | `.github/workflows/scrape.yml` — needs `secrets.DATABASE_URL` |
| **Cloud Run Job** | Cron via Cloud Scheduler | Deploy job image; set `DATABASE_URL` |

---

## Dependencies

Already in `requirements.txt`:
- `httpx` — HTTP client
- `beautifulsoup4` — HTML parsing

To add for JS pages:
```
playwright==1.49.0
```
Then: `playwright install chromium`

---

## Data Flow

```
Provider websites
       ↓
  Scrapers (fetch + parse)
       ↓
  run_scrape.py (orchestrator)
       ↓
  upsert_provider / upsert_model
       ↓
  PostgreSQL (providers, models, price_history)
```
