"use client";

import Image from "next/image";
import { useTranslations } from "next-intl";
import { Link, usePathname } from "@/i18n/routing";
import { LocaleSwitcher } from "./LocaleSwitcher";

export function Header() {
  const t = useTranslations("nav");
  const pathname = usePathname();

  const nav = [
    { href: "/", label: t("home") },
    { href: "/models", label: t("models") },
    { href: "/compare", label: t("compare") },
  ];

  return (
    <header className="border-b border-starquantix-navy-lighter bg-starquantix-navy-light backdrop-blur-sm">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-3">
          <Image
            src="/starquantix-logo.webp"
            alt="StarQuantix"
            width={40}
            height={40}
            className="rounded-lg"
          />
          <span className="text-xl font-bold">
            <span className="text-white">AI Models</span>
            <span className="text-starquantix-blue-light"> Stats</span>
          </span>
        </Link>
        <nav className="flex items-center gap-6">
          {nav.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              className={`transition-colors ${
                pathname === href || (href !== "/" && pathname.startsWith(href))
                  ? "text-starquantix-blue-light font-medium"
                  : "text-slate-300 hover:text-white"
              }`}
            >
              {label}
            </Link>
          ))}
          <LocaleSwitcher />
        </nav>
      </div>
    </header>
  );
}
