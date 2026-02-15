import { ModelsPageClient } from "./ModelsPageClient";
import { fetchModels, fetchProviders } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function ModelsPage() {
  let models: Awaited<ReturnType<typeof fetchModels>> = [];
  let providers: Awaited<ReturnType<typeof fetchProviders>> = [];
  try {
    [models, providers] = await Promise.all([
      fetchModels(),
      fetchProviders(),
    ]);
  } catch {
    // API unavailable at build/SSR time
  }

  return (
    <ModelsPageClient
      initialModels={models}
      providers={providers}
    />
  );
}
