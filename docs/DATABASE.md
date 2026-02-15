# PostgreSQL Schema — AI Models Stats

**Database:** PostgreSQL 15+  
**Connection:** Via `DATABASE_URL` environment variable (12-factor config)

---

## Connection

```
DATABASE_URL=postgresql://user:password@host:port/dbname
```

All credentials from environment; never hardcoded.

---

## Tables

### providers

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(50) | PK | Unique slug (e.g., `openai`) |
| name | VARCHAR(255) | NOT NULL | Display name |
| pricing_url | VARCHAR(500) | NOT NULL | Source URL for pricing |
| api_docs_url | VARCHAR(500) | | API documentation URL |
| last_updated | TIMESTAMPTZ | NOT NULL | Last successful scrape |

### models

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(100) | PK | `{provider_id}-{model_slug}` |
| provider_id | VARCHAR(50) | FK → providers(id) | Provider reference |
| name | VARCHAR(255) | NOT NULL | Display name |
| api_id | VARCHAR(100) | | API model identifier |
| type | VARCHAR(50) | NOT NULL | `text`, `image`, `audio`, `video`, `embedding`, `multimodal` |
| modalities | TEXT[] | NOT NULL | `{text}`, `{text,image}` |
| capabilities | TEXT[] | NOT NULL | Capability cluster IDs |
| context_length | INTEGER | | Max context tokens |
| max_output_tokens | INTEGER | | Max output tokens |
| deprecated | BOOLEAN | NOT NULL DEFAULT false | EOL flag |
| deprecation_date | DATE | | When model goes EOL |
| pricing | JSONB | NOT NULL | Pricing object (see below) |
| self_hosted | JSONB | | For OSS models |
| source_url | VARCHAR(500) | NOT NULL | URL where data was extracted |
| last_updated | TIMESTAMPTZ | NOT NULL | Last update |

**Indexes:**
- `idx_models_provider_id` ON (provider_id)
- `idx_models_type` ON (type)
- `idx_models_deprecated` ON (deprecated)
- `idx_models_capabilities` ON USING GIN (capabilities)

### price_history (optional — for future)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | BIGSERIAL | PK | Auto-increment |
| model_id | VARCHAR(100) | FK → models(id) | Model reference |
| date | DATE | NOT NULL | Snapshot date |
| pricing | JSONB | NOT NULL | Pricing snapshot |
| source | VARCHAR(50) | | `scrape` or `api` |
| created_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | Insert timestamp |

**Index:** `idx_price_history_model_date` ON (model_id, date)

---

## JSONB: pricing

```json
{
  "tier": "standard",
  "inputPerMillionTokens": 0.25,
  "outputPerMillionTokens": 2.0,
  "cacheInputPerMillionTokens": 0.025,
  "batchInputPerMillionTokens": 0.125,
  "batchOutputPerMillionTokens": 1.0,
  "imageInputPerImage": null,
  "imageOutputPerImage": 0.04,
  "audioInputPerMillionTokens": null,
  "audioOutputPerMillionTokens": 12.0,
  "videoPerSecond": 0.15,
  "freeTierInputPerMillionTokens": null,
  "freeTierOutputPerMillionTokens": null,
  "notes": "Batch API: 50% discount"
}
```

---

## JSONB: self_hosted

```json
{
  "minRamGb": 16,
  "minVramGb": 8,
  "recommendedGpu": "NVIDIA RTX 4080",
  "runsOn": ["m4-mac-mini", "gaming-pc", "cloud-gpu"],
  "quantization": ["fp16", "int8", "int4"],
  "notes": "M4 Mac Mini 16GB can run 7B at int4"
}
```

---

## Migrations

Migrations live in `apps/api/migrations/` (e.g., Alembic or raw SQL). Version-controlled; applied at deploy.

```
migrations/
├── 001_create_providers.sql
├── 002_create_models.sql
└── 003_create_price_history.sql
```

---

## Scraper → Database

Scrape job:
1. Connects via `DATABASE_URL`
2. Runs scrapers
3. Validates output against schema
4. **Upserts** into `providers` and `models` (by `id`)
5. Optionally appends to `price_history` for historical tracking
