# Decisions

**Purpose**: Architectural decisions and their rationale  
**Audience**: Developers understanding why the system works this way  
**Format**: Decision → Rationale → Trade-offs → Status  
**Last Updated**: February 2026 (v2026.02)

---

## Table of Contents

- [Current Active Decisions](#current-active-decisions)
- [Core Design Decisions](#core-design-decisions)
- [AI Stack Decisions](#ai-stack-decisions)
- [Infrastructure Decisions](#infrastructure-decisions)
- [Service Management Decisions](#service-management-decisions)
- [Archived Decisions](#archived-decisions)

---

## How to Use This Document

**When to add a decision**:
- Architectural changes affecting multiple components
- Trade-offs that future maintainers should understand
- Alternative approaches considered and rejected
- Security-critical choices
- Configuration patterns that differ from defaults

**When NOT to add**:
- Standard configurations following official docs
- Temporary debugging steps
- Minor preference choices
- Decisions obvious from code/configs

**Format**: Each decision explains "why" more than "what" (code shows what).

---

## Current Active Decisions

**Summary of active architectural choices** (v2026.02):

| Category | Decision | Status |
|----------|----------|--------|
| OS | Fedora Silverblue (immutable) | ✅ Stable |
| Containers | Podman (rootless) | ✅ Stable |
| Services | User-level systemd | ✅ Stable |
| Storage | UUID-based fstab | ✅ Stable |
| LLM Engine | Ollama (local) | ✅ Stable |
| API Gateway | LiteLLM (Podman) | ✅ Stable |
| Web UI | AnythingLLM | 🟡 In-progress |
| Cloud Provider | Groq (free tier) + Claude (paid) | ✅ Stable |
| Remote Access | Tailscale VPN | ✅ Stable |
| File Sharing | Samba (LAN only) | ✅ Stable |
| Database | None (stateless) | ✅ Stable |

---

## Core Design Decisions

### Silverblue over Fedora Workstation

**Date**: 2025-01  
**Decision**: Use Fedora Silverblue as base OS  
**Status**: ✅ Stable - No regrets

**Rationale**:
- Immutable OS provides stability and predictability
- Atomic updates with automatic rollback
- Clear separation: OS vs apps vs data
- Reproducible across machines
- No dependency conflicts between system packages

**Trade-offs**:
- Less flexibility than traditional distros
- Steeper learning curve
- Some tools require containers
- More planning required for system changes

**Alternatives considered**:
- Fedora Workstation: Too mutable, package conflicts
- Ubuntu: Not immutable, snap conflicts
- Debian: Conservative package versions
- NixOS: Too complex for this use case

**Outcome**: Perfect fit for 24/7 headless server with frequent updates.

---

### Container-Based Development (Toolbox + Podman)

**Date**: 2025-01  
**Decision**: Use toolbox for development, Podman for services  
**Status**: ✅ Stable - Works well

**Rationale**:
- **Toolbox**: Isolated Python environments without venvs
- **Podman**: Production-ready service deployment
- Native Fedora integration (both)
- Rootless by default (security)
- No daemon required (vs Docker)
- Compatible with Docker images

**Trade-offs**:
- **Toolbox**: Fedora-specific (vs Distrobox)
- **Podman**: Slightly different from Docker (99% compatible)
- Learning curve for systemd integration

**Why not Docker**: Requires daemon, rootful by default, less Fedora integration.

**Outcome**: Clean separation between dev (toolbox) and production (Podman).

---

### User-Level Services

**Date**: 2025-01  
**Decision**: Run AI services as user systemd, not system services  
**Status**: ✅ Stable - Auto-start working

**Rationale**:
- No reboots required for updates
- Easier debugging (no sudo needed)
- Per-user isolation and quotas
- Aligns with headless/SSH workflow
- Survives across OS updates (user home persists)

**Trade-offs**:
- Slightly more complex setup than system services
- Requires `loginctl enable-linger`
- Need to understand user vs system systemd

**System services ONLY for**:
- Network services (SSH, Samba, Tailscale)
- Hardware management
- OS-level functionality

**Outcome**: Perfect for headless operation, easy updates without reboots.

---

### Centralized Configuration File

**Date**: 2025-01  
**Decision**: Single `~/.silverblue-ai-config` for all secrets  
**Status**: ✅ Stable - Working well

**Rationale**:
- Single source of truth
- Easier to backup securely
- Consistent access pattern (source config)
- All environment variables in one place

**Trade-offs**:
- Must secure properly (chmod 600)
- All eggs in one basket
- Could be split by service for granular access

**Security measures**:
- chmod 600 (user read/write only)
- Never commit to git (.gitignore)
- Separate from service configs
- Easy to rotate all credentials at once

**Outcome**: Simple, secure, easy to manage.

---

### UUID-Based Storage Mounts

**Date**: 2025-01  
**Decision**: Use UUIDs in fstab, never device letters  
**Status**: ✅ Stable - Critical for reliability

**Rationale**:
- Device letters (sda, sdb) change with boot order
- BIOS/UEFI boot sequence not guaranteed
- UUIDs are persistent across reboots
- Prevents wrong device mounting

**Trade-offs**:
- Less human-readable than /dev/sda1
- Requires detection step (lsblk)
- More typing

**Critical rule**: ALWAYS verify UUID before editing fstab.

**Implementation**:
```bash
# Wrong (breaks on reboot)
/dev/sda1 /mnt/hdd ext4 defaults 0 2

# Correct (persistent)
UUID=actual-uuid /mnt/hdd ext4 defaults,nofail 0 2
```

**Outcome**: Zero mount failures due to device letter changes.

---

## AI Stack Decisions

### LiteLLM via Podman (Not Pip)

**Date**: 2025-02-07  
**Decision**: Deploy LiteLLM as Podman container, not pip install  
**Status**: ✅ Stable - Service operational

**Rationale**:
- Python 3.14 in ai-stack too new for uvloop/uvicorn
- Immutable OS philosophy - prefer containers
- Official Docker image is production pattern
- Avoids Python version conflicts
- Easier to update (pull new image)

**Trade-offs**:
- Additional service layer (systemd quadlet)
- Slightly more complex than pip
- Container updates separate from system

**Evidence**:
- Pip install failed with uvloop errors
- Podman deployment worked first try
- LiteLLM docs recommend Docker

**Alternatives tried**:
- pip in ai-stack: Failed (Python 3.14 incompatibility)
- pip in vibe: Would work but breaks container philosophy
- System pip: Breaks immutable OS philosophy

**Outcome**: Perfect solution, aligns with architecture.

---

### Ollama Network Binding (0.0.0.0)

**Date**: 2025-02-08  
**Decision**: Bind Ollama to all interfaces, not just localhost  
**Status**: ✅ Stable - LiteLLM routing working

**Rationale**:
- Containers with `--network host` need to reach Ollama
- Default 127.0.0.1 not accessible from containers
- LiteLLM container needs Ollama API access

**Trade-offs**:
- Slightly less secure (LAN exposure)
- Mitigated by firewall (blocks external access)

**Implementation**:
```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
```

**Security**:
- Firewall blocks port 11434 from LAN
- Only accessible via localhost or containers
- No authentication (localhost trust model)

**Outcome**: Works perfectly, no security issues.

---

### LiteLLM Minimal Configuration

**Date**: 2025-02-08  
**Decision**: Start with minimal config, add features incrementally  
**Status**: ✅ Stable - Proven working

**Rationale**:
- Reduces failure surface area
- Easier to debug when issues occur
- Add complexity only when needed
- Proven working in production

**What's included**:
- Model definitions (local + cloud)
- `drop_params: true` (Ollama compatibility)
- Master key authentication

**What's excluded** (for now):
- Database logging (caused deadlock in Sessions 12-14)
- Caching (not needed yet)
- Complex fallback chains
- Load balancing
- Prometheus metrics

**Outcome**: Rock-solid reliability, easy to troubleshoot.

---

### LiteLLM EnvironmentFile Location (Critical Fix)

**Date**: 2025-02-12 (Session 15)  
**Decision**: Put EnvironmentFile in [Container] section, NOT [Service]  
**Status**: ✅ Stable - API keys reaching container

**Root cause discovered**:
- EnvironmentFile in [Service] sets env for systemd process only
- Vars don't automatically pass to podman run command
- Container launches without environment variables

**Correct pattern**:
```ini
[Container]
EnvironmentFile=%h/.config/litellm.env  # HERE
# ... other settings

[Service]
Restart=on-failure
# NOT here - won't reach container
```

**How to verify**:
```bash
podman exec litellm printenv | grep ANTHROPIC_API_KEY
# Should show actual key, not empty
```

**Impact**: Affected all deployments following v2.2 guide until fixed.

**Outcome**: Now documented in deployment guide, no more failures.

---

### No Database for LiteLLM

**Date**: 2025-12 (Sessions 12-14)  
**Decision**: Remove database stack, keep LiteLLM stateless  
**Status**: ✅ Stable - Zero deadlocks since removal

**Root cause**:
- Postgres database caused complete deadlock
- `update_spend` job reached "maximum running instances"
- Blocked ALL requests (no timeout, no error)
- LiteLLM hung indefinitely on every request

**Resolution**:
```bash
# Remove these files
rm ~/.config/containers/systemd/litellm-db.container
rm ~/.config/containers/systemd/litellm-db.volume
rm ~/.config/containers/systemd/litellm.network

# Remove from config
# database_url, store_model_in_db, litellm_salt_key
```

**Trade-offs**:
- Lost: Cost tracking, request logging
- Gained: 100% reliability, simpler debugging

**Rule going forward**: NEVER add `database_url` to LiteLLM config.

**Outcome**: 3 sessions of pain taught us - stateless is better.

---

### Groq Integration via LiteLLM

**Date**: 2026-02-14 (Session 19)  
**Decision**: Integrate Groq API via LiteLLM, not direct  
**Status**: ✅ Stable - Working via LiteLLM proxy

**Rationale**:
- Free tier cloud models (llama-3.3-70b, llama-3.1-8b)
- Fast responses (1-2s) vs local (10-30s)
- No cost (unlike Claude)
- Good for learning/experimentation

**Rate limits**:
- llama-3.3-70b: 12k TPM (tokens per minute)
- llama-3.1-8b: 6k TPM
- Sufficient for normal chat usage

**Trade-offs**:
- Rate limited (not suitable for agent frameworks)
- Requires internet connection
- Another API dependency

**Lessons learned**:
- Always check official documentation first
- Rate limits have multiple dimensions (RPM, TPM, RPD, TPD)
- Agent frameworks have high token usage (13k+ per request)

**Outcome**: Great for direct API use, incompatible with OpenClaw.

---

### Direct Groq Provider for OpenClaw - REJECTED

**Date**: 2026-02-14 (Session 19)  
**Decision**: Do NOT use Groq directly with agent frameworks  
**Status**: ❌ Rejected - Incompatible

**Attempted rationale**:
- Save ~200MB RAM by not running LiteLLM
- Simpler architecture (one less service)
- Direct connection potentially faster

**Why it failed**:
- OpenClaw sends 13k+ tokens per request
  - System prompts, workspace state, tools, history, user message
- Groq free tier limits:
  - llama-3.1-8b: 6k TPM (too low)
  - llama-3.3-70b: 12k TPM (barely too low)
- Every request hit 429 rate limit
- Session auto-restarted infinitely

**Error message**:
```
Error: 413 Request too large for model `llama-3.1-8b-instant`
Limit 6000, Requested 13032
```

**Why `maxTokens` doesn't help**: Only controls response size, not input.

**Alternative chosen**: Keep LiteLLM + local models routing
- Local models (smollm2, qwen2.5) have no rate limits
- Groq available via LiteLLM for occasional fast responses
- Already tested working (Session 18)
- Completely free, predictable

**Key insight**: Agent frameworks (OpenClaw, LangChain, etc.) have inherently high token usage. Free API tiers designed for simple completions may not be suitable.

**Outcome**: Documented limitation, prevented wasted effort.

---

### AnythingLLM as Primary Web UI

**Date**: 2026-02 (Session 21)  
**Decision**: Deploy AnythingLLM as primary web interface  
**Status**: 🟡 In-progress - Functional, being refined

**Rationale**:
- Modern web-based chat interface
- Document upload with RAG capabilities
- Multi-workspace support
- No Telegram dependencies (vs OpenClaw)
- Active development, good documentation

**Replaces**: OpenClaw (removed in v2026.01 due to security)

**Trade-offs**:
- Requires SSH tunnel for access
- More resource usage than simple bot
- Web-only (no native mobile app)

**Security**:
- No public exposure (localhost only)
- SSH tunnel required for access
- User authentication in web UI
- No CVEs or known vulnerabilities

**May revisit OpenClaw**: When security issues resolved and project matures.

**Outcome**: Working well, good user experience.

---

## Infrastructure Decisions

### Tailscale for Remote Access

**Date**: 2025-02  
**Decision**: Use Tailscale VPN for remote access, not public exposure  
**Status**: ✅ Stable - VPN active

**Rationale**:
- Zero-config VPN using WireGuard
- No port forwarding required
- Works behind NAT/firewalls
- Per-device authentication
- End-to-end encrypted

**Why NOT expose services directly**:
- Risk of unauthorized access
- DDoS vulnerability
- No need for public access
- Lab/learning deployment (not production)

**Trade-offs**:
- Requires Tailscale on all devices
- Depends on Tailscale service
- Learning curve for VPN concepts

**Alternatives**:
- Public IP + firewall: Too risky
- Cloudflare Tunnel: Unnecessary complexity
- WireGuard directly: More setup, less features

**Outcome**: Perfect balance of security and convenience.

---

### Single Samba Share

**Date**: 2025-01  
**Decision**: One shared directory instead of multiple shares  
**Status**: ✅ Stable - Simple and effective

**Rationale**:
- Simplicity (one share to manage)
- Sufficient for single-user deployment
- Easier to configure SELinux
- Less confusion for user

**Trade-offs**:
- Less granular access control
- Can't isolate sensitive data in shares
- Would need redesign for multi-user

**Current use**:
- Backups
- File transfer to/from Windows
- General shared storage

**Outcome**: Works perfectly for intended use case.

---

### GDM Disabled (v2026.02)

**Date**: 2026-02-15 (Session 21)  
**Decision**: Disable GNOME Display Manager  
**Status**: ✅ Stable - Reduces RAM usage

**Rationale**:
- Headless server doesn't need display manager
- Saves ~250MB RAM
- Faster boot times
- True headless operation (no X11/Wayland)

**Implementation**:
```bash
sudo systemctl disable gdm
sudo systemctl reboot
```

**Trade-offs**:
- No graphical console access
- Requires SSH for all access
- Can't easily show desktop to visitors

**Recovery**: SSH still works, can re-enable with `sudo systemctl enable gdm`

**Outcome**: Free RAM for AI services, cleaner architecture.

---

## Service Management Decisions

### Podman Quadlets for Services

**Date**: 2025-02  
**Decision**: Use Podman quadlets instead of podman-compose  
**Status**: ✅ Stable - Services auto-start

**Rationale**:
- Native systemd integration
- Declarative container definition
- Auto-start and restart policies
- systemd generates service automatically
- Better than raw podman run commands

**Format**:
```ini
# ~/.config/containers/systemd/service.container
[Container]
Image=ghcr.io/image:tag
# ... settings

[Service]
Restart=on-failure

[Install]
WantedBy=default.target
```

**Trade-offs**:
- Less familiar than docker-compose
- Fedora/RHEL specific
- Learning curve for quadlet syntax

**Why not docker-compose**: Requires Docker, less systemd integration.

**Outcome**: Excellent systemd integration, reliable auto-start.

---

### User Lingering Enabled

**Date**: 2025-01  
**Decision**: Enable user lingering for services  
**Status**: ✅ Stable - Services run without login

**Rationale**:
- Services run even when user not logged in
- Critical for headless/24/7 operation
- User systemd services auto-start on boot

**Implementation**:
```bash
loginctl enable-linger $USER
```

**What it does**: Keeps user systemd instance running at boot.

**Without lingering**: Services only start when user logs in via SSH.

**Outcome**: Perfect for headless server, services always running.

---

## Archived Decisions

### OpenClaw Deployment - ARCHIVED

**Date**: 2025-02 to 2026-01  
**Decision**: Deploy OpenClaw for Telegram bot interface  
**Status**: ⚠️ Archived - Removed due to security

**Why removed** (v2026.01):
- CVE-2026-25253 (CVSS 8.8): 1-click RCE
- CVE-2026-25157 (CVSS 7.8): SSH injection
- CVE-2026-24763 (CVSS 8.8): Container escape
- 21,639+ public instances compromised globally

**Decision**: Too risky for learning/lab environment

**Replaced with**: AnythingLLM (v2026.02)

**May revisit**: When project matures and security issues resolved

**Lessons**:
- Always monitor security advisories
- Open source != secure by default
- Lab deployments still need security baseline

---

## Decision-Making Process

**When evaluating decisions**:
1. What problem does this solve?
2. What are the alternatives?
3. What are the trade-offs?
4. Can we test this safely?
5. Can we roll back if needed?
6. Does this align with design philosophy?

**Red flags**:
- "Everyone does it this way" (not a rationale)
- "It's easier" (might sacrifice stability/security)
- "We can fix it later" (tech debt accumulation)

**Green flags**:
- Aligns with immutability principle
- Makes system more reproducible
- Reduces failure surface area
- Backed by evidence/testing
- Well-documented by upstream

---

**Related Documentation**:
- [ARCHITECTURE.md](ARCHITECTURE.md) - How decisions are implemented
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - When decisions cause issues
- [CHANGELOG.md](CHANGELOG.md) - When decisions were made

**Status**: Current decision log for v2026.02  
**Last Updated**: February 2026  
**Format**: Append-only (mark deprecated, don't delete)
