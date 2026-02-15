# Anthropic (Claude) Pricing — Page Structure & Models

**Purpose:** Document Anthropic's Claude model pricing for scraper reference.

**Source:** [https://platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing)

**Alternative:** [https://claude.com/pricing](https://claude.com/pricing)

---

## Model Pricing (per 1M tokens, USD)

| Model | Base Input | Cache (5m write) | Cache (1h write) | Cache Read | Output |
|-------|------------|------------------|------------------|------------|--------|
| Claude Opus 4.6 | $5 | $6.25 | $10 | $0.50 | $25 |
| Claude Opus 4.5 | $5 | $6.25 | $10 | $0.50 | $25 |
| Claude Opus 4.1 | $15 | $18.75 | $30 | $1.50 | $75 |
| Claude Opus 4 | $15 | $18.75 | $30 | $1.50 | $75 |
| Claude Sonnet 4.5 | $3 | $3.75 | $6 | $0.30 | $15 |
| Claude Sonnet 4 | $3 | $3.75 | $6 | $0.30 | $15 |
| Claude Sonnet 3.7 | $3 | $3.75 | $6 | $0.30 | $15 |
| Claude Haiku 4.5 | $1 | $1.25 | $2 | $0.10 | $5 |
| Claude Haiku 3.5 | $0.80 | $1 | $1.6 | $0.08 | $4 |
| Claude Opus 3 | $15 | $18.75 | $30 | $1.50 | $75 |
| Claude Haiku 3 | $0.25 | $0.30 | $0.50 | $0.03 | $1.25 |

**Cache multipliers:**
- 5-min cache write: 1.25× base input
- 1-hour cache write: 2× base input
- Cache read: 0.1× base input

---

## Batch API (50% discount)

| Model | Batch Input | Batch Output |
|-------|-------------|--------------|
| Opus 4.6/4.5 | $2.50 | $12.50 |
| Opus 4.1/4/3 | $7.50 | $37.50 |
| Sonnet 4.5/4/3.7 | $1.50 | $7.50 |
| Haiku 4.5 | $0.50 | $2.50 |
| Haiku 3.5 | $0.40 | $2 |
| Haiku 3 | $0.125 | $0.625 |

---

## Long Context (1M tokens)

For Opus 4.6, Sonnet 4.5, Sonnet 4 with >200K input tokens:
- Opus 4.6: $10 input, $37.50 output
- Sonnet 4.5/4: $6 input, $22.50 output

---

## Deprecated Models

- Claude Sonnet 3.7
- Claude Opus 3

---

## Third-Party Platforms

Claude also available on:
- [AWS Bedrock](https://aws.amazon.com/bedrock/pricing/)
- [Google Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/pricing)
- [Microsoft Foundry](https://azure.microsoft.com/en-us/pricing/details/ai-foundry/#pricing)
