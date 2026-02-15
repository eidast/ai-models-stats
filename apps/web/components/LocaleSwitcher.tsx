"use client";

import { useLocale } from "next-intl";
import { usePathname, useRouter } from "@/i18n/routing";

export function LocaleSwitcher() {
  const locale = useLocale();
  const router = useRouter();
  const pathname = usePathname();

  const switchLocale = () => {
    const newLocale = locale === "en" ? "es" : "en";
    const newPath = pathname.replace(`/${locale}`, `/${newLocale}`) || `/${newLocale}`;
    router.push(newPath);
  };

  return (
    <button
      onClick={switchLocale}
      className="text-sm text-slate-300 hover:text-white px-2 py-1 rounded border border-starquantix-navy-lighter hover:border-starquantix-blue transition-colors"
    >
      {locale === "en" ? "ES" : "EN"}
    </button>
  );
}
