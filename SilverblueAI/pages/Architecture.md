# Architecture

## Design Philosophy
Three principles guide every decision in this project:

**1. Immutability first** — The OS (Fedora Silverblue) is read-only. Updates are atomic and reversible. Nothing important is installed directly on the base OS if it can run in a container instead.

**2. Containers for services** — All AI services run in Podman containers. They are isolated, easy to update, and don't conflict with each other or the OS.

**3. User-level services** — Services run under the user account (not root), managed by user-level systemd. This means no reboots needed to restart services, and easier debugging.

## Four-Layer Stack

```
┌─────────────────────────────────────────┐
│  Layer 4: AI Services                   │
│  Ollama · LiteLLM · AnythingLLM · Caddy │
├─────────────────────────────────────────┤
│  Layer 3: Container Environment         │
│  Podman (rootless containers)           │
│  Systemd quadlets (auto-start)          │
├─────────────────────────────────────────┤
│  Layer 2: Persistent Storage            │
│  /mnt/hdd (HDD, UUID-mounted)           │
│  ~/.config, ~/.litellm (SSD configs)    │
├─────────────────────────────────────────┤
│  Layer 1: Immutable Base OS             │
│  Fedora Silverblue 40                   │
│  Tailscale · Samba (rpm-ostree layered) │
└─────────────────────────────────────────┘
```

## How Requests Flow
```
You (Windows PC)
    ↓  SSH tunnel or Tailscale VPN
AnythingLLM Web UI (port 3001)
    ↓  API calls
LiteLLM Gateway (port 4000)
    ↓  Routes to:
    ├── Ollama (local, port 11434) → smollm2, qwen2.5
    ├── Groq API (cloud) → llama-3.3-70b, llama-3.1-8b
    └── Anthropic API (cloud) → Claude Haiku, Sonnet
```

## How Documents Flow
```
You edit a page in Logseq (Windows PC)
    ↓  Logseq saves to F:\Projects\...\pages\
    ↓  F:\ is the Samba share → /mnt/hdd/share/ on server
AnythingLLM reads directly from /mnt/hdd/share/ (mounted as hotdir)
    ↓  No uploading needed — changes are immediately available
```

## Key Design Rules
- Never use device names (like `/dev/sda`) in fstab — always use UUIDs
- EnvironmentFile for API keys must be in `[Container]` section of quadlet files, NOT `[Service]`
- Ollama must bind to `0.0.0.0:11434` (not 127.0.0.1) so containers can reach it
- Never add a database to LiteLLM — causes deadlock (learned the hard way)
- Never expose services directly to the internet — Tailscale VPN only

## Configuration Files
| File | Purpose |
|---|---|
| `~/.silverblue-ai-config` | Master config: API keys, paths, tokens |
| `~/.litellm/config.yaml` | LiteLLM model routing rules |
| `~/.config/litellm.env` | LiteLLM environment variables (API keys) |
| `~/.config/systemd/user/ollama.service` | Ollama systemd service |
| `~/.config/containers/systemd/litellm.container` | LiteLLM quadlet |
| AnythingLLM launch command (see [[Services]]) | AnythingLLM run via podman run (not a quadlet) |

## What Was Deliberately Left Out
- No graphical desktop (headless by design, GDM disabled)
- No LiteLLM database (caused deadlocks in Sessions 12-14)
- No OpenClaw (security CVEs + Groq rate limit incompatibility)
- No GPU acceleration (hardware doesn't have a GPU)
- No public internet exposure (VPN only)

## Related
- [[Hardware]] — physical specs this runs on
- [[Services]] — details of each running service
- [[Decisions]] — why each design choice was made
