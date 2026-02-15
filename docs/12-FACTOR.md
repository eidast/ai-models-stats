# 12-Factor App — AI Models Stats

All applications (API, Web, Scrape Job) follow the [12-Factor App](https://12factor.net/) methodology for cloud-native development.

---

## 1. Codebase

One monorepo (`ai-models-stats`) tracked in git. Multiple apps share the same codebase.

---

## 2. Dependencies

- **API (Python):** `requirements.txt` with pinned versions; `pip install -r requirements.txt`
- **Web (Node):** `package.json` with lockfile (`pnpm-lock.yaml`)
- Explicitly declare and isolate dependencies; no implicit system-wide packages

---

## 3. Config

**All config via environment variables.** No credentials or environment-specific values in code.

| Variable | App | Required | Description |
|----------|-----|----------|-------------|
| `DATABASE_URL` | API, Scrape | Yes | PostgreSQL connection string |
| `DATABASE_USER` | API, Scrape | Alt | DB user (if not in URL) |
| `DATABASE_PASSWORD` | API, Scrape | Alt | DB password (if not in URL) |
| `DATABASE_HOST` | API, Scrape | Alt | DB host |
| `DATABASE_PORT` | API, Scrape | Alt | DB port (default 5432) |
| `DATABASE_NAME` | API, Scrape | Alt | DB name |
| `API_CORS_ORIGINS` | API | No | Allowed origins (default `*` for public) |
| `RATE_LIMIT` | API | No | Rate limit (e.g. `100/minute`). Empty to disable |
| `LOG_LEVEL` | API, Scrape | No | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `PORT` | API, Web | No | Server port (Cloud Run sets automatically) |
| `NEXT_PUBLIC_API_URL` | Web | No | API base URL for client fetches |

**Connection string format:** `postgresql://user:password@host:port/dbname`

Example `.env` (never commit):
```
DATABASE_URL=postgresql://user:password@localhost:5432/ai_models_stats
LOG_LEVEL=INFO
```

---

## 4. Backing Services

PostgreSQL is a **backing service** — attached resource, interchangeable. Same `DATABASE_URL` works locally and in Cloud Run (swap connection string per environment).

---

## 5. Build, Release, Run

Strict separation:

1. **Build:** `pnpm build` (web), `pip install` (api) — produces artifacts
2. **Release:** Docker image + config (env vars) — immutable release
3. **Run:** Start process; no code changes at runtime

---

## 6. Processes

Stateless processes. No in-memory state; all persistent data in PostgreSQL. Scale horizontally.

---

## 7. Port Binding

Apps are self-contained and export HTTP via port binding. Port from `PORT` env var (Cloud Run injects).

---

## 8. Concurrency

Scale out via process model. Cloud Run handles concurrency; API and Web scale independently.

---

## 9. Disposability

Fast startup, graceful shutdown. API: respond to SIGTERM, finish in-flight requests. Scrape job: idempotent; safe to kill and restart.

---

## 10. Dev/Prod Parity

Same backing services (PostgreSQL) in all environments. Use different `DATABASE_URL` per env. Avoid drift via Docker Compose for local dev.

---

## 11. Logs

Treat logs as event streams. Write to stdout/stderr. No log files. Cloud Run captures and routes to Cloud Logging.

---

## 12. Admin Processes

Scrape job runs as one-off process (Cloud Run Job). Same codebase, same env vars, run via `python -m jobs.scrape`.
