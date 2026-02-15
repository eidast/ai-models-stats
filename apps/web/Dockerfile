# Build from repo root: docker build -f apps/web/Dockerfile .
FROM node:20-alpine AS base

FROM base AS deps
WORKDIR /app
COPY package.json pnpm-workspace.yaml pnpm-lock.yaml* ./
COPY apps/web/package.json apps/web/
COPY packages/schema/package.json packages/schema/
COPY packages/shared-types/package.json packages/shared-types/
RUN corepack enable pnpm && pnpm install --frozen-lockfile

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/apps/web/node_modules ./apps/web/node_modules
COPY . .
RUN corepack enable pnpm && pnpm --filter web build

FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
# Ensure Cloud Run can reach the server (bind to all interfaces)
ENV HOSTNAME=0.0.0.0

COPY --from=builder /app/apps/web/public ./public
COPY --from=builder /app/apps/web/.next/standalone ./
COPY --from=builder /app/apps/web/.next/static ./.next/static

ENV PORT=3000
EXPOSE 3000

# Next.js standalone output writes the entrypoint at apps/web/server.js.
CMD ["node", "apps/web/server.js"]
