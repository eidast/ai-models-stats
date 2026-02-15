/**
 * Shared types for AI Models Stats — aligned with SCHEMA.md
 */

export interface Pricing {
  tier?: "standard" | "batch" | "free";
  inputPerMillionTokens?: number;
  outputPerMillionTokens?: number;
  cacheInputPerMillionTokens?: number;
  batchInputPerMillionTokens?: number;
  batchOutputPerMillionTokens?: number;
  imageInputPerImage?: number;
  imageOutputPerImage?: number;
  audioInputPerMillionTokens?: number;
  audioOutputPerMillionTokens?: number;
  videoPerSecond?: number;
  freeTierInputPerMillionTokens?: number;
  freeTierOutputPerMillionTokens?: number;
  notes?: string;
}

export interface SelfHosted {
  minRamGb?: number;
  minVramGb?: number;
  recommendedGpu?: string;
  runsOn?: string[];
  quantization?: string[];
  notes?: string;
}

export interface Provider {
  id: string;
  name: string;
  pricingUrl: string;
  apiDocsUrl?: string;
  lastUpdated: string;
}

export type ModelType =
  | "text"
  | "image"
  | "audio"
  | "video"
  | "embedding"
  | "multimodal";

export interface Model {
  id: string;
  providerId: string;
  name: string;
  apiId?: string;
  type: ModelType;
  modalities: string[];
  capabilities: string[];
  contextLength?: number;
  maxOutputTokens?: number;
  deprecated: boolean;
  deprecationDate?: string;
  pricing: Pricing;
  selfHosted?: SelfHosted | null;
  sourceUrl: string;
  lastUpdated: string;
}

export interface PriceHistory {
  modelId: string;
  date: string;
  pricing: Pricing;
  source?: "scrape" | "api";
}

/** Reference tasks for cost estimation */
export const TASK_COSTS = {
  summarize_1k: { inputTokens: 1500, outputTokens: 200 },
  summarize_10k: { inputTokens: 15000, outputTokens: 500 },
  translate_500: { inputTokens: 750, outputTokens: 750 },
  code_review: { inputTokens: 500, outputTokens: 300 },
} as const;

export type TaskId = keyof typeof TASK_COSTS;
