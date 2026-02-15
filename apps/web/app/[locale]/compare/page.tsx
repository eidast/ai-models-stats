import { ComparePageClient } from "./ComparePageClient";
import { fetchModels, fetchCompare } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function ComparePage({
  searchParams,
}: {
  searchParams: Promise<{ ids?: string }>;
}) {
  const { ids } = await searchParams;
  const modelIds = ids ? ids.split(",").map((i) => i.trim()).filter(Boolean).slice(0, 5) : [];
  const [allModels, compareData] = await Promise.all([
    fetchModels(),
    modelIds.length > 0 ? fetchCompare(modelIds) : Promise.resolve({ models: [] }),
  ]);

  return (
    <ComparePageClient
      allModels={allModels}
      initialSelected={modelIds}
      compareModels={compareData.models}
    />
  );
}
