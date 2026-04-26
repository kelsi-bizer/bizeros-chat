# BizerOS Chat

BizerOS Chat is a self-hosted team messaging and collaboration platform.

## Features

- **Channels & DMs** — public, private, and direct messaging with threaded
  replies.
- **File sharing & search** — upload files, full-text search across
  messages and files.
- **Integrations** — incoming/outgoing webhooks, slash commands, bot
  accounts, and a plugin framework.
- **Realtime presence** — typing indicators, read receipts, and
  WebSocket-driven updates.
- **Cross-platform** — works in any modern browser; mobile and desktop
  clients available separately.
- **Privacy by default** — runs entirely on your hardware, no third-party
  servers in the loop.

## Technical notes

- Backed by PostgreSQL (bundled).
- Listens internally on port `8065`.
- Default site name and email sender are pre-set to **BizerOS Chat** via
  environment variables; the bundled config-store still controls
  everything else and can be edited from the System Console once you log
  in.
- Image is published at `ghcr.io/kelsi-bizer/bizeros-chat`.

## First-time setup

1. Open the app at the URL Runtipi assigns.
2. Create the first user account — it automatically becomes the system
   administrator.
3. Visit **System Console → General → Configuration** to set the public
   site URL, file upload limits, SMTP relay for emails, and any
   integrations you need.

## Source

This is a rebrand of the open-source Mattermost Team Edition codebase.
The fork lives at <https://github.com/kelsi-bizer/bizeros-chat>.
