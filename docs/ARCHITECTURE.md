# Architecture — AI Models Stats Monorepo

**Stack:** Next.js (FE) + FastAPI (BE) | PostgreSQL | pnpm workspaces | GCP Cloud Run  
**Methodology:** [12-Factor App](12-FACTOR.md) — config via env vars, stateless processes

---

## 1. Monorepo Structure

```
ai-models-stats/
├── apps/
│   ├── web/                 # Next.js frontend
│   │   ├── app/
│   │   ├── components/
│   │   ├── lib/
│   │   └── package.json
│   └── api/                 # FastAPI backend
│       ├── app/
│       │   ├── main.py
│       │   ├── routers/
│       │   ├── services/
│       │   ├── scrapers/
│       │   └── migrations/
│       ├── requirements.txt
│       └── Dockerfile
├── packages/
│   ├── shared-types/        # TypeScript types (from schema)
│   │   └── package.json
│   └── schema/              # JSON Schema + validation
│       └── package.json
├── jobs/
│   └── scrape/              # Scraping job (Python)
│       └── run_scrape.py
├── docs/
│   ├── PRD.md
│   ├── SCHEMA.md
│   ├── DATABASE.md          # PostgreSQL schema
│   ├── 12-FACTOR.md         # 12-factor config & env vars
│   └── ARCHITECTURE.md
├── pnpm-workspace.yaml
├── package.json
├── turbo.json               # Optional: Turborepo
└── .github/
    └── workflows/           # CI/CD, scheduled scrape
```

---

## 2. Component Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           USERS (Browser)                                │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Next.js (apps/web)                                                       │
│  - App Router, i18n (EN/ES), SSR/SSG                                     │
│  - Model list, comparison table, filters, favorites (localStorage)        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
┌──────────────────────────────┐    ┌──────────────────────────────────────┐
│  Next.js (build/runtime)      │    │  FastAPI (apps/api)                    │
│  - Fetches from API           │    │  - GET /api/models, /api/providers      │
│  - Favorites in localStorage  │    │  - GET /api/compare?ids=...            │
└──────────────────────────────┘    └──────────────────────────────────────┘
                                                    │
                                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PostgreSQL                                                              │
│  - providers, models (pricing/self_hosted as JSONB), price_history       │
│  - Connection via DATABASE_URL env var                                    │
└─────────────────────────────────────────────────────────────────────────┘
                                    ▲
                                    │
┌─────────────────────────────────────────────────────────────────────────┐
│  Scraping Job (every 24h)                                                 │
│  - Cloud Scheduler → Cloud Run Job (or GitHub Actions cron)               │
│  - Python: Playwright/BeautifulSoup + provider-specific parsers           │
│  - Writes to PostgreSQL (upsert providers, models)                        │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Data Flow

### 3.1 Scrape Job (Daily)

1. **Trigger:** Cloud Scheduler (or GitHub Actions) at 00:00 UTC
2. **Config:** `DATABASE_URL` from environment (12-factor)
3. **Process:**
   - For each provider: check for official API first
   - If API: fetch pricing via API
   - Else: run scraper (Playwright/BeautifulSoup)
   - Parse → validate against schema → upsert to PostgreSQL
4. **Output:** Upsert into `providers`, `models`; optional append to `price_history`
5. **Deprecation:** Scraper or manual config marks `deprecated: true` for EOL models

### 3.2 Frontend (Next.js)

1. **Data source:** Fetch from FastAPI `/api/models` at runtime (API reads from PostgreSQL)
2. **Config:** `NEXT_PUBLIC_API_URL` for API base URL (env var, 12-factor)
3. **Favorites:** `localStorage` key `ai-models-favorites` = `string[]` of model IDs

### 3.3 API (FastAPI)

- `GET /api/models` — list all models (query: `?provider=`, `?capability=`, `?type=`)
- `GET /api/models/:id` — single model
- `GET /api/providers` — list providers
- `GET /api/compare` — `?ids=id1,id2,id3` → comparison payload
- `GET /api/health` — health check for Cloud Run

---

## 4. Technology Choices

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Backend | FastAPI (Python) | Strong scraping ecosystem (Playwright, BeautifulSoup); async; OpenAPI |
| Frontend | Next.js | SSR, i18n, Vercel/Cloud Run friendly |
| Database | PostgreSQL | Structured schema, JSONB for nested objects, strong query support |
| Monorepo | pnpm workspaces | Fast, disk-efficient; native workspace support |
| Config | Environment variables | 12-factor; credentials via `DATABASE_URL` |
| Deployment | GCP Cloud Run | Serverless, scales to zero; supports both Next.js and FastAPI |

---

## 5. Deployment (Cloud Run)

### 5.1 Services

| Service | Source | Port |
|---------|--------|------|
| `ai-models-web` | `apps/web` (Next.js) | 3000 |
| `ai-models-api` | `apps/api` (FastAPI) | 8080 |
| `ai-models-scrape` | `jobs/scrape` (Python) | Job (no HTTP) |

### 5.2 Build

- **Web:** `docker build -f apps/web/Dockerfile .` or `pnpm build` + Node runtime
- **API:** `docker build -f apps/api/Dockerfile .` (Python 3.11+)
- **Scrape:** Run as Cloud Run Job; reads URLs from config; writes to Cloud Storage or artifact registry

### 5.3 Data Persistence

- **PostgreSQL** — single source of truth
- Connection via `DATABASE_URL` (user/password from env; 12-factor)
- Scrape job writes directly to DB; API reads from DB
- See [DATABASE.md](DATABASE.md) for schema

---

## 6. Scraper Architecture

```
scrapers/
├── base.py           # Base scraper interface
├── openai.py         # OpenAI pricing page
├── google.py         # Google Gemini pricing
├── mistral.py        # Mistral pricing
├── deepseek.py       # DeepSeek pricing
└── registry.py       # Provider → scraper mapping
```

Each scraper:
1. Fetches URL (HTTP or Playwright for JS-rendered pages)
2. Parses HTML/JSON
3. Returns list of `Model` dicts
4. Validates against JSON Schema before write

---

## 7. 12-Factor & Config

All config via environment variables. See [12-FACTOR.md](12-FACTOR.md).

| Variable | Apps | Description |
|----------|------|--------------|
| `DATABASE_URL` | API, Scrape | `postgresql://user:password@host:port/dbname` |
| `PORT` | API, Web | Server port (Cloud Run sets) |
| `NEXT_PUBLIC_API_URL` | Web | API base URL |
| `LOG_LEVEL` | API, Scrape | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

---

## 8. Security Considerations

- No auth → public read-only API
- Credentials only in env vars; never in code
- Scrape job: no secrets in URLs; rate-limit requests to avoid blocking
- CORS: allow `ai-models-web` origin only
- No PII; no user data beyond localStorage (client-side)

---

## 10. Future Extensions

- Benchmark scores (MMLU, HumanEval) from public sources
- API-first providers: Anthropic, OpenAI (if pricing API exists)
- Admin UI for manual overrides / deprecation flags
