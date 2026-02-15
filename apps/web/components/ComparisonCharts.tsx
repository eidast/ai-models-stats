"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import type { Model } from "@/lib/api";

const CHART_COLORS = {
  input: "#3b82f6",
  output: "#60a5fa",
  cache: "#34d399",
  task: "#8b5cf6",
};

function formatPrice(n: number): string {
  return `$${n.toFixed(2)}`;
}

/** Bar chart: Input, Output, Cache ($/1M) per model */
export function PricingBarChart({ models }: { models: Model[] }) {
  const data = models.map((m) => ({
    name: m.name.length > 20 ? m.name.slice(0, 18) + "…" : m.name,
    fullName: m.name,
    input: typeof m.pricing.inputPerMillionTokens === "number"
      ? m.pricing.inputPerMillionTokens
      : 0,
    output: typeof m.pricing.outputPerMillionTokens === "number"
      ? m.pricing.outputPerMillionTokens
      : 0,
    cache: typeof m.pricing.cacheInputPerMillionTokens === "number"
      ? m.pricing.cacheInputPerMillionTokens
      : 0,
  }));

  const hasAnyCache = data.some((d) => d.cache > 0);

  return (
    <div className="h-80 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis
            dataKey="name"
            tick={{ fill: "#94a3b8", fontSize: 12 }}
            angle={-25}
            textAnchor="end"
            height={60}
          />
          <YAxis
            tick={{ fill: "#94a3b8", fontSize: 12 }}
            tickFormatter={(v) => `$${v}`}
            stroke="#64748b"
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "#1e293b",
              border: "1px solid #334155",
              borderRadius: "8px",
            }}
            labelStyle={{ color: "#f1f5f9" }}
            formatter={(value: number | undefined) =>
              value != null ? [formatPrice(value), ""] : ["—", ""]
            }
            labelFormatter={(_, payload) =>
              (payload?.[0] as { payload?: { fullName?: string } })?.payload?.fullName ?? ""
            }
          />
          <Legend
            wrapperStyle={{ paddingTop: 16 }}
            formatter={(value) => (
              <span className="text-slate-300 text-sm">{value}</span>
            )}
          />
          <Bar dataKey="input" fill={CHART_COLORS.input} name="Input / 1M" />
          <Bar dataKey="output" fill={CHART_COLORS.output} name="Output / 1M" />
          {hasAnyCache && (
            <Bar dataKey="cache" fill={CHART_COLORS.cache} name="Cache / 1M" />
          )}
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

/** Bar chart: Cost for "Summarize 1K words" across models */
export function TaskCostBarChart({ models }: { models: Model[] }) {
  const inputTokens = 1500;
  const outputTokens = 200;

  const data = models
    .map((m) => {
      const inP = typeof m.pricing.inputPerMillionTokens === "number"
        ? m.pricing.inputPerMillionTokens
        : 0;
      const outP = typeof m.pricing.outputPerMillionTokens === "number"
        ? m.pricing.outputPerMillionTokens
        : 0;
      if (inP === 0 && outP === 0) return null;
      const cost =
        (inputTokens / 1_000_000) * inP + (outputTokens / 1_000_000) * outP;
      return {
        name: m.name.length > 20 ? m.name.slice(0, 18) + "…" : m.name,
        fullName: m.name,
        cost,
      };
    })
    .filter((d): d is NonNullable<typeof d> => d !== null);

  if (data.length === 0) return null;

  const maxCost = Math.max(...data.map((d) => d.cost), 0.01);

  return (
    <div className="h-72 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 10, right: 30, left: 80, bottom: 10 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis
            type="number"
            tick={{ fill: "#94a3b8", fontSize: 12 }}
            tickFormatter={(v) => `$${v.toFixed(4)}`}
            domain={[0, maxCost * 1.1]}
            stroke="#64748b"
          />
          <YAxis
            type="category"
            dataKey="name"
            tick={{ fill: "#94a3b8", fontSize: 12 }}
            width={75}
            stroke="#64748b"
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "#1e293b",
              border: "1px solid #334155",
              borderRadius: "8px",
            }}
            formatter={(value: number | undefined) =>
              value != null ? [formatPrice(value), "Cost"] : ["—", "Cost"]
            }
            labelFormatter={(_, payload) =>
              (payload?.[0] as { payload?: { fullName?: string } })?.payload?.fullName ?? ""
            }
          />
          <Bar dataKey="cost" fill={CHART_COLORS.task} name="Cost" radius={[0, 4, 4, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
