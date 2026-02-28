# BUILD_ARCHITECTURE

## Executive Summary

This document consolidates the Silverblue AI platform architecture as defined across the uploaded Markdown sources. It provides a canonical structure, provenance, and a single source of truth for onboarding and maintenance.

## Table of Contents

- 1. Overview
- 2. System Architecture Diagram References
- 3. Core Components and Roles
- 4. Build & Deployment Pipeline
- 5. Runtime Environment and Tooling
- 6. Data Flows and Interactions
- 7. Configuration, Secrets, and Security
- 8. Observability, Telemetry, and Logging
- 9. Governance, Decisions, and Change History
- 10. Provenance and Source References
- 11. Future Work / Gaps

---

## 1. Overview

The Silverblue AI platform is a self‑hosted, 24/7 production‑ready AI stack built on Fedora Silverblue. It follows an immutable‑base, container‑centric design that separates the OS, persistent storage, container runtime, and AI services into four layers:

1. **Layer 1 – Immutable Base** – Fedora Silverblue 40 with minimal layered packages (tailscale, samba).
2. **Layer 2 – Persistent Storage** – SSD for OS and containers; HDD for models, projects, and backups.
3. **Layer 3 – Container Environment** – Toolbox for development, Podman for services.
4. **Layer 4 – AI Services** – Ollama (local LLMs), LiteLLM (API gateway), AnythingLLM (web UI), Caddy (reverse proxy).

The platform is designed for headless operation, remote access via Tailscale, and secure, user‑level services.

---

## 2. System Architecture Diagram References

- **Architecture Diagram** – see `docs/architecture.png` (generated from the diagram in the source files).
- **Data Flow Diagram** – see `docs/data_flow.png` (derived from the diagram in the source files).

---

## 3. Core Components and Roles

| Layer | Component | Role | Notes |
|-------|-----------|------|-------|
| 1 | Fedora Silverblue | Immutable OS | Atomic updates, rollback |
| 2 | SSD | OS & container layers | Fast I/O |
| 2 | HDD | Models & projects | Large capacity, persistent |
| 3 | Toolbox (ai‑stack, vibe) | Development | Python ML/AI, editors |
| 3 | Podman | Service runtime | Rootless, systemd integration |
| 4 | Ollama | Local LLM inference | 0.0.0.0:11434 |
| 4 | LiteLLM | OpenAI‑compatible API gateway | 0.0.0.0:4000 |
| 4 | AnythingLLM | Web UI | 0.0.0.0:3001 |
| 4 | Caddy | HTTPS reverse proxy | 0.0.0.0:8443 |
| 4 | Tailscale | VPN | 0.0.0.0:41641 |
| 4 | Samba | LAN file sharing | 139/445 |

---

## 4. Build & Deployment Pipeline

1. **Development** – Code is written inside a Toolbox container (`ai‑stack`).
2. **Container Build** – Dockerfile or Podman build is used to create images for services.
3. **Deployment** – Services are deployed via Podman quadlet (`.container` files) or systemd user services.
4. **Continuous Integration** – GitHub Actions run tests and linting on every push.
5. **Release** – Docker images are pushed to ghcr.io; systemd units are updated in the repo.

---

## 5. Runtime Environment and Tooling

- **Container Runtime** – Podman (rootless) with quadlet for declarative service definitions.
- **Development Environment** – Toolbox (`ai‑stack`) with Python 3.14, pip, scientific libraries.
- **Configuration** – Centralized config file `~/.silverblue‑ai‑config` (chmod 600). Service‑specific configs are in `~/.config/systemd/user/` and `~/.config/containers/systemd/`.
- **Secrets** – Stored in the config file; never committed to git.
- **Networking** – Host networking for services; VPN via Tailscale.

---

## 6. Data Flows and Interactions

```
User (browser) → SSH tunnel → AnythingLLM (3001) → LiteLLM (4000) →
  ├─ Ollama (11434) – local models
  ├─ Groq API – cloud models
  └─ Claude API – cloud models
```

The data flow diagram (see `docs/data_flow.png`) illustrates the request path from the web UI through the API gateway to the chosen model backend.

---

## 7. Configuration, Secrets, and Security

- **SSH** – Key‑based only; password disabled after initial setup.
- **Samba** – LAN‑only, per‑user passwords, anonymous access disabled.
- **LiteLLM** – Bearer token authentication; master key stored in `~/.silverblue‑ai‑config`.
- **AnythingLLM** – Web UI authentication; connects to LiteLLM via SSH tunnel.
- **Firewall** – Default firewalld enabled; only necessary ports open.
- **SELinux** – Enforced; containers run in separate namespaces.
- **Secrets** – Stored in `~/.silverblue‑ai‑config` with `chmod 600`; never committed.

---

## 8. Observability, Telemetry, and Logging

- **Service Health** – `systemctl --user status` for user services; `podman ps` for containers.
- **Logs** – `journalctl --user -u <service>`; `podman logs <container>`.
- **Metrics** – Basic `htop`, `podman stats`, `df -h` for disk usage.
- **Future Enhancements** – Prometheus exporters, Loki log aggregation, Grafana dashboards.

---

## 9. Governance, Decisions, and Change History

### Key Architectural Decisions
| Decision | Rationale | Status |
|----------|-----------|--------|
| Use Fedora Silverblue | Immutable OS, atomic updates | ✅ Stable |
| Toolbox for dev, Podman for services | Isolation, rootless, systemd integration | ✅ Stable |
| User‑level systemd services | No reboot on updates, per‑user isolation | ✅ Stable |
| UUID‑based fstab | Persistent mounts | ✅ Stable |
| Centralized config file | Single source of truth | ✅ Stable |
| LiteLLM as API gateway | Unified API, routing to local/cloud | ✅ Stable |
| AnythingLLM web UI | User‑friendly interface | 🟡 In‑progress |

### Decision Log
- **2025‑01** – Chose Silverblue over Workstation for immutability.
- **2025‑01** – Adopted Toolbox + Podman workflow.
- **2025‑01** – Decided on user‑level services.
- **2025‑01** – Implemented UUID‑based mounts.
- **2025‑01** – Created centralized config file.
- **2025‑01** – Integrated LiteLLM.
- **2026‑02** – Updated decisions to reflect current stable state.

---

## 10. Provenance and Source References

| Section | Source File |
|---------|-------------|
| 1. Overview | `ARCHITECTURE.md` |
| 2. Diagram References | `ARCHITECTURE.md` |
| 3. Core Components | `ARCHITECTURE.md` |
| 4. Build Pipeline | `ARCHITECTURE.md` |
| 5. Runtime Environment | `ARCHITECTURE.md` |
| 6. Data Flows | `ARCHITECTURE.md` |
| 7. Security | `ARCHITECTURE.md` |
| 8. Observability | `ARCHITECTURE.md` |
| 9. Governance | `DECISIONS.md` |
| 10. Provenance | This document |

---

## 11. Future Work / Gaps

- **GPU Acceleration** – Add GPU support for faster local inference.
- **Horizontal Scaling** – Multiple Ollama nodes with load balancing.
- **Automated Backups** – Scheduled snapshots of HDD data.
- **Enhanced Monitoring** – Prometheus + Grafana dashboards.
- **Cost Tracking** – Per‑model cost attribution for cloud APIs.

---

*Last updated: 2026‑02‑28*