---
title: "nimory: My Internet at Home"
subtitle: "How I run files, photos, notes, finance and a self-hosted AI on one home server with Go apps, Docker, Caddy and a Cloudflare Tunnel."
date: 2026-06-06
tags: [home,note,generic]
---

[nimory](https://home.nihars.com) is a single machine running everything I need — files, photos, notes, scheduling, finance, and a self-hosted AI persona.
No subscriptions. No third-party dependency for the things that matter.

This is a write-up of how it's built and how it works. It's had a full rewrite since the last version of this post — every custom app is now a small Go binary instead of Python, and two of them replaced three older ones.

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
* GPU      : Intel UHD 630 (integrated) — now doing real work, see Photos below
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

All traffic passes through a single entry point: **Caddy** — the only container with published ports.

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
* sync.nihars.com → Syncthing
* home.nihars.com → Dashboard
* notes.nihars.com → Samanote
* postgres.nihars.com → Adminer (Postgres admin)
* data.nihars.com → Natlas
* arthik.nihars.com → arthik (`/` is a public about page, `/app` is the finance PWA)
* health.nihars.com → static health site (generated nightly)

Nextcloud is gone — I never used it day-to-day, so a cloud.nihars.com file explorer wasn't replaced with anything. One less thing to maintain.

### LAN Domains

Local mirrors of everything above at `*.nimory`, plus:

* dns.nimory → AdGuard admin UI (LAN-only, not published to the internet)

---

## Containers 📦

Each service runs in isolation and communicates over a shared internal network.

* Network: `homelab`
* Communication via container names
* No external exposure unless routed by Caddy
* 15 containers total (down from 19 before this rewrite)

### Edge + Networking

* caddy → reverse proxy
* cloudflared → tunnel client
* adguard → DNS + ad blocking

### Infrastructure

* postgres (pgvector) → database — now used only by Immich
* postgresweb → Postgres admin UI (Adminer)

### Files + Sync

* syncthing → folder sync (notes, documents, music)

### Photos (Immich v3)

* immich-server → API, web UI, **and** background jobs — the old separate worker container is gone, merged into one process in v3
* immich-machine-learning → face detection, smart search
* immich-redis → now Valkey, not Redis, and kept on its own isolated internal network so nothing else on the homelab network can reach it — disposable by design, no persistence
* Photos get real hardware video transcoding now, via the box's integrated GPU (Intel QuickSync, `/dev/dri` passthrough)

### AI Runtime

* ollama → local model runtime, one model loaded at a time, tiered fast/deep depending on the task

### Custom apps (all Go, all single static binaries)

* natlas → personal data manager (events, subscriptions, inventory, health, birthdays)
* kronos → nightly automation and scheduling
* omnimo → the AI persona + the only thing that talks to Telegram
* arthik → personal finance, double-entry
* samanote → notes (file-based)
* dashboard → system homepage

---

## The Five Custom Apps 🧩

Previous write-ups covered three home-built apps. There are five now, and all of them got rewritten from Python to Go this year — smaller images, faster rebuilds, no dependency trees to manage. Everything else on this machine — Caddy, Immich, Syncthing — is infrastructure in service of these:

**Natlas** is the web UI for the flat-file vault — events, subscriptions, inventory, health, birthdays. The thing I like most about the rewrite: plugins are now pure YAML files, not Python modules. A new kind of data is a config file, not code.

**Kronos** replaces the old Taskmaster — same nightly pipeline (archive rollover, inbox cleanup, subscriptions, event lifecycle, birthday sync, health site regeneration, daily briefing), same one-container-one-scheduler design, but it no longer talks to Telegram directly. More on that below.

**Omnimo** replaces the old Telegram bot and chat backend, combined into one binary. It's the AI persona — reachable as a Telegram bot I talk to directly — and it picked up a download manager (`/download` a link, video, or torrent straight into my share folder) along the way. Backed by a local Ollama model, with a paid API as an online fallback when I want it.

**arthik** is new: a from-scratch double-entry personal finance app, PWA, works offline. It replaces an older CSV-based version of itself and its old demo site, which is now just a read-only demo login instead of a separate container.

**samanote** is the notes webapp, also rewritten — markdown editor with live preview, directly over the same vault, no database or index underneath it.

All five still read and write plain YAML/Markdown/CSV files in the same Obsidian vault — no database, no API layer between most of them. That part hasn't changed and isn't going to: I can open any of these files by hand and understand exactly what's in it.

### How three of them talk to each other without a database

This is the part I actually find interesting enough to write about. Natlas, Kronos, and Omnimo all touch the same vault, and two small conventions are what let them cooperate without stepping on each other:

* **The outbox.** Only Omnimo is allowed to send a Telegram message. Kronos doesn't have a bot token anymore — when it needs to notify me about something, it drops a small JSON file into a shared `outbox/` folder instead. Omnimo polls that folder every few seconds and delivers whatever it finds. If Omnimo's down, Kronos keeps running — the message just waits.
* **A locked shared file.** One file in the vault, `event.md`, gets written by all three apps constantly enough that I gave it a real file lock. Every write grabs a short lock first; if it's busy, the write politely waits instead of corrupting the file. Everything else in the vault still has no lock at all — that's an accepted trade-off, not an oversight.

arthik and samanote stay deliberately outside both of these — they don't need to notify me yet, so they don't carry the complexity of hooking into them.

---

## Storage 💾

All persistent data lives on host:

    /home/datar/
    ├── data/
    │   ├── notes/       ← the vault: events, subscriptions, health, inventory, birthdays, outbox, finance
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

Kronos runs its own scheduler inside one container, against a job list, and works through the same nightly pipeline as before:

    archive rollover → inbox cleanup → subscriptions → event lifecycle
      → birthday sync (weekly) → event updates → regenerate health site
      → build daily briefing → hand it to Omnimo → Telegram

One real improvement worth a mention: date math around month-end now holds correctly for recurring things that fall on the 31st — it used to drift down to the 28th over a couple of months, it doesn't anymore.

---

## Security Model 🔐

* No open router ports
* No public SSH — Tailscale only
* Internal-only databases, and Postgres now has exactly one consumer (Immich) instead of several
* Immich's job queue is isolated on its own internal network, unreachable from anything else
* `no-new-privileges` enabled on hardened containers; arthik also runs with a read-only root filesystem
* All access via Caddy
* Secrets only in `.env` files — never in compose files or app config

One deliberate exception, unchanged from before: the dashboard has read-only access to the host filesystem and the Docker socket, which is how it shows live container and system stats. It's the one container with that level of visibility, kept that way on purpose.

A new, narrow one: Immich's photo server now has passthrough access to the GPU device for hardware video transcoding. Worth a mental note, not a concern — QuickSync transcoding itself doesn't need broad privileges.

Attack surface is otherwise intentionally minimal.

---

## Not Done Yet 🚧

* Alerting system — Kronos can tell me its *own* jobs failed, but nothing watches overall container health, disk space, or backup success and pages me proactively
* Restore documentation — still just "I know how this works," not written down anywhere
* Backup retention policy — backups happen, retention isn't formally decided
* Finance app tied into the rest of the vault — arthik can't yet push me a Telegram notice through Omnimo, or read upcoming bills out of my subscriptions list
* Vector search over the vault — Postgres has had `pgvector` installed and unused for a while now; it's time to either build something against it or stop pretending I will

---

nimory runs quietly and stays out of the way.

It's not complex for the sake of it. Just controlled, predictable, and entirely mine.
