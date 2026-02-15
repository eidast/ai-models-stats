# Product Requirements Document (PRD)
## AI Models Stats — LLM Comparison Reference Site

**Version:** 1.0  
**Last Updated:** 2025-02-14  
**Status:** Draft

---

## 1. Executive Summary

AI Models Stats is a public reference website that enables users to quickly compare LLM models across providers. The primary value proposition is **cost transparency** and **capability clustering** — helping users identify which models are best suited for specific tasks (summarization, coding, image generation, etc.) and at what price.

---

## 2. Problem Statement

- **Cost opacity:** Pricing structures vary widely across providers (per token, per image, per second of video, cache tiers, batch discounts). Users struggle to compare apples-to-apples.
- **Capability discovery:** No single place to filter models by functionality (e.g., "models good for RAG" or "models that generate images").
- **Information fragmentation:** Prices and capabilities are scattered across multiple provider sites, often changing frequently.
- **Deprecation visibility:** Models going out of support are not clearly flagged, leading to unexpected migration needs.

---

## 3. Goals & Success Metrics

| Goal | Success Metric |
|------|----------------|
| Cost comparison | Users can compare input/output prices per 1M tokens across models in < 30 seconds |
| Capability filtering | Users can filter by at least 5 functionality clusters |
| Data freshness | Prices updated at least daily |
| Accessibility | Site available in English and Spanish |
| Usability | No login required; favorites via localStorage |

---

## 4. User Personas

**Primary:** General public — developers, product managers, researchers, and anyone evaluating LLM options for projects or learning.

**Needs:**
- Quick cost lookup
- Side-by-side model comparison
- Filter by use case (coding, summaries, RAG, etc.)
- Save favorite models locally
- Bilingual support (EN/ES)

---

## 5. Functional Requirements

### 5.1 Core Features

| ID | Feature | Description | Priority |
|----|---------|-------------|----------|
| F1 | Model catalog | Display all models with provider, name, type (text, image, audio, video) | P0 |
| F2 | Price comparison | Show input/output price per 1M tokens (USD), cache pricing when applicable | P0 |
| F3 | Task cost table | Estimated cost for common tasks (e.g., summarize 1K words, translate 500 words) | P0 |
| F4 | Capability clustering | Filter/group by: document analysis, summaries, RAG, translation, story generation, coding, image gen, audio gen | P0 |
| F5 | Limits & capabilities | Context length, max output, rate limits, multimodal support | P1 |
| F6 | Deprecation flag | Mark models going out of support; exclude from default ranking | P1 |
| F7 | Favorites (localStorage) | Save favorite models; persist across sessions | P1 |
| F8 | Open-source self-hosted | Include OSS models with hardware requirements (e.g., M4 Mac Mini, Gaming PC) | P2 |

### 5.2 Data Collection

| ID | Requirement | Description |
|----|-------------|-------------|
| D1 | Update frequency | Job runs every 24 hours |
| D2 | Source priority | Prefer official APIs for pricing; fallback to web scraping |
| D3 | Deprecation handling | Detect EOL announcements; remove or flag models accordingly |
| D4 | Price history | Store for historical purposes only; no UI feature in v1 |

### 5.3 Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NF1 | i18n: English and Spanish |
| NF2 | No authentication |
| NF3 | Responsive design (mobile-friendly) |
| NF4 | Deploy on GCP Cloud Run |
| NF5 | Monorepo with pnpm workspaces |

---

## 6. Out of Scope (v1)

- User accounts / authentication
- Price history visualization
- PWA / offline mode
- Multi-currency (USD only)
- Benchmark scores (future phase; use public benchmarks when available)

---

## 7. Data Sources (Initial)

| Provider | URL | Type |
|----------|-----|------|
| Mistral | https://mistral.ai/pricing#api | Scraping |
| OpenAI | https://openai.com/es-419/api/pricing/ | Scraping |
| Google (Gemini) | https://ai.google.dev/gemini-api/docs/pricing?hl=es-419 | Scraping |
| DeepSeek | https://api-docs.deepseek.com/quick_start/pricing | Scraping / API if available |

**Planned providers:** Anthropic, Meta, Cohere, Amazon Bedrock, Azure OpenAI.

---

## 8. Capability Clusters

Models will be tagged with one or more of:

| Cluster | Description |
|---------|-------------|
| Document analysis | Parse, extract, understand documents |
| Document summaries | Summarize long documents |
| RAG | Retrieval-augmented generation, embeddings |
| Translation | Multilingual translation |
| Story generation | Creative writing, long-form content |
| Coding | Code generation, completion, debugging |
| Image generation | Text-to-image, image editing |
| Audio generation | TTS, speech synthesis |
| Video generation | Text-to-video |

**Source for tagging:** Public benchmarks + provider documentation.

---

## 9. Tech Stack Summary

| Layer | Technology |
|-------|------------|
| Frontend | Next.js (App Router) |
| Backend (API + scraping) | FastAPI (Python) |
| Monorepo | pnpm workspaces |
| Deployment | GCP Cloud Run |
| Data storage | TBD (PostgreSQL / Firestore / JSON files) |

---

## 10. Open Questions

- [ ] Exact storage choice (DB vs file-based) for scraped data
- [ ] Benchmark data sources for capability tagging
- [ ] API availability for each provider (to prioritize over scraping)
