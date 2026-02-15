# AI Models Stats

A reference website for comparing LLM models across providers — costs, capabilities, and limits.

## Documentation

| Document | Description |
|----------|-------------|
| [PRD](docs/PRD.md) | Product Requirements Document — goals, features, scope |
| [SCHEMA](docs/SCHEMA.md) | Data schema for models, providers, pricing |
| [DATABASE](docs/DATABASE.md) | PostgreSQL schema, migrations |
| [ARCHITECTURE](docs/ARCHITECTURE.md) | Monorepo structure, tech stack, deployment |
| [12-FACTOR](docs/12-FACTOR.md) | 12-factor app methodology, environment variables |
| [ACTIVITIES](docs/ACTIVITIES.md) | Implementation tasks and sprint breakdown |
| [SCRAPING](docs/SCRAPING.md) | How to fetch real data from provider sites and run scrape |
| [OPENAI_PRICING](docs/OPENAI_PRICING.md) | OpenAI pricing page structure (developers.openai.com) |
| [MISTRAL_PRICING](docs/MISTRAL_PRICING.md) | Mistral AI model ecosystem and pricing |
| [ANTHROPIC_PRICING](docs/ANTHROPIC_PRICING.md) | Anthropic (Claude) pricing structure |

## Tech Stack

- **Frontend:** Next.js (App Router)
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL (config via `DATABASE_URL`)
- **Monorepo:** pnpm workspaces
- **Methodology:** 12-Factor App (config via env vars)
- **Deployment:** GCP Cloud Run

## Initial Data Sources

- [OpenAI Pricing](https://developers.openai.com/api/docs/pricing)
- [Anthropic (Claude) Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [Google Gemini Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Mistral Pricing](https://mistral.ai/pricing#api)
- [DeepSeek Pricing](https://api-docs.deepseek.com/quick_start/pricing)

## Quick Start

1. **Copy env and set `DATABASE_URL`:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

2. **Create Python venv and install deps:**
   ```bash
   python3 -m venv .venv
   .venv/bin/pip install -r apps/api/requirements.txt
   ```

3. **Install, migrate and seed:**
   ```bash
   pnpm install
   pnpm db:migrate
   pnpm db:seed
   ```

4. **Run API and Web (two terminals):**
   ```bash
   pnpm dev:api   # Terminal 1 — API on :8080
   pnpm dev:web   # Terminal 2 — Web on :3000
   ```

5. **Open:** http://localhost:3000

6. **Run scrape (optional — fetches/upserts models to DB):**
   ```bash
   pnpm db:scrape
   ```
   See [SCRAPING](docs/SCRAPING.md) for real-data strategy (scrapers currently use static placeholders).

## License

See [LICENSE](LICENSE).
