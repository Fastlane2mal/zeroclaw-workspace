# Architecture

**Purpose**: System design, component relationships, and technical patterns  
**Audience**: Engineers and developers understanding system internals  
**Last Updated**: February 2026 (v2026.02)

---

## Table of Contents

- [Design Philosophy](#design-philosophy)
  - [Immutability First](#immutability-first)
  - [Container-Based Development](#container-based-development)
  - [User-Level Services](#user-level-services)
- [4-Layer Architecture](#4-layer-architecture)
  - [Layer 1: Immutable Base](#layer-1-immutable-base-silverblue)
  - [Layer 2: Persistent Storage](#layer-2-persistent-storage)
  - [Layer 3: Container Environment](#layer-3-container-environment)
  - [Layer 4: AI Services](#layer-4-ai-services)
- [Network Architecture](#network-architecture)
- [Configuration Management](#configuration-management)
- [Security Architecture](#security-architecture)
- [Service Management Patterns](#service-management-patterns)

---

## Design Philosophy

### Immutability First

**Silverblue's ostree design**:
- Base OS is read-only and versioned
- Updates are atomic (all-or-nothing)
- Automatic rollback on failed updates
- No dependency conflicts between system packages

**Implications for this project**:
- Minimize rpm-ostree layering (only tailscale, samba)
- All development happens in containers
- User-space tools installed in containers or ~/.local
- System services configured via systemd, not package installs

**Benefits**:
- Predictable system state
- Easy rollback after bad updates
- Clear separation: OS vs apps vs data
- Reproducible across machines

### Container-Based Development

**Toolbox pattern** (Development):
```bash
toolbox create -c ai-stack
toolbox enter ai-stack
# Now in isolated environment with access to HDD
```

**Podman pattern** (Services):
```bash
podman run -d --name litellm \
  --network host \
  -v ~/.litellm:/app/litellm \
  ghcr.io/berriai/litellm:main-stable
```

**Why containers**:
- Isolation: Different Python versions, dependencies
- Reproducibility: Containers defined by images
- Flexibility: Easy to add/remove environments
- Immutability-friendly: No host modifications

**Container access to HDD**:
- Host path: `/mnt/hdd`
- Container path: `/var/mnt/hdd`
- Automatic mount via toolbox/podman configuration

### User-Level Services

**Pattern**: Services run as user, not root

```bash
# User systemd service
~/.config/systemd/user/ollama.service

# Managed by user
systemctl --user start ollama
systemctl --user enable ollama
```

**Why user-level**:
- No reboots required for updates
- Per-user isolation and quotas
- Easier debugging (no sudo needed)
- Aligns with headless/SSH workflow
- Survives across OS updates

**System services only for**:
- Network services (ssh, samba, tailscale)
- Hardware management
- OS-level functionality

---

## 4-Layer Architecture

```
┌─────────────────────────────────────────────────────────┐
│ Layer 4: AI Services                                    │
│ (Ollama, LiteLLM, AnythingLLM)                          │
├─────────────────────────────────────────────────────────┤
│ Layer 3: Container Environment                          │
│ (Toolbox: ai-stack, vibe | Podman: services)           │
├─────────────────────────────────────────────────────────┤
│ Layer 2: Persistent Storage                             │
│ (SSD: OS/containers | HDD: models/data)                 │
├─────────────────────────────────────────────────────────┤
│ Layer 1: Immutable Base                                 │
│ (Fedora Silverblue 40 + minimal layered packages)      │
└─────────────────────────────────────────────────────────┘
```

### Layer 1: Immutable Base (Silverblue)

**Components**:
- Fedora Silverblue 40 (rpm-ostree)
- Base packages (read-only)
- Layered packages (minimal):
  - tailscale (VPN access)
  - samba (file sharing)

**System Services**:
- sshd.service (remote access)
- smb.service + nmb.service (file sharing)
- tailscaled.service (VPN)

**Power Management**:
- All sleep/suspend targets masked (24/7 operation)
- GDM (GNOME Display Manager) disabled (v2026.02+)

**Management**:
```bash
# View layered packages
rpm-ostree status

# Add package (requires reboot)
rpm-ostree install <package>
sudo systemctl reboot

# Rollback if issues
rpm-ostree rollback
sudo systemctl reboot
```

### Layer 2: Persistent Storage

**Storage Strategy**:
- **System SSD**: OS, containers, ephemeral data
  - Fast, limited capacity (~224GB)
  - OS images, container layers, cache
  - User home directory (code, configs)

- **Secondary HDD**: Models, projects, long-term data
  - Large capacity (~932GB)
  - LLM models (multi-GB files)
  - Project data, backups, archives
  - Network share directory

**Mount Architecture**:
```
/mnt/hdd (host)
  ├── llms/          # Ollama models (~10-20GB)
  ├── projects/      # Development work
  │   ├── anythingllm-storage/
  │   ├── openclaw-config/ (archived)
  │   └── openclaw-workspace/ (archived)
  ├── backups/       # Daily backups (future)
  ├── cloud/         # Cloud sync (future)
  └── share/         # Samba network share

/var/mnt/hdd (containers)
  # Same directories, bind-mounted
```

**fstab Configuration**:
```
UUID=<actual-uuid> /mnt/hdd ext4 defaults,nofail 0 2
```

**Critical rules**:
- NEVER use device letters (sda, sdb) - boot order changes them
- ALWAYS use UUIDs - persistent across reboots
- Use `nofail` flag - system boots even if HDD fails
- Interactive detection before setup - verify user's hardware

**Device detection pattern**:
```bash
# Show all storage devices with details
lsblk -o NAME,SIZE,TYPE,ROTA,MOUNTPOINT,UUID

# ROTA=0 → SSD (fast, OS)
# ROTA=1 → HDD (large, data)
```

### Layer 3: Container Environment

#### Toolbox Containers (Development)

**ai-stack**: Python ML/AI development
```bash
toolbox create -y -c ai-stack
# Inside: Python 3.14, pip, scientific libraries
```

**vibe**: General development
```bash
toolbox create -y -c vibe
# Inside: Editors, build tools, utilities
```

**Container creation rules**:
- ALWAYS run as actual user: `sudo -u ${user} toolbox create`
- NEVER run toolbox as root (wrong user store)
- Use explicit image versions: `--image fedora-toolbox:43`
- HDD access via `/var/mnt/hdd` (automatic)

#### Podman Containers (Services)

**LiteLLM**: LLM routing proxy
```yaml
Service: ~/.config/systemd/user/litellm.service
Image: ghcr.io/berriai/litellm:main-stable
Port: 4000
Network: host (for Ollama access)
Config: ~/.litellm/config.yaml
```

**AnythingLLM**: Web UI with RAG
```yaml
Service: Manual (not auto-start yet)
Image: ghcr.io/mintplex-labs/anythingllm:master
Port: 3001
Network: host
Storage: /mnt/hdd/projects/anythingllm-storage
```

**Caddy**: HTTPS reverse proxy
```yaml
Service: Auto-restart enabled
Image: caddy:latest
Port: 8443
Network: host
Config: Inline reverse-proxy command
```

**Why Podman for services**:
- Production deployment pattern
- systemd integration (auto-restart)
- No daemon required (vs Docker)
- Rootless by default (security)
- Compatible with Docker images/compose files

### Layer 4: AI Services

#### Ollama (Local LLMs)

**Architecture**:
```
Binary: /usr/local/bin/ollama (system-wide)
Service: ~/.config/systemd/user/ollama.service (user)
Models: /mnt/hdd/llms (HDD via OLLAMA_MODELS env var)
API: 0.0.0.0:11434 (accessible from containers)
```

**Network binding**:
```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
```
- Default `127.0.0.1` not accessible from containers
- `0.0.0.0` binds to all interfaces (including container network)
- LiteLLM connects via `localhost:11434` (host network mode)

**Current models** (v2026.02):
- smollm2 (1.7B) - Fast, general chat (~10-15s)
- qwen2.5:1.5b - Coding specialist (~20-30s)

**Model management**:
```bash
# Download model
ollama pull smollm2

# Models stored on HDD automatically
ls /mnt/hdd/llms/blobs/

# Run locally
ollama run smollm2 "Hello"

# Remove slow models
ollama rm llama3.2
```

#### LiteLLM (API Gateway)

**Architecture**:
```
Deployment: Podman container (quadlet)
Port: 4000 (OpenAI-compatible API)
Config: ~/.litellm/config.yaml
Auth: Bearer token (LITELLM_MASTER_KEY)
Network: host mode
```

**Configuration pattern** (minimal, proven working):
```yaml
model_list:
  # Local models (FREE)
  - model_name: smollm2
    litellm_params:
      model: ollama/smollm2
      api_base: http://localhost:11434
  
  - model_name: qwen2.5-1.5b
    litellm_params:
      model: ollama/qwen2.5:1.5b
      api_base: http://localhost:11434
  
  # Cloud models - Groq (FREE, rate limited)
  - model_name: llama-3.3-70b
    litellm_params:
      model: groq/llama-3.3-70b-versatile
      api_key: os.environ/GROQ_API_KEY
  
  - model_name: llama-3.1-8b
    litellm_params:
      model: groq/llama-3.1-8b-instant
      api_key: os.environ/GROQ_API_KEY
  
  # Cloud models - Claude (PAID)
  - model_name: claude-haiku-4
    litellm_params:
      model: claude-3-5-haiku-20241022
      api_key: os.environ/ANTHROPIC_API_KEY

litellm_settings:
  drop_params: true  # Strip unsupported params before forwarding
```

**Why minimal config**:
- Reduces failure surface area
- Easier to debug
- Add features incrementally
- Proven working in current deployment

**Request flow**:
```
AnythingLLM → POST localhost:4000/v1/chat/completions
              ├→ smollm2 → Ollama → Local CPU inference (FREE)
              ├→ llama-3.3-70b → Groq API → Cloud (FREE, rate limited)
              └→ claude-haiku-4 → Claude API → Cloud (PAID)
```

**Parameter handling**:
- LiteLLM receives OpenAI-format params
- `drop_params: true` removes Ollama-unsupported params
- Forwards clean request to backend (Ollama, Groq, or Claude)

#### AnythingLLM (Web UI)

**Architecture** (v2026.02 - In Progress):
```
Deployment: Podman container
Port: 3001 (web interface)
Storage: /mnt/hdd/projects/anythingllm-storage (persistent)
Network: host mode (for LiteLLM access)
Access: SSH tunnel (http://localhost:3001)
```

**Features**:
- Modern chat interface
- Document upload with RAG
- Multi-workspace support
- Model selection via dropdown
- Conversation history

**LiteLLM connection**:
```
Base URL: http://localhost:4000/v1
API Key: ${LITELLM_MASTER_KEY}
Provider: Generic OpenAI
```

**Replaces**: OpenClaw (removed v2026.01 due to security)

#### OpenClaw (Archived)

**Status**: Removed in v2026.01 due to security vulnerabilities  
**Decision**: See DECISIONS.md and CHANGELOG.md  
**May be revisited**: When project matures and security issues resolved

---

## Network Architecture

### Service Ports

```
22    - SSH (sshd) - System service
139   - Samba NetBIOS (nmb) - System service
445   - Samba file sharing (smb) - System service
3001  - AnythingLLM web UI - Podman container
4000  - LiteLLM proxy (OpenAI-compatible API) - Podman container
8443  - Caddy HTTPS proxy - Podman container
11434 - Ollama (LLM inference API) - User systemd service
41641 - Tailscale (VPN) - System service
```

### Firewall Strategy

**Silverblue default**:
- Firewalld enabled
- SSH allowed by default
- Samba requires zone configuration

**v2026.02 Hardened Configuration**:
- SSH: Allowed (with key auth only)
- Samba: LAN zone only (home/trusted)
- LiteLLM: Localhost only (no firewall exposure)
- Ollama: Localhost only (bound to 0.0.0.0 but firewalled)
- AnythingLLM: Localhost only (SSH tunnel required)
- Caddy: Localhost only (SSH tunnel required)
- Tailscale: VPN mesh network (handles own traversal)

**Critical**: Removed dangerous 1025-65535 port range (Session 17 fix)

### Remote Access

**Primary**: SSH via Tailscale
```bash
ssh mal@silverblue-ai.your-tailnet.ts.net
```

**Secondary**: SSH via LAN
```bash
ssh mal@192.168.0.33
```

**Web UI Access**: SSH tunnel
```bash
# AnythingLLM
ssh -L 3001:localhost:3001 mal@silverblue-ai.your-tailnet.ts.net
# Then browse: http://localhost:3001
```

**File sharing**: Samba (LAN only)
```
\\192.168.0.33\share
\\silverblue-ai.your-tailnet.ts.net\share
```

---

## Configuration Management

### Centralized Config File

**Location**: `~/.silverblue-ai-config`  
**Permissions**: `chmod 600` (user read/write only)  
**Format**: Bash export statements

```bash
#!/usr/bin/env bash
# Silverblue AI Platform - Centralized Configuration

# PATHS
export HDD_MOUNT="/mnt/hdd"
export MODELS_DIR="${HDD_MOUNT}/llms"
export PROJECTS_DIR="${HDD_MOUNT}/projects"

# OLLAMA
export OLLAMA_HOST="0.0.0.0:11434"
export OLLAMA_MODELS="${MODELS_DIR}"

# LITELLM
export LITELLM_PROXY_PORT="4000"
export LITELLM_MASTER_KEY="sk-..."

# API KEYS
export ANTHROPIC_API_KEY="sk-ant-..."
export GROQ_API_KEY="gsk_..."

# (TELEGRAM_BOT_TOKEN removed - OpenClaw archived)
```

**Auto-sourcing**: Added to `~/.bashrc`
```bash
if [ -f ~/.silverblue-ai-config ]; then
    source ~/.silverblue-ai-config
fi
```

**Security**:
- Never commit to git (.gitignore entry)
- Generated during installation
- Contains all secrets in one place
- Easy to backup securely

### Service-Specific Configs

**Ollama**: Environment variables only
- Via systemd service file
- No separate config file needed

**LiteLLM**: `~/.litellm/config.yaml`
- Model definitions
- Routing rules
- Features (minimal: drop_params only)

**LiteLLM Environment**: `~/.config/litellm.env`
- Generated from ~/.silverblue-ai-config
- Format: No export, no quotes (for container)
- Used by Podman quadlet EnvironmentFile

**AnythingLLM**: Via web UI
- Workspace settings
- LiteLLM connection config
- Document embeddings settings

### Podman Quadlet Pattern

**Critical for environment variables**:
```ini
[Container]
Image=ghcr.io/berriai/litellm:main-stable
EnvironmentFile=%h/.config/litellm.env  # IN [Container] SECTION
# ... other settings

[Service]
Restart=on-failure
# NO EnvironmentFile here - won't reach container
```

**Lesson learned**: EnvironmentFile in [Service] section sets variables for systemd process only, NOT container. Must be in [Container] section.

---

## Security Architecture

### Authentication Layers

**SSH access**:
- Key-based only (production)
- Password auth disabled after initial setup
- Fail2ban integration (optional, future)

**Samba**:
- Per-user passwords (smbpasswd)
- LAN-only access (firewall rules)
- Anonymous access disabled

**LiteLLM**:
- Bearer token authentication
- Master key required for all requests
- No public exposure (localhost only)

**AnythingLLM**:
- User account authentication (via web UI)
- API key for LiteLLM connection
- No public exposure (SSH tunnel required)

### Data Isolation

**OS level**:
- Immutable base OS (read-only)
- rpm-ostree prevents unauthorized changes
- SELinux enabled (Silverblue default)

**Container level**:
- Separate user namespaces
- Bind mounts for HDD (read/write controlled)
- No privileged containers
- Rootless Podman

**Service level**:
- User-level systemd (non-root)
- Per-service file permissions
- Config files chmod 600

**Network level**:
- Firewall blocks high ports (1025-65535 removed)
- Services localhost-only
- VPN for remote access (Tailscale)

---

## Service Management Patterns

### Systemd User Services

**Location**: `~/.config/systemd/user/<service>.service`

**Template**:
```ini
[Unit]
Description=Service Name
After=network.target

[Service]
Type=simple
ExecStart=/path/to/command
Restart=on-failure
EnvironmentFile=%h/.silverblue-ai-config

[Install]
WantedBy=default.target
```

**Management**:
```bash
# Reload after changes
systemctl --user daemon-reload

# Start service
systemctl --user start <service>

# Enable auto-start
systemctl --user enable <service>

# View logs
journalctl --user -u <service> -f
```

**Auto-start requirements**:
- Service file must have `[Install]` section
- Must run `systemctl --user enable <service>`
- User must have lingering enabled: `loginctl enable-linger`

### Podman Quadlet Services

**Location**: `~/.config/containers/systemd/<name>.container`

**Advantages**:
- Declarative container definition
- systemd generates service automatically
- Auto-restart and dependency management
- EnvironmentFile support in [Container] section

**Example**:
```ini
[Unit]
Description=LiteLLM Proxy Server
After=network-online.target

[Container]
Image=ghcr.io/berriai/litellm:main-stable
ContainerName=litellm
Network=host
EnvironmentFile=%h/.config/litellm.env
Exec=--config /app/.litellm/config.yaml --port 4000

[Service]
Restart=on-failure

[Install]
WantedBy=default.target
```

### Podman Container Commands

**For non-quadlet containers** (AnythingLLM, Caddy):
```bash
# Start container
podman run -d --name anythingllm ...

# Enable auto-restart
podman update --restart=always anythingllm

# View logs
podman logs anythingllm --tail 50 -f

# Stop container
podman stop anythingllm

# Remove container
podman rm anythingllm
```

---

## Data Flow Diagram

```
                    ┌─────────────┐
                    │   User      │
                    │  (Browser)  │
                    └──────┬──────┘
                           │
                           │ SSH Tunnel
                           │ (localhost:3001)
                           │
                    ┌──────▼──────────┐
                    │  AnythingLLM    │
                    │  Web UI         │
                    │  (Port 3001)    │
                    └──────┬──────────┘
                           │
                           │ HTTP POST
                           │ /v1/chat/completions
                           │
                    ┌──────▼──────────┐
                    │   LiteLLM       │
                    │   API Gateway   │
                    │   (Port 4000)   │
                    └──────┬──────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              │            │            │
      ┌───────▼──────┐  ┌──▼──────┐  ┌──▼──────────┐
      │   Ollama     │  │  Groq   │  │  Claude     │
      │   (local)    │  │  API    │  │  API        │
      │              │  │ (cloud) │  │  (cloud)    │
      │ - smollm2    │  │ - llama │  │ - haiku-4   │
      │ - qwen2.5    │  │   3.3   │  │ - sonnet-4  │
      │              │  │   70b   │  │             │
      │ FREE         │  │ FREE*   │  │ PAID        │
      │ 10-30s       │  │ 1-2s    │  │ 1-3s        │
      └──────────────┘  └─────────┘  └─────────────┘

*Rate limited: 12k TPM for llama-3.3-70b
```

---

## Performance Characteristics

### Current System (v2026.02)

**Hardware**: Intel i5-8250U, 11GB RAM, 916GB HDD

**Response Times**:
- Local models (smollm2): 10-15 seconds
- Local models (qwen2.5): 20-30 seconds
- Groq cloud (llama-3.3-70b): 1-2 seconds
- Claude cloud (haiku-4): 1-3 seconds

**Resource Usage**:
- Idle RAM: ~3.5GB (down from ~4GB after GDM disabled)
- Ollama RAM: ~500MB base + model size during inference
- LiteLLM RAM: ~200MB
- AnythingLLM RAM: ~300MB
- Boot time: ~45 seconds (improved from 60s)

**Storage**:
- OS + containers: ~30GB (SSD)
- Models: ~10-15GB (HDD)
- Workspace: ~1GB (HDD)
- Available: ~200GB SSD, ~900GB HDD

### Bottlenecks

**CPU**: Primary bottleneck for local inference
- 8 threads (4C/8T) maxed during model runs
- Models >3B parameters take 60+ seconds (too slow)
- Solution: Use small models (1.5-2B parameters)

**RAM**: Adequate for current models
- 11GB sufficient for 1.5B models
- Larger models (7B+) would require 16GB+
- Swap not used during normal operation

**Storage**: Not a bottleneck
- Model loading: <5 seconds from HDD
- Could improve with SSD storage for models
- Network share adequate for file access

**Network**: Not a bottleneck
- Local: No network involved
- Cloud: Limited by API latency (already 1-3s)
- Tailscale: No noticeable overhead

---

## Scalability Considerations

### Current Limitations

**Single-node design**:
- No high availability
- No load balancing
- No automatic failover

**Resource constraints**:
- Local models limited by RAM/CPU
- HDD speed bottleneck for very large models
- Network bandwidth for cloud fallback

### Future Scaling Paths

**Vertical scaling**:
- Add GPU for faster local inference (10-100x speedup)
- More RAM for larger models (16GB → 32GB)
- Faster storage (NVMe) for model loading

**Horizontal scaling** (major architecture change):
- Multiple Ollama nodes with load balancing
- Distributed model serving
- Shared model cache (NFS or object storage)

**Current decision**: Keep simple single-node design until it becomes a bottleneck

---

## Monitoring and Observability

### Current State (Minimal)

**Service health**:
```bash
systemctl --user status ollama litellm
podman ps
systemctl status sshd smb nmb tailscaled
```

**Logs**:
```bash
journalctl --user -u ollama -f
podman logs litellm --tail 50 -f
podman logs anythingllm --tail 50 -f
```

**Resource usage**:
```bash
htop
podman stats
df -h /mnt/hdd
```

**Storage**:
```bash
du -sh /mnt/hdd/llms/
du -sh /mnt/hdd/projects/
```

### Future Enhancements (Not Implemented)

**Metrics collection**:
- Prometheus exporters for services
- Grafana dashboards
- Alert rules (disk space, service failures)

**Log aggregation**:
- Centralized logging (Loki)
- Log retention policies
- Search and analysis (Grafana)

**Cost tracking**:
- LiteLLM database logging (removed in v2025.12)
- Per-user/model cost attribution
- Budget alerts

---

## Related Documentation

- [README.md](README.md) - Project overview and current status
- [DEPLOYMENT.md](DEPLOYMENT.md) - How to deploy this architecture
- [OPERATIONS.md](OPERATIONS.md) - How to operate these services
- [DECISIONS.md](DECISIONS.md) - Why these architectural choices
- [REFERENCE.md](REFERENCE.md) - Quick lookup for commands and configs

---

**Status**: Stable production architecture (v2026.02)  
**Last Updated**: February 2026  
**Next Review**: Major changes only (breaking changes require discussion)
