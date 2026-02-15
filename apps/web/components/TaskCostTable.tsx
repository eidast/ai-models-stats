"use client";

import { Fragment } from "react";
import { useTranslations } from "next-intl";
import type { Model } from "@/lib/api";

type TaskCluster = "text" | "image" | "audio" | "video";

interface TextTask {
  cluster: "text";
  id: string;
  input: number;
  output: number;
}

interface ImageTask {
  cluster: "image";
  id: string;
}

interface AudioTask {
  cluster: "audio";
  id: string;
  /** Approx tokens for 1 min (input for transcribe, output for TTS) */
  tokens: number;
  useOutput: boolean;
}

interface VideoTask {
  cluster: "video";
  id: string;
  seconds: number;
}

type Task = TextTask | ImageTask | AudioTask | VideoTask;

const TASKS: Task[] = [
  // Text cluster
  { cluster: "text", id: "summarize1k", input: 1500, output: 200 },
  { cluster: "text", id: "summarize10k", input: 15000, output: 500 },
  { cluster: "text", id: "translate500", input: 750, output: 750 },
  { cluster: "text", id: "codeReview", input: 500, output: 300 },
  // Image cluster
  { cluster: "image", id: "image1" },
  // Audio cluster
  { cluster: "audio", id: "tts1min", tokens: 1500, useOutput: true },
  { cluster: "audio", id: "transcribe1min", tokens: 1500, useOutput: false },
  // Video cluster
  { cluster: "video", id: "video1sec", seconds: 1 },
];

const CLUSTER_CAPABILITIES: Record<TaskCluster, string[]> = {
  text: ["coding", "document_summaries", "translation", "document_analysis", "rag"],
  image: ["image_generation"],
  audio: ["audio_generation"],
  video: ["video_generation"],
};

function modelSupportsCluster(model: Model, cluster: TaskCluster): boolean {
  const caps = CLUSTER_CAPABILITIES[cluster];
  return caps.some((c) => model.capabilities.includes(c));
}

function calcTaskCost(model: Model, task: Task): number | null {
  const p = model.pricing;

  switch (task.cluster) {
    case "text": {
      const inPrice = p.inputPerMillionTokens ?? 0;
      const outPrice = p.outputPerMillionTokens ?? 0;
      if (inPrice === 0 && outPrice === 0) return null;
      return (
        ((task as TextTask).input / 1_000_000) * inPrice +
        ((task as TextTask).output / 1_000_000) * outPrice
      );
    }
    case "image": {
      const perImage = p.imageOutputPerImage ?? p.imageInputPerImage;
      return typeof perImage === "number" ? perImage : null;
    }
    case "audio": {
      const t = task as AudioTask;
      const price = t.useOutput
        ? p.audioOutputPerMillionTokens ?? p.outputPerMillionTokens
        : p.audioInputPerMillionTokens ?? p.inputPerMillionTokens;
      if (typeof price !== "number") return null;
      return (t.tokens / 1_000_000) * price;
    }
    case "video": {
      const perSec = p.videoPerSecond;
      if (typeof perSec !== "number") return null;
      return perSec * (task as VideoTask).seconds;
    }
  }
}

function formatCost(cost: number | null): string {
  if (cost == null) return "—";
  return cost < 0.01 ? `$${cost.toFixed(4)}` : `$${cost.toFixed(2)}`;
}

export function TaskCostTable({ models }: { models: Model[] }) {
  const t = useTranslations("taskCosts");

  const taskLabels: Record<string, string> = {
    summarize1k: t("summarize1k"),
    summarize10k: t("summarize10k"),
    translate500: t("translate500"),
    codeReview: t("codeReview"),
    image1: t("image1"),
    tts1min: t("tts1min"),
    transcribe1min: t("transcribe1min"),
    video1sec: t("video1sec"),
  };

  const clusterLabels: Record<TaskCluster, string> = {
    text: t("clusterText"),
    image: t("clusterImage"),
    audio: t("clusterAudio"),
    video: t("clusterVideo"),
  };

  // Group tasks by cluster; only show clusters where at least one model supports it
  const clusters = (["text", "image", "audio", "video"] as TaskCluster[]).filter(
    (cluster) => models.some((m) => modelSupportsCluster(m, cluster))
  );

  if (clusters.length === 0) return null;

  return (
    <div>
      <h2 className="text-lg font-semibold mb-4 text-slate-200">{t("title")}</h2>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-starquantix-navy-lighter">
              <th className="text-left py-2 px-2 text-slate-200">Task</th>
              {models.map((m) => (
                <th
                  key={m.id}
                  className="text-right py-2 px-2 font-medium text-slate-200"
                >
                  {m.name}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {clusters.map((cluster) => (
              <Fragment key={cluster}>
                <tr
                  key={`cluster-${cluster}`}
                  className="bg-starquantix-navy-light/30"
                >
                  <td
                    colSpan={models.length + 1}
                    className="py-1.5 px-2 text-xs font-medium text-slate-400 uppercase tracking-wider"
                  >
                    {clusterLabels[cluster]}
                  </td>
                </tr>
                {TASKS.filter((task) => task.cluster === cluster).map((task) => (
                  <tr
                    key={task.id}
                    className="border-b border-starquantix-navy-lighter"
                  >
                    <td className="py-2 px-2 text-slate-300">
                      {taskLabels[task.id]}
                    </td>
                    {models.map((m) => {
                      const supports =
                        modelSupportsCluster(m, cluster) &&
                        calcTaskCost(m, task) != null;
                      const cost = supports ? calcTaskCost(m, task)! : null;
                      return (
                        <td
                          key={m.id}
                          className="py-2 px-2 text-right font-mono text-slate-200"
                        >
                          {formatCost(cost)}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
