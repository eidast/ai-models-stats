# CI/CD & Configuration — Analysis

**Purpose:** Document the CI/CD pipelines and configuration added to the project (e.g. by automation agents).

---

## 1. GitHub Actions Workflows

### 1.1 CI (`ci.yml`)

**Trigger:** Push/PR to `main`

**Jobs:**
- **lint-build:** Lint + build web
  - pnpm 9.14.2, Node 20
  - `NEXT_PUBLIC_API_URL: https://api.example.com` (placeholder for build)
- **api-test:** API integration tests
  - Postgres 16 service
  - Migrations → seed → start API → health check + `/api/models` curl

### 1.2 Deploy Web (`deploy-web-cloudrun.yml`)

**Trigger:** Push to `main` when paths change: `apps/web/**`, packages, lockfile, workflow file

**Config:**
- Project: `sq-websites`
- Region: `us-central1`
- Service: `ai-models-web`
- Auth: Workload Identity Federation (no JSON keys)
- Build: Docker → Artifact Registry
- Deploy: Cloud Run, port 3000
- Env: `NEXT_PUBLIC_API_URL` from secrets

### 1.3 Deploy API (`deploy-api-cloudrun.yml`)

**Trigger:** Push to `main` when paths change: `apps/api/**`, `jobs/**`, packages, lockfile

**Config:**
- Service: `ai-models-api`
- Runtime SA: `ai-models-runtime@sq-websites.iam.gserviceaccount.com`
- Cloud SQL: `starquantix-databases:us-central1:rombell`
- Secrets: `DATABASE_URL` from Secret Manager (`SQ_MODELS_DATABASE_URL`)

### 1.4 Daily Scrape (`scrape.yml`)

**Trigger:** Cron 00:00 UTC daily, or manual `workflow_dispatch`

**Steps:** Checkout → Python 3.12 → pip install → `python -m jobs.scrape.run_scrape`  
**Secrets:** `DATABASE_URL`

---

## 2. Environment Variables

| Variable | Used by | Description |
|----------|---------|-------------|
| `DATABASE_URL` | API, Scrape, CI | PostgreSQL connection string |
| `NEXT_PUBLIC_API_URL` | Web (build-time) | API base URL for frontend |
| `PORT` | API | Server port (default 8080) |
| `LOG_LEVEL` | API | Logging level |
| `API_CORS_ORIGINS` | API | CORS allowed origins |
| `RATE_LIMIT` | API | Rate limit (e.g. `100/minute`) |

---

## 3. Required Secrets (GitHub)

- `GCP_WORKLOAD_IDENTITY_PROVIDER` — Workload Identity
- `GCP_SERVICE_ACCOUNT` — Service account for deploy
- `NEXT_PUBLIC_API_URL` — Production API URL (Web deploy)
- `DATABASE_URL` — Production DB (Scrape job)

---

## 4. GCP Resources

- **Artifact Registry:** `us-central1-docker.pkg.dev/sq-websites/cloudrun`
- **Cloud Run:** `ai-models-web`, `ai-models-api`
- **Cloud SQL:** `rombell` instance
- **Secret Manager:** `SQ_MODELS_DATABASE_URL`
