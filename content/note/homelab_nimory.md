---
title: "nimory: My Internet at Home"
subtitle: "nihar's internet microcloud operating runtime yottabyte"
date: 2026-05-13
tags: [home,note,generic]
---

[nimory](https://home.nihars.com) is a single machine running everything I need — files, photos, notes, sync, and local AI.
No subscriptions. No third-party dependency for the things that matter.

This is a write-up of how it's built and how it works.

<picture>
  <source srcset="/assets/nimory_arch_dark.webp" media="(prefers-color-scheme: dark)">
  <img src="/assets/nimory_arch_light.webp" alt="nimory architecture">
</picture>

---

## Hardware 🖥️

A Dell OptiPlex 7060. Small form factor, low power, silent enough to ignore.

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
* nimos.nihars.com → AI UI

### LAN Domains

* photos.nimory → Immich
* cloud.nimory → Nextcloud
* sync.nimory → Syncthing
* home.nimory → Dashboard
* notes.nimory → Samanote
* nimos.nimory → AI UI
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

* postgres → shared database
* redis → cache + queues

### Files + Sync

* nextcloud → file storage
* syncthing → folder sync

### Photos (Immich)

* immich_server → API + UI
* immich_worker → background jobs
* immich_ml → ML processing

### AI Stack (Nimos)

* nimos_ollama → model runtime
* nimos_webui → chat UI
* nimos → backend

Everything runs locally. No external API calls.

### Apps

* samanote → notes (file-based)
* dashboard → system homepage

---

## Storage 💾

All persistent data lives on host:

    /home/datar/
    ├── data/
    │   ├── notes/
    │   ├── backups/
    │   └── workspace/
    └── docker/

* Containers mount host paths
* Rebuilds don’t affect data

---

## Automation ⚙️

Two cron jobs manage the system:

    30 2 * * * flock -n /tmp/notesctl.lock timeout 60m  ./notesctl
    30 3 * * * flock -n /tmp/nimoryd.lock  timeout 180m ./nimoryd

### notesctl

* Creates daily notes
* Removes empty notes
* Archives old notes
* Encrypts + uploads backups

### nimoryd

* Ensures Tailscale is running
* Restarts containers
* Updates compose stacks
* Pulls git repos
* Builds tools
* Manages backups

---

## Security Model 🔐

* No open router ports
* No public SSH
* Internal-only databases
* `no-new-privileges` enabled
* Encrypted backups (AES-256)
* All access via Caddy

Attack surface is intentionally minimal.

---

## Not Done Yet 🚧

* Alerting system
* Restore documentation
* Backup retention policy
* Advanced monitoring

---

nimory runs quietly and stays out of the way.

It’s not complex for the sake of it. Just controlled, predictable, and entirely mine.

