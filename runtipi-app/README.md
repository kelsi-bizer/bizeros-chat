# Runtipi app definition for BizerOS Chat

This directory contains a Runtipi app package for installing **BizerOS
Chat** on a Runtipi instance. It is shipped here so the source of truth
lives next to the rebrand, but for actual installation the files need
to be copied into your custom app store repository at
<https://github.com/kelsi-bizer/bizeros-appstore>.

## Contents

```
bizeros-chat/
├── config.json              # App metadata (name, port, version, form fields)
├── docker-compose.yml       # Compose definition (BizerOS Chat + Postgres)
└── metadata/
    ├── description.md       # Long description shown in Runtipi UI
    └── logo.jpg             # 512×512 app icon
```

## How to install

### 1. Publish the image to GHCR

The `.github/workflows/build-image.yml` workflow in the parent repo
builds and pushes `ghcr.io/kelsi-bizer/bizeros-chat:<tag>` automatically
on every push to `main`, every `claude/**` branch, and every `v*.*.*`
tag. The first push will need the GHCR package to be set to **public**
so Runtipi hosts can pull without auth — do this once via the package
settings page after the first successful run:

  https://github.com/kelsi-bizer/bizeros-chat/pkgs/container/bizeros-chat

You can also build it manually:

```sh
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --file build/bizeros/Dockerfile \
  --tag ghcr.io/kelsi-bizer/bizeros-chat:latest \
  --push \
  .
```

### 2. Copy the app into your appstore repo

```sh
git clone https://github.com/kelsi-bizer/bizeros-appstore.git
cp -r runtipi-app/bizeros-chat bizeros-appstore/apps/
cd bizeros-appstore
git add apps/bizeros-chat
git commit -m "Add BizerOS Chat app"
git push
```

### 3. Register the app store in Runtipi

In Runtipi → **Settings → App Stores → Add custom app store** and point
it at your `bizeros-appstore` repo URL. Refresh the app list and
**BizerOS Chat** will appear under the *Social* category.

### 4. Install

Click **Install**, set a strong **Database password** when prompted,
choose a domain, and start the app. First user created becomes the
system administrator.

## What the image contains

The image is built by `build/bizeros/Dockerfile` in two stages:

1. **webapp-builder** (node:24): builds the rebranded React webapp
   from `webapp/` source via `npm ci && npm run build`. The output is
   the `webapp/channels/dist/` directory.
2. **final** (`mattermost/mattermost-team-edition`): starts from the
   upstream Mattermost server image and overlays the freshly-built
   webapp client plus our rebranded `server/i18n/` and
   `server/templates/` files.

The Go server binary is **not** rebuilt — it ships unchanged from
upstream. The two compiled-in `"Mattermost"` defaults (config default
site name and email-sender fallback) are overridden at runtime via
`MM_TEAMSETTINGS_SITENAME` and `MM_EMAILSETTINGS_FEEDBACKNAME` env
vars set in `docker-compose.yml`.

## Updating to a new upstream Mattermost release

1. Bump `UPSTREAM_IMAGE` default in `build/bizeros/Dockerfile`.
2. Bump `version` and `tipi_version` in `runtipi-app/bizeros-chat/config.json`.
3. Push — the workflow rebuilds and republishes.
4. In your appstore repo, copy the updated `config.json` + compose, commit, push.
5. Runtipi users see an "Update available" badge.
