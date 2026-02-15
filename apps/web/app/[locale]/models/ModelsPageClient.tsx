"use client";

import { useTranslations } from "next-intl";
import { useCallback, useEffect, useState } from "react";
import { Link } from "@/i18n/routing";
import type { Model, Provider } from "@/lib/api";
import { fetchModels } from "@/lib/api";
import { getFavorites, toggleFavorite } from "@/lib/favorites";
import { TaskCostTable } from "@/components/TaskCostTable";

const CAPABILITIES = [
  "coding",
  "document_summaries",
  "document_analysis",
  "rag",
  "translation",
  "story_generation",
  "image_generation",
  "audio_generation",
  "video_generation",
];

function formatPrice(n: number | undefined): string {
  if (n == null) return "—";
  return `$${n.toFixed(2)}`;
}

export function ModelsPageClient({
  initialModels,
  providers,
}: {
  initialModels: Model[];
  providers: Provider[];
}) {
  const t = useTranslations("models");
  const [models, setModels] = useState(initialModels);
  const [favorites, setFavorites] = useState<string[]>([]);
  const [provider, setProvider] = useState<string>("");
  const [capability, setCapability] = useState<string>("");
  const [modelType, setModelType] = useState<string>("");
  const [includeDeprecated, setIncludeDeprecated] = useState(false);
  const [loading, setLoading] = useState(false);
  const [showFavoritesOnly, setShowFavoritesOnly] = useState(false);
  const [sortBy, setSortBy] = useState<"input" | "output" | "cache" | "context" | "name" | "provider">("provider");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc");

  useEffect(() => {
    setFavorites(getFavorites());
  }, []);

  useEffect(() => {
    setLoading(true);
    fetchModels({
      provider: provider || undefined,
      capability: capability || undefined,
      type: modelType || undefined,
      includeDeprecated,
      sortBy,
      sortOrder,
    })
      .then(setModels)
      .finally(() => setLoading(false));
  }, [provider, capability, modelType, includeDeprecated, sortBy, sortOrder]);

  const handleSort = (column: "input" | "output" | "cache" | "context" | "name" | "provider") => {
    if (sortBy === column) {
      setSortOrder((o) => (o === "asc" ? "desc" : "asc"));
    } else {
      setSortBy(column);
      setSortOrder("asc");
    }
  };

  const SortIcon = ({ col }: { col: "input" | "output" | "cache" | "context" | "name" | "provider" }) => {
    if (sortBy !== col) return <span className="opacity-40">↕</span>;
    return <span>{sortOrder === "asc" ? "↑" : "↓"}</span>;
  };

  const handleToggleFavorite = useCallback((id: string) => {
    setFavorites((prev) => toggleFavorite(id));
  }, []);

  const displayedModels = showFavoritesOnly
    ? models.filter((m) => favorites.includes(m.id))
    : models;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6 text-white">{t("title")}</h1>

      {/* Filters */}
      <div className="flex flex-wrap gap-4 mb-6 p-4 bg-starquantix-navy-light rounded-lg border border-starquantix-navy-lighter">
        <select
          value={provider}
          onChange={(e) => setProvider(e.target.value)}
          className="bg-starquantix-navy border border-starquantix-navy-lighter rounded px-3 py-2 text-sm text-white"
        >
          <option value="">{t("filterProvider")} — All</option>
          {providers.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name}
            </option>
          ))}
        </select>
        <select
          value={capability}
          onChange={(e) => setCapability(e.target.value)}
          className="bg-starquantix-navy border border-starquantix-navy-lighter rounded px-3 py-2 text-sm text-white"
        >
          <option value="">{t("filterCapability")} — All</option>
          {CAPABILITIES.map((c) => (
            <option key={c} value={c}>
              {c.replace(/_/g, " ")}
            </option>
          ))}
        </select>
        <select
          value={modelType}
          onChange={(e) => setModelType(e.target.value)}
          className="bg-starquantix-navy border border-starquantix-navy-lighter rounded px-3 py-2 text-sm text-white"
        >
          <option value="">{t("filterType")} — All</option>
          <option value="text">text</option>
          <option value="multimodal">multimodal</option>
          <option value="image">image</option>
          <option value="audio">audio</option>
          <option value="video">video</option>
          <option value="embedding">embedding</option>
        </select>
        <label className="flex items-center gap-2 text-sm text-slate-200">
          <input
            type="checkbox"
            checked={includeDeprecated}
            onChange={(e) => setIncludeDeprecated(e.target.checked)}
            className="rounded"
          />
          {t("includeDeprecated")}
        </label>
        <label className="flex items-center gap-2 text-sm text-slate-200">
          <input
            type="checkbox"
            checked={showFavoritesOnly}
            onChange={(e) => setShowFavoritesOnly(e.target.checked)}
            className="rounded"
          />
          {t("favorites")}
        </label>
      </div>

      {loading ? (
        <p className="text-slate-300">Loading...</p>
      ) : (
        <>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-starquantix-navy-lighter">
                  <th className="text-left py-3 px-2 text-slate-200"></th>
                  <th
                    className="text-left py-3 px-2 text-slate-200 cursor-pointer hover:text-white select-none"
                    onClick={() => handleSort("name")}
                  >
                    Model <SortIcon col="name" />
                  </th>
                  <th
                    className="text-left py-3 px-2 text-slate-200 cursor-pointer hover:text-white select-none"
                    onClick={() => handleSort("provider")}
                  >
                    Provider <SortIcon col="provider" />
                  </th>
                  <th className="text-left py-3 px-2 text-slate-200">Type</th>
                  <th
                    className="text-right py-3 px-2 text-slate-200 cursor-pointer hover:text-white select-none"
                    onClick={() => handleSort("input")}
                  >
                    {t("inputPerM")} <SortIcon col="input" />
                  </th>
                  <th
                    className="text-right py-3 px-2 text-slate-200 cursor-pointer hover:text-white select-none"
                    onClick={() => handleSort("output")}
                  >
                    {t("outputPerM")} <SortIcon col="output" />
                  </th>
                  <th
                    className="text-right py-3 px-2 text-slate-200 cursor-pointer hover:text-white select-none"
                    onClick={() => handleSort("cache")}
                  >
                    {t("cachePerM")} <SortIcon col="cache" />
                  </th>
                  <th
                    className="text-right py-3 px-2 text-slate-200 cursor-pointer hover:text-white select-none"
                    onClick={() => handleSort("context")}
                  >
                    {t("context")} <SortIcon col="context" />
                  </th>
                  <th className="text-left py-3 px-2 text-slate-200"></th>
                </tr>
              </thead>
              <tbody>
                {displayedModels.map((m) => (
                  <tr key={m.id} className="border-b border-starquantix-navy-lighter hover:bg-starquantix-navy-light/50">
                    <td className="py-3 px-2">
                      <button
                        onClick={() => handleToggleFavorite(m.id)}
                        className="text-lg text-amber-400"
                        aria-label="Toggle favorite"
                      >
                        {favorites.includes(m.id) ? "★" : "☆"}
                      </button>
                    </td>
                    <td className="py-3 px-2">
                      <Link href={`/models/${m.id}`} className="text-starquantix-blue-light hover:underline font-medium">
                        {m.name}
                      </Link>
                      {m.deprecated && (
                        <span className="ml-2 text-xs bg-amber-900/50 text-amber-400 px-1.5 py-0.5 rounded">
                          {t("deprecated")}
                        </span>
                      )}
                    </td>
                    <td className="py-3 px-2 text-slate-300">{m.providerId}</td>
                    <td className="py-3 px-2 text-slate-300">{m.type}</td>
                    <td className="py-3 px-2 text-right font-mono text-slate-200">
                      {formatPrice(m.pricing.inputPerMillionTokens)}
                    </td>
                    <td className="py-3 px-2 text-right font-mono text-slate-200">
                      {formatPrice(m.pricing.outputPerMillionTokens)}
                    </td>
                    <td className="py-3 px-2 text-right font-mono text-slate-200">
                      {formatPrice(m.pricing.cacheInputPerMillionTokens)}
                    </td>
                    <td className="py-3 px-2 text-right text-slate-200">
                      {m.contextLength ? (m.contextLength / 1000).toFixed(0) + "K" : "—"}
                    </td>
                    <td className="py-3 px-2">
                      <Link
                        href={`/compare?ids=${m.id}`}
                        className="text-starquantix-blue-light hover:underline text-xs"
                      >
                        {t("compare")}
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {displayedModels.length > 0 && (
            <div className="mt-8">
              <TaskCostTable models={displayedModels.slice(0, 10)} />
            </div>
          )}
        </>
      )}
    </div>
  );
}
