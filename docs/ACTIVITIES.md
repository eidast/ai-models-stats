# Implementation Activities — AI Models Stats

**Purpose:** Ordered list of tasks to build the product. Can be used as sprint backlog or roadmap.

---

## Phase 0: Foundation

| ID | Activity | Description | Est. |
|----|----------|-------------|------|
| 0.1 | Monorepo setup | Create `pnpm-workspace.yaml`, root `package.json`, `apps/`, `packages/` structure | 0.5d |
| 0.2 | Shared schema package | JSON Schema for Model, Provider, Pricing; export from `packages/schema` | 0.5d |
| 0.3 | Shared types package | TypeScript types generated from schema for `packages/shared-types` | 0.5d |
| 0.4 | PostgreSQL migrations | Create `apps/api/migrations/` with SQL for `providers`, `models`, `price_history` | 0.5d |
| 0.5 | Sample data / seed | Seed script to insert 2–3 sample models into PostgreSQL | 0.5d |

---

## Phase 1: Backend (API + Scraping)

| ID | Activity | Description | Est. |
|----|----------|-------------|------|
| 1.1 | FastAPI project | Initialize `apps/api` with FastAPI, structure `routers/`, `services/` | 0.5d |
| 1.2 | Models router | `GET /api/models`, `GET /api/models/:id` with query filters (provider, capability, type) | 1d |
| 1.3 | Providers router | `GET /api/providers` | 0.25d |
| 1.4 | Compare endpoint | `GET /api/compare?ids=id1,id2` returns comparison payload | 0.5d |
| 1.5 | Database layer | Async PostgreSQL client (asyncpg); load models/providers from DB; use `DATABASE_URL` | 1d |
| 1.6 | Base scraper | Abstract base class + fetch logic (httpx + optional Playwright) | 1d |
| 1.7 | OpenAI scraper | Parser for https://openai.com/es-419/api/pricing/ | 1.5d |
| 1.8 | Google scraper | Parser for https://ai.google.dev/gemini-api/docs/pricing | 2d |
| 1.9 | Mistral scraper | Parser for https://mistral.ai/pricing#api | 1d |
| 1.10 | DeepSeek scraper | Parser for https://api-docs.deepseek.com/quick_start/pricing | 0.5d |
| 1.11 | Scrape job script | `jobs/scrape/run_scrape.py` — runs all scrapers, validates, upserts to PostgreSQL via `DATABASE_URL` | 1d |
| 1.12 | Schema validation | Validate scraper output against JSON Schema before write | 0.5d |
| 1.13 | API Dockerfile | Dockerfile for FastAPI; Cloud Run ready; `DATABASE_URL` from env | 0.5d |
| 1.14 | .env.example | Document all env vars; add to repo (no secrets) | 0.25d |

---

## Phase 2: Frontend (Next.js)

| ID | Activity | Description | Est. |
|----|----------|-------------|------|
| 2.1 | Next.js project | Initialize `apps/web` with App Router, Tailwind | 0.5d |
| 2.2 | i18n setup | next-intl or similar for EN/ES | 0.5d |
| 2.3 | Layout & navigation | Header, footer, basic layout | 0.5d |
| 2.4 | Home page | Landing with CTA to model list | 0.5d |
| 2.5 | Model list page | Table/cards of models; fetch from API or static JSON | 1d |
| 2.6 | Filters | Filter by provider, capability, type (client or server) | 1d |
| 2.7 | Model detail page | Single model view with full pricing, capabilities, limits | 1d |
| 2.8 | Comparison view | Select 2–5 models; side-by-side table (input/output per 1M, context, etc.) | 1.5d |
| 2.9 | Task cost table | Component showing estimated cost for reference tasks | 1d |
| 2.10 | Favorites (localStorage) | Toggle favorite; persist; filter "My favorites" | 0.5d |
| 2.11 | Deprecation badge | Show "Deprecated" / "EOL" badge; exclude from default list option | 0.25d |
| 2.12 | Responsive design | Mobile-friendly tables (horizontal scroll or cards) | 0.5d |
| 2.13 | Web Dockerfile | Dockerfile for Next.js; Cloud Run ready | 0.5d |

---

## Phase 3: Capability Tagging & OSS

| ID | Activity | Description | Est. |
|----|----------|-------------|------|
| 3.1 | Capability research | Document benchmark sources (MMLU, HumanEval, etc.) and mapping to clusters | 1d |
| 3.2 | Capability tagging | Add `capabilities` to each model (manual or script from provider docs) | 1d |
| 3.3 | OSS models list | Add Llama, Mistral OSS, etc. with `selfHosted` block | 1d |
| 3.4 | Hardware requirements | Define `runsOn` values; document M4 Mac Mini, Gaming PC specs | 0.5d |

---

## Phase 4: DevOps & Automation

| ID | Activity | Description | Est. |
|----|----------|-------------|------|
| 4.1 | GitHub Actions: CI | Lint, test, build on PR | 0.5d |
| 4.2 | GitHub Actions: Scrape | Scheduled workflow (daily) to run scrape, commit `data/` if changed | 1d |
| 4.3 | Cloud Run: API | Deploy FastAPI to Cloud Run | 0.5d |
| 4.4 | Cloud Run: Web | Deploy Next.js to Cloud Run | 0.5d |
| 4.5 | Cloud Scheduler (optional) | If not using GitHub Actions for scrape | 0.5d |

---

## Phase 5: Polish

| ID | Activity | Description | Est. |
|----|----------|-------------|------|
| 5.1 | SEO & meta | Title, description, OG tags per page | 0.25d |
| 5.2 | Error states | 404, API error handling | 0.25d |
| 5.3 | Loading states | Skeletons, spinners | 0.25d |
| 5.4 | Accessibility | Basic a11y (labels, focus, contrast) | 0.5d |

---

## Dependency Graph (Critical Path)

```
0.1 → 0.2 → 0.3 → 0.4 → 0.5
  ↓
1.1 → 1.2, 1.3, 1.4, 1.5 (parallel)
  ↓
1.6 → 1.7, 1.8, 1.9, 1.10 (parallel) → 1.11 → 1.12

0.5, 1.5 → 2.1 → 2.2 → 2.3 → 2.4 → 2.5 → 2.6, 2.7, 2.8, 2.9, 2.10
```

---

## Suggested Sprint Breakdown

| Sprint | Focus | Activities |
|--------|-------|------------|
| 1 | Foundation + API | 0.1–0.5, 1.1–1.5 |
| 2 | Scrapers | 1.6–1.12 |
| 3 | Frontend core | 2.1–2.7 |
| 4 | Comparison + favorites | 2.8–2.12 |
| 5 | Capabilities + OSS | 3.1–3.4 |
| 6 | DevOps + polish | 4.1–4.5, 5.1–5.4 |

---

## Total Estimate

| Phase | Days |
|-------|------|
| 0 | 2.5 |
| 1 | 10.75 |
| 2 | 9 |
| 3 | 3.5 |
| 4 | 3 |
| 5 | 1.25 |
| **Total** | **~28.75 d** |

(Assuming 1 developer; parallelization can reduce calendar time.)
