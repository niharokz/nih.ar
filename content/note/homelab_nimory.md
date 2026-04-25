---
title: "nimory: My Internet at Home"
subtitle: "nihar's internet microcloud operating runtime yottabyte"
date: 2026-04-25
tags: [home,note,generic]
---

nimory is my personal homelab. A single machine running everything I need — file storage, photos, notes, syncing, and a local AI stack. No subscriptions. No third-party dependency for the things that matter.

This is a write-up of how it's built and how it works.

---

## Hardware

A Dell OptiPlex 7060. Small form factor, low power, silent enough to ignore.

```
Hostname : nimory
OS       : Debian 12 (Bookworm)
CPU      : Intel i5-8400T — 6 cores, up to 3.3 GHz
RAM      : 16 GB
Storage  : 1.8 TB NVMe SSD
```

Storage is partitioned with LVM:

```
nvme0n1
├── nvme0n1p1   512M   /boot/efi
├── nvme0n1p2   488M   /boot
└── nvme0n1p3   1.8T   LVM
    ├── nimory--vg-root    →  /
    └── nimory--vg-swap_1  →  swap
```

Memory under normal load sits around 3.4 GB used, 12 GB available. Swap is untouched.

---

## Network and Access

### Internet access via Cloudflare Tunnel

There are no open ports on the router. nimory establishes an outbound encrypted tunnel to Cloudflare, and all public traffic comes through that tunnel. The home IP is never exposed.

```
Browser → Cloudflare DNS → Cloudflare Tunnel → cloudflared → Caddy → App
```

All public apps are served under `nihars.com`. Caddy handles TLS termination, routing, and security headers.

### Admin access via Tailscale

SSH is not exposed publicly. Remote administration goes through Tailscale — a private WireGuard mesh network between my devices.

```bash
tailscale ssh nimory
```

Works from anywhere, as if the machine is on the same LAN.

### Local LAN access

When on the same network, AdGuard Home resolves `*.nimory` names directly to the machine. This skips Cloudflare entirely and hits Caddy through the LAN IP.

```
Device (same Wi-Fi) → AdGuard DNS → Caddy → App
```

### Access summary

| Context | Apps | SSH |
|---|---|---|
| Internet | `*.nihars.com` via Cloudflare Tunnel | `tailscale ssh` |
| LAN | `*.nimory` via AdGuard DNS | `tailscale ssh` |
| Physical | — | avoided |

---

## Reverse Proxy: Caddy

Caddy is the single entry point for all traffic. It handles routing, TLS, and applies security headers to every response.

Security headers on every route:

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
```

### Public routing

| Domain | App |
|---|---|
| `photos.nihars.com` | Immich |
| `cloud.nihars.com` | Nextcloud |
| `sync.nihars.com` | Syncthing |
| `home.nihars.com` | Dashboard |
| `notes.nihars.com` | Samanote |
| `nimos.nihars.com` | AI UI |

### LAN routing

| Hostname | App |
|---|---|
| `photos.nimory` | Immich |
| `cloud.nimory` | Nextcloud |
| `sync.nimory` | Syncthing |
| `home.nimory` | Dashboard |
| `notes.nimory` | Samanote |
| `nimos.nimory` | AI UI |
| `dns.nimory` | AdGuard Home |

---

## Containers

All containers share an external Docker network named `homelab`. Services talk to each other by container name. Nothing is reachable from outside unless Caddy routes to it.

### Edge and networking

| Container | Image | Purpose |
|---|---|---|
| `caddy` | `caddy:2` | Reverse proxy, TLS |
| `cloudflared` | `cloudflare/cloudflared:latest` | Tunnel client |
| `adguard` | `adguard/adguardhome` | DNS, ad blocking |

### Infrastructure

| Container | Image | Purpose |
|---|---|---|
| `postgres` | `pgvector/pgvector:pg15` | Shared database |
| `redis` | `redis:7-alpine` | Cache, job queues |

Both are internal-only. No host ports exposed.

### Files and sync

| Container | Image | Purpose |
|---|---|---|
| `nextcloud` | `nextcloud:28-apache` | File storage |
| `syncthing` | `syncthing/syncthing:latest` | Folder sync |

Nextcloud compose (simplified):

```yaml
services:
  nextcloud:
    image: nextcloud:28-apache
    container_name: nextcloud
    restart: unless-stopped
    environment:
      POSTGRES_HOST: postgres
      POSTGRES_DB: ${NC_DB_NAME}
      POSTGRES_USER: ${NC_DB_USER}
      POSTGRES_PASSWORD: ${NC_DB_PASSWORD}
      REDIS_HOST: ${REDIS_HOST}
      REDIS_PORT: ${REDIS_PORT}
      REDIS_HOST_PASSWORD: ${REDIS_PASSWORD}
      TZ: ${TZ}
    volumes:
      - ./storage:/var/www/html
      - /home/datar/data:/external-data
    networks:
      - homelab
    security_opt:
      - no-new-privileges:true

networks:
  homelab:
    external: true
