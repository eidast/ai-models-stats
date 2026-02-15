import { notFound } from "next/navigation";
import { fetchModel } from "@/lib/api";
import { ModelDetail } from "./ModelDetail";

export const dynamic = "force-dynamic";

export default async function ModelDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const model = await fetchModel(id);
  if (!model) notFound();
  return <ModelDetail model={model} />;
}
