import createMiddleware from "next-intl/middleware";
import { NextResponse, type NextRequest } from "next/server";
import { routing } from "./routing";

const intlMiddleware = createMiddleware(routing);

// Friendly redirects for Spanish slugs (avoid 404s / broken console logs)
const REDIRECTS: Record<string, string> = {
  "/modelos": "/models",
  "/comparar": "/compare",
  "/es/modelos": "/es/models",
  "/es/comparar": "/es/compare",
};

export default function middleware(req: NextRequest) {
  const { pathname, search } = req.nextUrl;
  const target = REDIRECTS[pathname];
  if (target) {
    const url = req.nextUrl.clone();
    url.pathname = target;
    url.search = search;
    return NextResponse.redirect(url);
  }
  return intlMiddleware(req);
}

export const config = {
  matcher: ["/((?!api|_next|_vercel|.*\\..*).*)"],
};
