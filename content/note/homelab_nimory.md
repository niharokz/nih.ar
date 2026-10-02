---
title: "nimory: My Internet at Home"
subtitle: "nihar's internet microcloud operating runtime yottabyte"
date: 2026-10-03
tags: [home,note,generic]
---

[nimory](https://home.nihars.com) is a single machine running everything I need — files, photos, notes, sync, automation, and local AI.
No subscriptions. No third-party dependency for the things that matter.

This is a write-up of how it's built and how it works.

<picture>
  <source srcset="/assets/nimory_arch_dark.webp" media="(prefers-color-scheme: dark)">
  <img src="/assets/nimory_arch_light.webp" alt="nimory architecture">
</picture>

---

## Hardware 🖥️

A Dell OptiPlex 7060 Micro. Small form factor, low power, silent enough to ignore.

* Hostname : nimory
* OS       : Debian 12 (Bookworm)
* CPU      : Intel i5-8400T — 6 cores, up to 3.3 GHz
* RAM      : 16 GB
* Storage  : 1.8 TB NVMe SSD

Storage is partitioned with LVM:

    nvme0n1
    ├── nvme0n1p1   512M   /boot/efi
    ├── nvme0n1p2   488M   /boot
    └── nvme0n1p3   1.8T   LVM
        ├── nimory--vg-root    →  /
        └── nimory--vg-swap_1  →  swap

It runs continuously with minimal intervention and low power usage.

---

## Access Model 🌐

### Internet (Cloudflare Tunnel)

No ports are exposed on the router. nimory establishes an outbound encrypted tunnel.

    Browser → Cloudflare DNS → Cloudflare Tunnel → cloudflared → Caddy → App

* Public apps served via `*.nihars.com`
* TLS + routing handled by Caddy
* Home IP never exposed

### Admin (Tailscale)

SSH is private via WireGuard mesh:

```bash
tailscale ssh nimory
```

* Works from anywhere
* No public SSH exposure

### Local LAN

AdGuard resolves local domains:

    Device → AdGuard DNS → Caddy → App

* `*.nimory` domains
* No external routing
* Ads/tracking blocked

### Access Summary

* Internet → apps via Cloudflare, SSH via Tailscale
* LAN → apps via AdGuard, SSH via Tailscale
* Physical → avoided

---

## Reverse Proxy 🧭

All traffic passes through a single entry point: **Caddy**

* Handles TLS termination
* Routes based on domain
* Applies security headers

Security headers:

    Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
    X-Content-Type-Options: nosniff
    X-Frame-Options: SAMEORIGIN
    X-XSS-Protection: 1; mode=block
    Referrer-Policy: strict-origin-when-cross-origin

### Public Domains

* photos.nihars.com → Immich
* cloud.nihars.com → Nextcloud
* sync.nihars.com → Syncthing
* home.nihars.com → Dashboard
* notes.nihars.com → Samanote
* postgres.nihars.com → Adminer (Postgres admin)
* data.nihars.com → Natlas
* health.nihars.com → static health site (generated nightly)
* arthik.nihars.com → static site
* demoarthik.nihars.com → Arthik demo

### LAN Domains

* photos.nimory → Immich
* cloud.nimory → Nextcloud
* sync.nimory → Syncthing
* home.nimory → Dashboard
* notes.nimory → Samanote
* postgres.nimory → Adminer
* data.nimory → Natlas
* dns.nimory → AdGuard

---

## Containers 📦

Each service runs in isolation and communicates over a shared internal network.

* Network: `homelab`
* Communication via container names
* No external exposure unless routed by Caddy

### Edge + Networking

* caddy → reverse proxy
* cloudflared → tunnel client
* adguard → DNS + ad blocking

### Infrastructure

* postgres (pgvector) → shared database
* postgresweb → Postgres admin UI (Adminer)
* redis → cache + queues

### Files + Sync

* nextcloud → file storage (rarely used day-to-day)
* syncthing → folder sync (notes, documents, music)

### Photos (Immich)

* immich_server → API + UI
* immich_worker → background jobs
* immich_ml → ML processing (face detection, etc.)

### AI Runtime

* ollama → local model runtime
* nimo → chat backend (used internally, e.g. by the nightly briefing)
* telegrambot → "Nimo," the Telegram-facing persona

Each talks to Ollama independently — there's no shared AI gateway, just one local
runtime backing two different front doors. Everything runs locally. No external API calls
unless I've explicitly enabled an online fallback.

### Apps

* natlas → personal data manager (events, subscriptions, inventory, health, birthdays)
* taskmaster → nightly automation and scheduling
* samanote → notes (file-based)
* dashboard → system homepage

---

## The Three Custom Apps 🧩

Previous write-ups of nimory glossed over this, but three home-built apps are really what
the whole machine is *for*. Everything else — Caddy, Immich, Nextcloud — is infrastructure
in service of these:

**Natlas** is the web UI — a single-user FastAPI + Alpine.js app for editing the flat-file
vault: events, subscriptions, inventory, health, birthdays. Plugin-first: a new feature is a
folder, not a change to the core.

**Taskmaster** is the automation layer — one container, one internal scheduler, no OS-level
cron. It runs a nightly pipeline over the same vault: rolling over old notes, advancing
recurring events, syncing birthdays from Google Contacts, regenerating the static health site,
and sending me a daily briefing over Telegram.

**Nimo** is the AI persona, reachable two ways — as a Telegram bot I talk to directly, and as
an internal chat backend Taskmaster calls for the nightly briefing. Backed by a local Ollama
model, with an online fallback if I want it.

All three read and write the same plain YAML/Markdown/CSV files in an Obsidian vault — no
database, no API layer between them. That's deliberate: I can open any of these files by hand
and understand exactly what's in it.

---

## Storage 💾

All persistent data lives on host:

    /home/datar/
    ├── data/
    │   ├── notes/       ← the vault: events, subscriptions, health, inventory, birthdays
    │   ├── documents/   ← Syncthing
    │   ├── music/       ← Syncthing
    │   ├── photos/      ← manual, selected subset only (not Syncthing)
    │   ├── share/       ← Samba, LAN only
    │   ├── backups/
    │   └── workspace/
    └── docker/

* Containers mount host paths
* Rebuilds don't affect data

---

## Automation ⚙️

Taskmaster replaces what used to be two host cron jobs. It runs its own scheduler inside one
container, against `schedule.yml`, and works through a nightly pipeline against the vault:

    archive rollover → inbox cleanup → subscriptions → event lifecycle
      → birthday sync (weekly) → event updates → regenerate health site
      → build daily briefing → send it to Telegram

Nothing touches the vault without going through `yaml.safe_dump` — a past f-string YAML writer
once corrupted an events file, so every writer (Natlas, Taskmaster, the Telegram bot) follows
the same rule now.

---

## Security Model 🔐

* No open router ports
* No public SSH — Tailscale only
* Internal-only databases
* `no-new-privileges` enabled on hardened containers
* Encrypted backups
* All access via Caddy
* Secrets only in `.env` files — never in compose files or app config

One deliberate exception: the dashboard has read-only access to the host filesystem and the
Docker socket, which is how it shows live container and system stats. It's the one container
with that level of visibility, and I'm keeping it that way on purpose rather than by oversight.

Attack surface is otherwise intentionally minimal.

---

## Not Done Yet 🚧

* Alerting system
* Restore documentation
* Backup retention policy
* Advanced monitoring
* A proper finance dashboard (demoarthik is the prototype)
* Vector search over the vault (Postgres already has pgvector ready for it)

---

nimory runs quietly and stays out of the way.

It's not complex for the sake of it. Just controlled, predictable, and entirely mine.
