import { useTranslations } from "next-intl";
import { Link } from "@/i18n/routing";

export default function HomePage() {
  const t = useTranslations("home");
  return (
    <section className="text-center py-20">
      <h1 className="text-4xl font-bold mb-4 text-white">{t("title")}</h1>
      <p className="text-xl text-slate-300 mb-8 max-w-2xl mx-auto">{t("subtitle")}</p>
      <Link
        href="/models"
        className="inline-block px-6 py-3 bg-starquantix-blue hover:bg-starquantix-blue-light rounded-lg font-medium transition-colors text-white"
      >
        {t("cta")}
      </Link>
    </section>
  );
}
