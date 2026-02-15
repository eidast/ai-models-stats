# Mistral AI Pricing — Page Structure & Models

**Purpose:** Document Mistral's model ecosystem and pricing for scraper reference.

**Sources:**
- [https://mistral.ai/pricing#api](https://mistral.ai/pricing#api) — main pricing (API section)
- [https://docs.mistral.ai/deployment/ai-studio/pricing](https://docs.mistral.ai/deployment/ai-studio/pricing) — redirects to main
- [pricepertoken.com](https://pricepertoken.com/pricing-page/provider/mistral-ai) — aggregated reference (27 models, Feb 2026)

---

## Model Ecosystem (27 models)

### Budget / Entry
| Model | Input $/M | Output $/M | Context |
|-------|-----------|------------|---------|
| Mistral Nemo | 0.02 | 0.04 | 131K |
| Mistral Small 3.1 24B | 0.03 | 0.11 | 131K |
| Devstral 2 | 0.05 | 0.22 | 262K |
| Mistral Small 3 | 0.05 | 0.08 | 32K |
| Mistral Small 3.2 24B | 0.06 | 0.18 | 131K |

### Mid-tier
| Model | Input $/M | Output $/M | Context |
|-------|-----------|------------|---------|
| Mistral Small Creative | 0.10 | 0.30 | 32K |
| Ministral 3 3B | 0.10 | 0.10 | 131K |
| Voxtral Small 24B | 0.10 | 0.30 | 32K |
| Devstral Small 1.1 | 0.10 | 0.30 | 131K |
| Ministral 3 8B | 0.15 | 0.15 | 262K |
| Ministral 3 14B | 0.20 | 0.20 | 262K |
| Saba | 0.20 | 0.60 | 32K |
| Mistral 7B Instruct | 0.20 | 0.20 | 32K |
| Codestral 2508 | 0.30 | 0.90 | 256K |

### Premium
| Model | Input $/M | Output $/M | Context |
|-------|-----------|------------|---------|
| Mistral Medium 3 / 3.1 | 0.40 | 2.00 | 131K |
| Devstral Medium | 0.40 | 2.00 | 131K |
| Mistral Large 3 | 0.50 | 1.50 | 262K |
| Mixtral 8x7B | 0.54 | 0.54 | 32K |
| Mistral Large 24-11 / 24-07 | 2.00 | 6.00 | 131K |
| Pixtral Large (vision) | 2.00 | 6.00 | 131K |
| Mixtral 8x22B | 2.00 | 6.00 | 65K |
| Mistral Large | 2.00 | 6.00 | 128K |

### Specialized
- **Devstral** — coding-focused
- **Codestral** — coding
- **Pixtral** — vision (multimodal)
- **Voxtral** — audio
- **Ministral** — small efficient models
- **Saba** — general purpose

---

## Cache pricing (where available)

- Mistral Small 3.1 24B: $0.015/M cache read
- Mistral Small 3.2 24B: $0.03/M cache read
- Devstral 2: $0.025/M cache read

---

## Notes

- Some models use tiered pricing by prompt length; displayed prices for prompts ≤200K tokens.
- Codestral, Devstral: coding-optimized.
- Pixtral: vision/multimodal (text + image).
