"use client";

import Image from "next/image";
import { useTranslations } from "next-intl";

export function Footer() {
  const t = useTranslations("footer");
  return (
    <footer className="border-t border-starquantix-navy-lighter bg-starquantix-navy-light py-8 mt-auto">
      <div className="container mx-auto px-4">
        <div className="flex flex-col items-center gap-4">
          <a
            href="https://starquantix.com"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 hover:opacity-90 transition-opacity"
          >
            <Image
              src="/starquantix-logo.webp"
              alt="StarQuantix"
              width={28}
              height={28}
              className="rounded"
            />
            <span className="text-slate-300 text-sm">
              {t("developedBy")} <span className="font-semibold text-white">StarQuantix LLC</span>
            </span>
          </a>
          <p className="text-slate-400 text-sm text-center">
            {t("tagline")}
          </p>
        </div>
      </div>
    </footer>
  );
}
