# Data Schema — AI Models Stats

**Purpose:** Standard schema for all scraped/ingested model data. Any data capture service (scrapers, API clients) must output data conforming to this schema.

---

## 1. Provider

```json
{
  "id": "openai",
  "name": "OpenAI",
  "pricingUrl": "https://openai.com/api/pricing/",
  "apiDocsUrl": "https://platform.openai.com/docs",
  "lastUpdated": "2025-02-14T00:00:00Z"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | Unique slug (lowercase, alphanumeric) |
| name | string | Yes | Display name |
| pricingUrl | string | Yes | Source URL for pricing |
| apiDocsUrl | string | No | API documentation URL |
| lastUpdated | ISO8601 | Yes | Last successful scrape/API fetch |

---

## 2. Model

```json
{
  "id": "openai-gpt-5-mini",
  "providerId": "openai",
  "name": "GPT-5 mini",
  "apiId": "gpt-5-mini",
  "type": "text",
  "modalities": ["text"],
  "capabilities": ["coding", "summaries", "translation"],
  "contextLength": 128000,
  "maxOutputTokens": 16384,
  "deprecated": false,
  "deprecationDate": null,
  "pricing": { ... },
  "selfHosted": null,
  "sourceUrl": "https://openai.com/api/pricing/",
  "lastUpdated": "2025-02-14T00:00:00Z"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | Unique: `{providerId}-{modelSlug}` |
| providerId | string | Yes | FK to Provider |
| name | string | Yes | Display name |
| apiId | string | No | API model identifier (e.g., `gpt-5-mini`) |
| type | enum | Yes | `text`, `image`, `audio`, `video`, `embedding`, `multimodal` |
| modalities | string[] | Yes | `["text"]`, `["text","image"]`, etc. |
| capabilities | string[] | Yes | From capability clusters (see PRD) |
| contextLength | number | No | Max context in tokens |
| maxOutputTokens | number | No | Max output tokens |
| deprecated | boolean | Yes | Default `false` |
| deprecationDate | ISO8601 | No | When model goes EOL |
| pricing | Pricing | Yes | See below |
| selfHosted | SelfHosted | No | For OSS models only |
| sourceUrl | string | Yes | URL where data was extracted |
| lastUpdated | ISO8601 | Yes | Last update timestamp |

---

## 3. Pricing

Supports multiple pricing dimensions. All amounts in **USD**.

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

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| tier | string | No | `standard`, `batch`, `free` — for multi-tier models |
| inputPerMillionTokens | number | No | USD per 1M input tokens |
| outputPerMillionTokens | number | No | USD per 1M output tokens |
| cacheInputPerMillionTokens | number | No | Cached context pricing |
| batchInputPerMillionTokens | number | No | Batch API input |
| batchOutputPerMillionTokens | number | No | Batch API output |
| imageInputPerImage | number | No | USD per image input |
| imageOutputPerImage | number | No | USD per image output |
| audioInputPerMillionTokens | number | No | Audio input |
| audioOutputPerMillionTokens | number | No | Audio output (TTS) |
| videoPerSecond | number | No | USD per second of video |
| freeTierInputPerMillionTokens | number | No | Free tier input |
| freeTierOutputPerMillionTokens | number | No | Free tier output |
| notes | string | No | Clarifications (e.g., "720p/1080p") |

**Rule:** At least one of the `*PerMillionTokens`, `*PerImage`, or `videoPerSecond` must be set.

---

## 4. SelfHosted (Open-Source Models)

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

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| minRamGb | number | No | Minimum system RAM |
| minVramGb | number | No | Minimum GPU VRAM |
| recommendedGpu | string | No | Example GPU |
| runsOn | string[] | No | `m4-mac-mini`, `gaming-pc`, `cloud-gpu`, etc. |
| quantization | string[] | No | Supported precisions |
| notes | string | No | Free-form requirements |

---

## 5. Price History (Optional — for future use)

```json
{
  "modelId": "openai-gpt-5-mini",
  "date": "2025-02-14",
  "inputPerMillionTokens": 0.25,
  "outputPerMillionTokens": 2.0,
  "source": "scrape"
}
```

Stored for historical analysis; no UI in v1.

---

## 6. Capability Clusters (Reference)

| ID | Display (EN) | Display (ES) |
|----|--------------|--------------|
| document_analysis | Document analysis | Análisis de documentos |
| document_summaries | Document summaries | Resúmenes de documentos |
| rag | RAG | RAG |
| translation | Translation | Traducción |
| story_generation | Story generation | Generación de historias |
| coding | Coding | Codificación |
| image_generation | Image generation | Generación de imágenes |
| audio_generation | Audio generation | Generación de audio |
| video_generation | Video generation | Generación de video |

---

## 7. Task Cost Table (Computed / Static)

Reference tasks for cost estimation, **clustered by capability**:

| Cluster | Task ID | Description (EN) | Cost formula |
|---------|---------|------------------|--------------|
| **Text** | summarize_1k | Summarize 1,000 words | input/1M × inPrice + output/1M × outPrice |
| | summarize_10k | Summarize 10,000 words | ~15K in, ~500 out |
| | translate_500 | Translate 500 words | ~750 in, ~750 out |
| | code_review | Code review (100 lines) | ~500 in, ~300 out |
| **Image** | image_1 | Generate 1 image | imageOutputPerImage × 1 |
| **Audio** | tts_1min | TTS 1 minute | audioOutputPerMillionTokens × ~1500/1M |
| | transcribe_1min | Transcribe 1 minute | audioInputPerMillionTokens × ~1500/1M |
| **Video** | video_1sec | Generate 1 sec video | videoPerSecond × 1 |

Tasks are shown only for clusters where at least one model has the matching capability (e.g. `image_generation`, `audio_generation`, `video_generation`).

---

## 8. Output: Scraper → PostgreSQL

Scrapers produce in-memory objects conforming to this schema. The scrape job:

1. Validates output against JSON Schema
2. **Upserts** into PostgreSQL (`providers`, `models` tables)
3. Optionally appends to `price_history` for historical tracking

See [DATABASE.md](DATABASE.md) for PostgreSQL table definitions. The logical schema above maps to:

- `providers` table
- `models` table (with `pricing` and `self_hosted` as JSONB)
