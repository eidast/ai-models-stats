"use client";

import { useTranslations } from "next-intl";
import { Link } from "@/i18n/routing";
import type { Model } from "@/lib/api";
import { TaskCostTable } from "@/components/TaskCostTable";

function formatPrice(n: number | undefined): string {
  if (n == null) return "—";
  return `$${n.toFixed(2)}`;
}

export function ModelDetail({ model }: { model: Model }) {
  const t = useTranslations("models");
  const p = model.pricing;

  return (
    <div>
      <Link href="/models" className="text-starquantix-blue-light hover:underline mb-4 inline-block">
        ← Back to models
      </Link>
      <div className="flex items-start justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-bold">{model.name}</h1>
          <p className="text-slate-300">{model.providerId} · {model.type}</p>
          {model.deprecated && (
            <span className="inline-block mt-2 text-sm bg-amber-900/50 text-amber-400 px-2 py-1 rounded">
              {t("deprecated")}
            </span>
          )}
        </div>
        <Link
          href={`/compare?ids=${model.id}`}
          className="px-4 py-2 bg-starquantix-blue hover:bg-starquantix-blue-light rounded-lg text-sm font-medium text-white"
        >
          {t("compare")}
        </Link>
      </div>

      <div className="grid gap-6 md:grid-cols-2 mb-8">
        <div className="p-4 bg-starquantix-navy-light rounded-lg border border-starquantix-navy-lighter">
          <h2 className="font-semibold mb-3 text-slate-200">Pricing (USD per 1M tokens)</h2>
          <dl className="space-y-2 text-sm">
            <div className="flex justify-between">
              <dt className="text-slate-300">Input</dt>
              <dd className="font-mono text-slate-200">{formatPrice(p.inputPerMillionTokens)}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-slate-300">Output</dt>
              <dd className="font-mono text-slate-200">{formatPrice(p.outputPerMillionTokens)}</dd>
            </div>
            {p.cacheInputPerMillionTokens != null && (
              <div className="flex justify-between">
                <dt className="text-slate-300">Cache input</dt>
                <dd className="font-mono text-slate-200">{formatPrice(p.cacheInputPerMillionTokens)}</dd>
              </div>
            )}
          </dl>
        </div>
        <div className="p-4 bg-starquantix-navy-light rounded-lg border border-starquantix-navy-lighter">
          <h2 className="font-semibold mb-3 text-slate-200">Capabilities</h2>
          <ul className="flex flex-wrap gap-2">
            {model.capabilities.map((c) => (
              <li
                key={c}
                className="px-2 py-1 bg-starquantix-navy rounded text-sm text-slate-200"
              >
                {c.replace(/_/g, " ")}
              </li>
            ))}
          </ul>
          <div className="mt-3 text-sm text-slate-300">
            Context: {model.contextLength ? (model.contextLength / 1000).toFixed(0) + "K" : "—"} · 
            Max output: {model.maxOutputTokens ?? "—"}
          </div>
        </div>
      </div>

      <TaskCostTable models={[model]} />
    </div>
  );
}
