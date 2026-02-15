# OpenAI Pricing — Page Structure & Data Sources

**Purpose:** Document the structure of OpenAI's pricing pages for scraper implementation and reference.

**Primary source:** [https://developers.openai.com/api/docs/pricing](https://developers.openai.com/api/docs/pricing)

**Alternative:** [https://openai.com/api/pricing/](https://openai.com/api/pricing/) (marketing site, may differ)

---

## Page Sections

The developers pricing page is organized into the following sections:

### 1. Text tokens (per 1M tokens)

Four tiers: **Batch**, **Flex**, **Standard**, **Priority**

| Tier | Use case |
|------|----------|
| Batch | Non-time-sensitive; 50% discount |
| Flex | Lower price, higher latency |
| Standard | Default API tier |
| Priority | Faster processing |

**Models (Standard tier):** gpt-5.2, gpt-5.1, gpt-5, gpt-5-mini, gpt-5-nano, gpt-5.2-pro, gpt-5-pro, gpt-4.1, gpt-4.1-mini, gpt-4.1-nano, gpt-4o, gpt-4o-mini, o1, o1-pro, o3-pro, o3, o4-mini, o3-mini, o1-mini, gpt-image-1.5, chatgpt-image-latest, gpt-image-1, gpt-image-1-mini, gpt-realtime, gpt-realtime-mini, gpt-audio, gpt-audio-mini, computer-use-preview, codex variants, etc.

**Columns:** Input | Cached input | Output

---

### 2. Image tokens (per 1M tokens)

For vision models that process images. Tiers: **Batch**, **Standard**

**Models:** gpt-image-1.5, chatgpt-image-latest, gpt-image-1, gpt-image-1-mini, gpt-realtime, gpt-realtime-mini

---

### 3. Audio tokens (per 1M tokens)

**Models:** gpt-realtime, gpt-realtime-mini, gpt-4o-realtime-preview, gpt-4o-mini-realtime-preview, gpt-audio, gpt-audio-mini, gpt-4o-audio-preview, gpt-4o-mini-audio-preview

**Columns:** Input | Cached Input | Output

---

### 4. Video (per second)

| Model | Resolution | Price/sec |
|-------|------------|-----------|
| sora-2 | 720x1280 (portrait/landscape) | $0.10 |
| sora-2-pro | 720x1280 | $0.30 |
| sora-2-pro | 1024x1792 / 1792x1024 | $0.50 |

---

### 5. Fine-tuning (per 1M tokens)

**Models:** o4-mini, gpt-4.1, gpt-4.1-mini, gpt-4.1-nano, gpt-4o, gpt-4o-mini, gpt-3.5-turbo, davinci-002, babbage-002

**Columns:** Training | Input | Cached Input | Output

---

### 6. Built-in tools

- **Container usage** (Code Interpreter, Shell): per container, by memory tier (1/4/16/64 GB)
- **File search storage:** $0.10 / GB-day (1GB free)
- **File search tool call:** $2.50 / 1k calls (Responses API)
- **Web search:** $10–25 / 1k calls + token costs

---

### 7. Transcription and speech

- **gpt-4o-mini-tts:** Text in $0.60/1M, Audio out $12/1M
- **gpt-4o-transcribe / diarize:** $2.50 in, $10 out (text); $6 in (audio)
- **gpt-4o-mini-transcribe:** $1.25 in, $5 out
- **Whisper:** $0.006 / minute
- **TTS:** $15 / 1M chars; **TTS HD:** $30 / 1M chars

---

### 8. Image generation (per image)

| Model | Quality | 1024×1024 | 1024×1536 | 1536×1024 |
|-------|---------|------------|-----------|------------|
| GPT Image 1.5 | Low/Med/High | $0.009–0.133 | $0.013–0.2 | $0.013–0.2 |
| GPT Image 1 | Low/Med/High | $0.011–0.167 | ... | ... |
| GPT Image 1 Mini | Low/Med/High | $0.005–0.036 | ... | ... |

| Model | Quality | 1024×1024 | 1024×1792 | 1792×1024 |
|-------|---------|------------|-----------|------------|
| DALL·E 3 | Standard/HD | $0.04–0.08 | $0.08–0.12 | $0.08–0.12 |

| Model | 256×256 | 512×512 | 1024×1024 |
|-------|---------|---------|-----------|
| DALL·E 2 | $0.016 | $0.018 | $0.02 |

---

### 9. Embeddings (per 1M tokens)

| Model | Cost | Batch cost |
|-------|------|------------|
| text-embedding-3-small | $0.02 | $0.01 |
| text-embedding-3-large | $0.13 | $0.065 |
| text-embedding-ada-002 | $0.10 | $0.05 |

---

### 10. Moderation

`omni-moderation` models: **free**

---

### 11. Legacy models

gpt-4-turbo, gpt-4-0125-preview, gpt-4o-2024-05-13, gpt-3.5-turbo variants, davinci-002, babbage-002, etc.

---

## Scraper Notes

- **developers.openai.com** is the canonical API docs; structure may be JS-rendered.
- **Tiers:** Store Standard as primary; add `batchInputPerMillionTokens` / `batchOutputPerMillionTokens` when available.
- **Video:** Use `videoPerSecond` in pricing.
- **Image gen:** Use `imageOutputPerImage` (e.g. 1024×1024 Standard).
- **Embeddings:** Single `inputPerMillionTokens` (no output).
- **Deprecated:** Mark `gpt-4o-2024-05-13`, legacy models with `deprecated: true` when appropriate.
