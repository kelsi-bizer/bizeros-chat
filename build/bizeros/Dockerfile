# BizerOS Chat image — overlays a rebranded webapp build on top of the
# upstream mattermost-team-edition release. Server binary, OS deps, and
# distroless runtime come from upstream; the React client and the
# server-side i18n / template strings are replaced with our rebranded
# versions.
#
# Build context: repository root.

# ---------------------------------------------------------------------------
# Stage 1: build the rebranded React webapp from source.
# ---------------------------------------------------------------------------
FROM node:24-bookworm AS webapp-builder

WORKDIR /webapp

# Copy only what's needed to install workspaces, then full source.
# A single COPY keeps the layer count low; build context is filtered
# by .dockerignore to keep this small.
COPY webapp/ /webapp/

# `npm ci` requires a clean lockfile / package.json match. Fall back
# to `npm install` if upstream lockfile drifted.
RUN npm ci --no-audit --no-fund || npm install --no-audit --no-fund

# Build all platform subpackages and the channels webapp.
# Output lands in /webapp/channels/dist/.
RUN npm run build

# ---------------------------------------------------------------------------
# Stage 2: final image — upstream Mattermost server with our client overlay.
# ---------------------------------------------------------------------------
# Pin the upstream image with a build arg so CI can bump it cleanly.
ARG UPSTREAM_IMAGE=mattermost/mattermost-team-edition:release-11.7
FROM ${UPSTREAM_IMAGE}

# Replace the bundled webapp with our rebranded build. Existing files
# in /mattermost/client/ that aren't overwritten (e.g. plugins/) are
# preserved by COPY's merge semantics.
COPY --from=webapp-builder --chown=2000:2000 /webapp/channels/dist/ /mattermost/client/

# Overlay rebranded server-side i18n strings (used by API responses,
# system messages, push notifications) and email/HTML templates.
COPY --chown=2000:2000 server/i18n/ /mattermost/i18n/
COPY --chown=2000:2000 server/templates/ /mattermost/templates/

# Image labels for GHCR / OCI consumers.
LABEL org.opencontainers.image.title="BizerOS Chat"
LABEL org.opencontainers.image.description="BizerOS Chat — team messaging and collaboration platform"
LABEL org.opencontainers.image.source="https://github.com/kelsi-bizer/bizeros-chat"
LABEL org.opencontainers.image.licenses="MIT"
