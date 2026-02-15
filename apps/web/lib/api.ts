const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080";

export interface Model {
  id: string;
  providerId: string;
  name: string;
  apiId?: string;
  type: string;
  modalities: string[];
  capabilities: string[];
  contextLength?: number;
  maxOutputTokens?: number;
  deprecated: boolean;
  deprecationDate?: string;
  pricing: {
    inputPerMillionTokens?: number;
    outputPerMillionTokens?: number;
    cacheInputPerMillionTokens?: number;
    [key: string]: number | string | undefined;
  };
  selfHosted?: unknown;
  sourceUrl: string;
  lastUpdated: string;
}

export interface Provider {
  id: string;
  name: string;
  pricingUrl: string;
  apiDocsUrl?: string;
  lastUpdated: string;
}

async function apiFetch(url: string): Promise<Response> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 5000);
  try {
    return await fetch(url, {
      next: { revalidate: 60 },
      signal: controller.signal,
    });
  } finally {
    clearTimeout(timeout);
  }
}

export type SortBy = "input" | "output" | "cache" | "context" | "name" | "provider";
export type SortOrder = "asc" | "desc";

export async function fetchModels(params?: {
  provider?: string;
  capability?: string;
  type?: string;
  includeDeprecated?: boolean;
  sortBy?: SortBy;
  sortOrder?: SortOrder;
}): Promise<Model[]> {
  const search = new URLSearchParams();
  if (params?.provider) search.set("provider", params.provider);
  if (params?.capability) search.set("capability", params.capability);
  if (params?.type) search.set("type", params.type);
  if (params?.includeDeprecated) search.set("include_deprecated", "true");
  if (params?.sortBy) search.set("sort_by", params.sortBy);
  if (params?.sortOrder) search.set("sort_order", params.sortOrder);
  const res = await apiFetch(`${API_URL}/api/models?${search}`);
  if (!res.ok) throw new Error("Failed to fetch models");
  return res.json();
}

export async function fetchModel(id: string): Promise<Model | null> {
  const res = await apiFetch(`${API_URL}/api/models/${id}`);
  if (res.status === 404) return null;
  if (!res.ok) throw new Error("Failed to fetch model");
  return res.json();
}

export async function fetchProviders(): Promise<Provider[]> {
  const res = await apiFetch(`${API_URL}/api/providers`);
  if (!res.ok) throw new Error("Failed to fetch providers");
  return res.json();
}

export async function fetchCompare(ids: string[]): Promise<{ models: Model[] }> {
  const res = await apiFetch(`${API_URL}/api/compare?ids=${ids.join(",")}`);
  if (!res.ok) throw new Error("Failed to fetch comparison");
  return res.json();
}