```

### Photos: Immich

Three containers working together:

| Container | Role |
|---|---|
| `immich_server` | API, web UI |
| `immich_worker` | Background jobs, thumbnails |
| `immich_ml` | Face detection, smart search (CPU-only) |

Upload path is mounted from the host: `${IMMICH_UPLOAD_PATH}` → `/usr/src/app/upload`. Both Postgres and Redis are shared with Nextcloud.

### AI stack: Nimos

| Container | Image | Role |
|---|---|---|
| `nimos_ollama` | `ollama/ollama:latest` | LLM runtime |
| `nimos_webui` | `ghcr.io/open-webui/open-webui:main` | Browser chat UI |
| `nimos` | `nimos-nimos` | Local backend |

Ollama compose (simplified):

```yaml
services:
  ollama:
    image: ollama/ollama:latest
    container_name: nimos_ollama
    restart: unless-stopped
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_NUM_THREADS=4
      - OLLAMA_MAX_LOADED_MODELS=1
      - OLLAMA_NUM_PARALLEL=1
    networks:
      - homelab
    security_opt:
      - no-new-privileges:true

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: nimos_webui
    restart: unless-stopped
    depends_on:
      - ollama
    environment:
      - OLLAMA_BASE_URL=http://nimos_ollama:11434
    volumes:
      - webui_data:/app/backend/data
    networks:
      - homelab
    security_opt:
      - no-new-privileges:true
```

Everything runs on-device. No external API calls.

### Apps

| Container | Image | Purpose |
|---|---|---|
| `samanote` | `note-samanote` | Notes app |
| `dashboard` | `dashboard-dashboard` | System homepage |

The dashboard runs with a read-only filesystem and mounts the Docker socket to read container stats. Samanote reads and writes from `/home/datar/data/notes` directly.

---

## Storage

All persistent data is on the host under `/home/datar/`. Containers mount from there. Rebuilding or updating a container image changes nothing on disk.

```
/home/datar/
├── data/
│   ├── notes/
│   │   └── Archive/
│   ├── backups/
│   │   ├── logs/
│   │   └── tar/
│   └── workspace/
│       ├── narch/
│       └── nih.ar/
└── docker/          ← all Docker Compose stacks
    ├── nextcloud/
    ├── immich/
    ├── nimos/
    ├── postgres/
    ├── caddy/
    └── ...
```

---

## Automation

Two cron jobs handle daily maintenance. Both written in Go.

```bash
# crontab
30 2 * * * flock -n /tmp/notesctl.lock timeout 60m  ./notesctl --config notesconfig.yml
30 3 * * * flock -n /tmp/nimoryd.lock  timeout 180m ./nimoryd  --config config.yaml
```

`flock -n` ensures only one instance runs at a time. `timeout` ensures they can't hang indefinitely.

### notesctl — runs at 02:30

Manages the daily notes lifecycle:

1. **Create** — makes today's note if it doesn't exist
2. **Prune** — deletes empty notes within the last 3 days
3. **Archive** — moves notes older than 10 days to `Archive/`
4. **Month-end** — groups archive files into a `YYYYMM/` folder on the last day of the month
5. **Backup** — tarballs the notes directory, encrypts with GPG (AES-256), uploads with rclone

Backup flow from the source:

```go
// create tar.gz
exec.Command("tar", "-czf", tarFile, "-C", cfg.Paths.NotesDir, ".").Run()

// encrypt
exec.Command(
    "gpg",
    "--batch", "--yes",
    "--symmetric",
    "--cipher-algo", "AES256",
    "-o", encFile,
    tarFile,
).Run()

os.Remove(tarFile)

// upload
dest := fmt.Sprintf("%s:%s", cfg.Rclone.Remote, cfg.Rclone.RemotePath)
exec.Command("rclone", "copy", encFile, dest, "-P").Run()

// cleanup only after successful upload
os.Remove(encFile)
```

The temp file is only deleted after the upload succeeds. If rclone fails, the encrypted archive stays for the next run.

notesctl config:

```yaml
paths:
  notes_dir:   /home/datar/data/notes
  archive_dir: /home/datar/data/notes/Archive
  logs_dir:    /home/datar/data/backups/logs
  temp_dir:    /tmp/notesctl

daily_note:
  delete_empty_lookback_days: 3

archive:
  archive_after_days: 10
  exclude_patterns:
    - ".*"
    - "syncthing*.txt"

month_end:
  enabled: true

rclone:
  enabled: true
  remote: "<remote>"
  remote_path: "notes"

encryption:
  enabled: true
  method: "gpg"
```

### nimoryd — runs at 03:30

Handles host and service maintenance:

1. **Tailscale** — ensures it's up with `tailscale up --ssh`
2. **Container restarts** — restarts selected containers (e.g. `dashboard`)
3. **Compose updates** — pulls and redeploys stacks every 5 days
4. **Git pulls** — keeps `narch` and `nih.ar` repos current
5. **Builds** — compiles `notesctl` and `nimoryd` after repo updates
6. **Backup housekeeping** — moves archive files to `/home/datar/data/backups/tar`

---

## Security

The surface is kept small by design:

- **No open router ports** — Cloudflare Tunnel initiates outbound; no inbound connections needed
- **No public SSH** — only accessible through Tailscale
- **Postgres and Redis** are internal-only — no host port bindings, ever
- **`no-new-privileges: true`** on all containers where set
- **Backups encrypted** with AES-256 GPG before leaving the machine
- **Caddy fronts everything** — apps are never directly reachable

---

## What's Not Done Yet

- Alerting — there's no notification if something breaks
- Restore documentation — the process is clear in my head, not on paper
- Backup retention policy — currently unbounded
- Monitoring beyond the dashboard

---

nimory runs quietly and stays out of the way. One machine, one disk, a shared Docker network, and two cron jobs holding everything together. It does what it needs to do.
