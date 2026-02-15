"use client";

import { useTranslations } from "next-intl";
import { useCallback, useState } from "react";
import { useRouter } from "@/i18n/routing";
import type { Model } from "@/lib/api";
import { TaskCostTable } from "@/components/TaskCostTable";

function formatPrice(n: number | undefined): string {
  if (n == null) return "—";
  return `$${n.toFixed(2)}`;
}

export function ComparePageClient({
  allModels,
  initialSelected,
  compareModels,
}: {
  allModels: Model[];
  initialSelected: string[];
  compareModels: Model[];
}) {
  const t = useTranslations("compare");
  const router = useRouter();
  const [selected, setSelected] = useState<string[]>(initialSelected);

  const addModel = useCallback(
    (id: string) => {
      if (selected.includes(id) || selected.length >= 5) return;
      const next = [...selected, id];
      setSelected(next);
      router.replace(`/compare?ids=${next.join(",")}`);
    },
    [selected, router]
  );

  const removeModel = useCallback(
    (id: string) => {
      const next = selected.filter((x) => x !== id);
      setSelected(next);
      router.replace(next.length ? `/compare?ids=${next.join(",")}` : "/compare");
    },
    [selected, router]
  );

  // Sync with URL - refetch if compareModels is stale
  const models = compareModels.length === selected.length
    ? compareModels
    : allModels.filter((m) => selected.includes(m.id));

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6 text-white">{t("title")}</h1>

      <div className="mb-6">
        <p className="text-slate-300 mb-3">{t("selectModels")}</p>
        <select
          onChange={(e) => {
            const id = e.target.value;
            if (id) addModel(id);
            e.target.value = "";
          }}
          className="bg-starquantix-navy border border-starquantix-navy-lighter rounded px-3 py-2 text-white"
        >
          <option value="">{t("addModel")}</option>
          {allModels
            .filter((m) => !selected.includes(m.id))
            .map((m) => (
              <option key={m.id} value={m.id}>
                {m.name} ({m.providerId})
              </option>
            ))}
        </select>
      </div>

      {models.length > 0 ? (
        <>
          <div className="overflow-x-auto mb-8">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-starquantix-navy-lighter">
                  <th className="text-left py-3 px-2 w-32 text-slate-200">Metric</th>
                  {models.map((m) => (
                    <th key={m.id} className="text-left py-3 px-2 text-slate-200">
                      <div className="flex items-center justify-between">
                        <span>{m.name}</span>
                        <button
                          onClick={() => removeModel(m.id)}
                          className="text-red-400 hover:text-red-300 text-xs"
                        >
                          ×
                        </button>
                      </div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                <tr className="border-b border-starquantix-navy-lighter">
                  <td className="py-2 px-2 text-slate-300">Provider</td>
                  {models.map((m) => (
                    <td key={m.id} className="py-2 px-2 text-slate-200">{m.providerId}</td>
                  ))}
                </tr>
                <tr className="border-b border-starquantix-navy-lighter">
                  <td className="py-2 px-2 text-slate-300">Input / 1M</td>
                  {models.map((m) => (
                    <td key={m.id} className="py-2 px-2 font-mono text-slate-200">
                      {formatPrice(m.pricing.inputPerMillionTokens)}
                    </td>
                  ))}
                </tr>
                <tr className="border-b border-starquantix-navy-lighter">
                  <td className="py-2 px-2 text-slate-300">Output / 1M</td>
                  {models.map((m) => (
                    <td key={m.id} className="py-2 px-2 font-mono text-slate-200">
                      {formatPrice(m.pricing.outputPerMillionTokens)}
                    </td>
                  ))}
                </tr>
                <tr className="border-b border-starquantix-navy-lighter">
                  <td className="py-2 px-2 text-slate-300">Cache / 1M</td>
                  {models.map((m) => (
                    <td key={m.id} className="py-2 px-2 font-mono text-slate-200">
                      {formatPrice(m.pricing.cacheInputPerMillionTokens)}
                    </td>
                  ))}
                </tr>
                <tr className="border-b border-starquantix-navy-lighter">
                  <td className="py-2 px-2 text-slate-300">Context</td>
                  {models.map((m) => (
                    <td key={m.id} className="py-2 px-2 text-slate-200">
                      {m.contextLength ? (m.contextLength / 1000).toFixed(0) + "K" : "—"}
                    </td>
                  ))}
                </tr>
              </tbody>
            </table>
          </div>
          <TaskCostTable models={models} />
        </>
      ) : (
        <p className="text-slate-300">Select models above to compare.</p>
      )}
    </div>
  );
}
