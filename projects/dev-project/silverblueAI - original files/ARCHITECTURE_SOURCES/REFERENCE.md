# Reference

**Purpose**: Quick lookup for commands, configurations, and technical details  
**Audience**: Operators and developers needing fast reference  
**Last Updated**: February 2026 (v2026.02)

---

## Table of Contents

- [System Information](#system-information)
- [File Locations](#file-locations)
- [Service Details](#service-details)
- [Common Commands](#common-commands)
- [Model Information](#model-information)
- [Configuration Templates](#configuration-templates)
- [API Endpoints](#api-endpoints)
- [Network Ports](#network-ports)

---

## System Information

### Hardware Specifications

| Component | Specification |
|-----------|---------------|
| CPU | Intel Core i5-8250U @ 1.60GHz |
| Cores | 4 physical, 8 threads |
| RAM | 11GB |
| Storage (SSD) | 224GB WDC WDS240G2G0B-00EPW0 |
| Storage (HDD) | 932GB WDC WD10JPVX-60JC3T1 |
| Network | eno1 (wired), wlo1 (wireless) |

### Software Versions

| Component | Version |
|-----------|---------|
| OS | Fedora Silverblue 40 |
| Kernel | 6.x (check: `uname -r`) |
| Ollama | Latest (check: `ollama --version`) |
| LiteLLM | main-stable (Docker tag) |
| AnythingLLM | master (Docker tag) |
| Podman | 4.x+ (check: `podman --version`) |
| Python (ai-stack) | 3.14 |

### Network Configuration

| Item | Value |
|------|-------|
| Hostname | silverblue-ai |
| LAN IP | 192.168.0.33 (example) |
| Tailscale IP | 100.110.112.76 |
| Tailscale Hostname | silverblue-ai.{tailnet}.ts.net |
| Primary Interface | eno1 (wired) |
| Firewall | firewalld (active) |

---

## File Locations

### Configuration Files

| File | Location |
|------|----------|
| Master config | `~/.silverblue-ai-config` |
| LiteLLM config | `~/.litellm/config.yaml` |
| LiteLLM env (container) | `~/.config/litellm.env` |
| SSH keys (public) | `~/.ssh/authorized_keys` |
| SSH keys (private) | `~/.ssh/id_ed25519` (Windows: `%USERPROFILE%\.ssh\`) |
| Bashrc | `~/.bashrc` |
| fstab | `/etc/fstab` |

### Service Files

| Service | Location |
|---------|----------|
| Ollama | `~/.config/systemd/user/ollama.service` |
| LiteLLM (quadlet) | `~/.config/containers/systemd/litellm.container` |
| SSH | `/etc/systemd/system/sshd.service` (system) |
| Samba | `/etc/systemd/system/smb.service` (system) |
| Tailscale | `/etc/systemd/system/tailscaled.service` (system) |

### Data Directories

| Purpose | Location |
|---------|----------|
| HDD mount | `/mnt/hdd` |
| Ollama models | `/mnt/hdd/llms` |
| Projects | `/mnt/hdd/projects` |
| AnythingLLM data | `/mnt/hdd/projects/anythingllm-storage` |
| Samba share | `/mnt/hdd/share` |
| Backups (future) | `/mnt/hdd/backups` |

### Log Locations

| Service | Command |
|---------|---------|
| Ollama | `journalctl --user -u ollama` |
| LiteLLM | `podman logs litellm` |
| AnythingLLM | `podman logs anythingllm` |
| Caddy | `podman logs caddy-https` |
| System | `journalctl` |
| SSH | `journalctl -u sshd` |
| Samba | `journalctl -u smb` |

---

## Service Details

### Active Services

| Service | Type | Port | Status | Auto-start |
|---------|------|------|--------|------------|
| Ollama | User systemd | 11434 | Running | Yes |
| LiteLLM | Podman quadlet | 4000 | Running | Yes |
| AnythingLLM | Podman | 3001 | Running | Manual |
| Caddy | Podman | 8443 | Running | Yes |
| SSH | System | 22 | Running | Yes |
| Samba | System | 445, 139 | Running | Yes |
| Tailscale | System | 41641 | Running | Yes |

### Service Management Commands

**User services** (Ollama, LiteLLM):
```bash
systemctl --user start <service>
systemctl --user stop <service>
systemctl --user restart <service>
systemctl --user status <service>
systemctl --user enable <service>
systemctl --user disable <service>
journalctl --user -u <service> -f
```

**System services** (SSH, Samba, Tailscale):
```bash
sudo systemctl start <service>
sudo systemctl stop <service>
sudo systemctl restart <service>
systemctl status <service>
sudo systemctl enable <service>
sudo systemctl disable <service>
journalctl -u <service> -f
```

**Podman containers**:
```bash
podman ps                           # List running containers
podman ps -a                        # List all containers
podman start <container>
podman stop <container>
podman restart <container>
podman logs <container> --tail 50 -f
podman stats                        # Real-time resource usage
podman inspect <container>
podman update --restart=always <container>
```

---

## Common Commands

### System Administration

**Check system status**:
```bash
# OS version
cat /etc/os-release

# Layered packages
rpm-ostree status

# Disk usage
df -h

# RAM usage
free -h

# CPU info
lscpu

# Process list
htop  # or: top
```

**Update system**:
```bash
# Check for updates
rpm-ostree upgrade --check

# Apply updates
rpm-ostree upgrade

# Reboot to apply
sudo systemctl reboot

# Rollback if issues
rpm-ostree rollback
sudo systemctl reboot
```

**Storage management**:
```bash
# Show all storage
lsblk -o NAME,SIZE,TYPE,ROTA,MOUNTPOINT,UUID

# Get UUID
sudo blkid /dev/sdX1

# Check HDD mount
mount | grep /mnt/hdd

# Disk usage by directory
du -sh /mnt/hdd/*

# Find large files
du -ah /mnt/hdd | sort -rh | head -20
```

### SSH and Remote Access

**From Windows PowerShell**:
```powershell
# SSH to server (LAN)
ssh mal@192.168.0.33

# SSH via Tailscale
ssh mal@silverblue-ai.your-tailnet.ts.net

# SSH with tunnel (AnythingLLM)
ssh -L 3001:localhost:3001 mal@silverblue-ai

# SSH with tunnel (HTTPS/Caddy)
ssh -L 8443:localhost:8443 mal@silverblue-ai

# Check SSH key
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub
```

**On server**:
```bash
# Check SSH service
systemctl status sshd

# View SSH connections
sudo ss -tnp | grep :22

# Regenerate SSH host keys (if needed)
sudo ssh-keygen -A
sudo systemctl restart sshd
```

### Tailscale Management

```bash
# Check status
sudo tailscale status

# Get IP address
sudo tailscale ip -4

# Bring up VPN
sudo tailscale up --authkey ${TAILSCALE_AUTHKEY}

# Bring down VPN
sudo tailscale down

# Show connection details
sudo tailscale netcheck

# View logs
journalctl -u tailscaled -f
```

### Ollama Operations

**Model management**:
```bash
# List installed models
ollama list

# Pull a model
ollama pull smollm2
ollama pull qwen2.5:1.5b

# Remove a model
ollama rm llama3.2

# Run model interactively
ollama run smollm2

# Show model info
ollama show smollm2
```

**Service management**:
```bash
# Check status
systemctl --user status ollama

# Start/stop/restart
systemctl --user start ollama
systemctl --user stop ollama
systemctl --user restart ollama

# View logs
journalctl --user -u ollama -f

# Test API
curl http://localhost:11434/api/generate -d '{
  "model": "smollm2",
  "prompt": "Hello",
  "stream": false
}'
```

### LiteLLM Operations

**Service management**:
```bash
# Check status
systemctl --user status litellm

# Restart after config change
systemctl --user restart litellm

# View logs
podman logs litellm --tail 50 -f

# Check environment variables
podman exec litellm printenv | grep -E "ANTHROPIC|GROQ|LITELLM"
```

**API testing**:
```bash
# Source config for API key
source ~/.silverblue-ai-config

# Test health endpoint
curl http://localhost:4000/health \
  -H "Authorization: Bearer ${LITELLM_MASTER_KEY}"

# List models
curl http://localhost:4000/v1/models \
  -H "Authorization: Bearer ${LITELLM_MASTER_KEY}"

# Test local model (smollm2)
curl http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer ${LITELLM_MASTER_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "smollm2",
    "messages": [{"role": "user", "content": "Hello"}]
  }'

# Test Groq model
curl http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer ${LITELLM_MASTER_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.3-70b",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### AnythingLLM Operations

**Container management**:
```bash
# Start AnythingLLM
podman run -d \
  --name anythingllm \
  --network host \
  -v /mnt/hdd/projects/anythingllm-storage:/app/server/storage:Z \
  --cap-add SYS_ADMIN \
  ghcr.io/mintplex-labs/anythingllm:master

# Stop
podman stop anythingllm

# Remove
podman rm anythingllm

# View logs
podman logs anythingllm --tail 50 -f

# Check storage
du -sh /mnt/hdd/projects/anythingllm-storage
```

**Access**:
```bash
# From Windows (SSH tunnel)
ssh -L 3001:localhost:3001 mal@silverblue-ai

# Then browse to: http://localhost:3001
```

### Samba Operations

**Service management**:
```bash
# Check status
systemctl status smb nmb

# Restart
sudo systemctl restart smb nmb

# Set user password
smbpasswd -a $USER

# Test configuration
testparm

# View active connections
sudo smbstatus
```

**SELinux management**:
```bash
# Enable Samba SELinux booleans
sudo setsebool -P samba_export_all_rw on
sudo setsebool -P samba_export_all_ro on

# Set context on share
sudo semanage fcontext -a -t samba_share_t "/mnt/hdd/share(/.*)?"
sudo restorecon -Rv /mnt/hdd/share

# Check context
ls -Z /mnt/hdd/share
```

**Firewall**:
```bash
# Check active zone
sudo firewall-cmd --get-active-zones

# Add Samba to zone
sudo firewall-cmd --permanent --zone=FedoraWorkstation --add-service=samba
sudo firewall-cmd --reload

# Verify
sudo firewall-cmd --list-services
```

### Firewall Management

```bash
# Check all rules
sudo firewall-cmd --list-all

# Check specific zone
sudo firewall-cmd --zone=FedoraWorkstation --list-all

# Add service
sudo firewall-cmd --permanent --add-service=<service>
sudo firewall-cmd --reload

# Remove dangerous port range (if present)
sudo firewall-cmd --permanent --remove-port=1025-65535/tcp
sudo firewall-cmd --permanent --remove-port=1025-65535/udp
sudo firewall-cmd --reload

# Test port from Windows
Test-NetConnection -ComputerName 192.168.0.33 -Port 4000
```

---

## Model Information

### Local Models (Ollama)

| Model | Size | RAM | Response Time | Use Case | Cost |
|-------|------|-----|---------------|----------|------|
| smollm2 | 1.7B | ~2GB | 10-15s | General chat | FREE |
| qwen2.5:1.5b | 1.5B | ~2GB | 20-30s | Coding | FREE |

### Cloud Models (Groq)

| Model | Response Time | TPM Limit | RPM Limit | Use Case | Cost |
|-------|---------------|-----------|-----------|----------|------|
| llama-3.3-70b-versatile | 1-2s | 12,000 | 30 | Complex tasks | FREE |
| llama-3.1-8b-instant | 1s | 6,000 | 30 | Fast responses | FREE |
| mixtral-8x7b-32768 | 1-2s | 5,000 | 30 | Reasoning | FREE |

**Rate limits**: TPM = Tokens Per Minute, RPM = Requests Per Minute

### Cloud Models (Anthropic)

| Model | Response Time | Context | Use Case | Cost (per message) |
|-------|---------------|---------|----------|-------------------|
| claude-3-5-haiku-20241022 | 1-3s | 200k | Fast, efficient | ~$0.0001 |
| claude-3-5-sonnet-20241022 | 2-4s | 200k | High quality | ~$0.001 |
| claude-opus-4 | 3-6s | 200k | Best quality | ~$0.015 |

**Note**: Actual costs vary by input/output token count.

### Model Selection Guide

**Use local models when**:
- Cost is primary concern (FREE)
- Privacy is important (data stays local)
- Offline capability needed
- Response time 10-30s acceptable

**Use Groq when**:
- Need fast responses (1-2s)
- Tasks within rate limits
- Want free cloud quality
- Can tolerate occasional rate limit errors

**Use Claude when**:
- Need best quality
- Complex reasoning required
- Rate limits unacceptable
- Willing to pay for reliability

---

## Configuration Templates

### ~/.silverblue-ai-config

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
export LITELLM_MASTER_KEY="sk-GENERATE_WITH_openssl_rand_-hex_32"

# ANTHROPIC (optional - for Claude)
export ANTHROPIC_API_KEY="sk-ant-YOUR_KEY_FROM_console.anthropic.com"

# GROQ (optional - for free cloud models)
export GROQ_API_KEY="gsk_YOUR_KEY_FROM_console.groq.com"

# TAILSCALE (optional - for VPN)
export TAILSCALE_AUTHKEY="tskey-auth-YOUR_KEY_FROM_tailscale.com"
```

**Generate keys**:
```bash
# LiteLLM master key
openssl rand -hex 32

# Get API keys from:
# - Anthropic: https://console.anthropic.com
# - Groq: https://console.groq.com
# - Tailscale: https://login.tailscale.com/admin/settings/keys
```

### ~/.litellm/config.yaml

```yaml
litellm_settings:
  drop_params: true  # Required for Ollama compatibility

model_list:
  # Local models (FREE, CPU-only)
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

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
```

### ~/.config/systemd/user/ollama.service

```ini
[Unit]
Description=Ollama Local LLM Service
After=network-online.target

[Service]
Type=simple
ExecStart=/usr/local/bin/ollama serve
Restart=on-failure
RestartSec=5
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_MODELS=/mnt/hdd/llms"

[Install]
WantedBy=default.target
```

### ~/.config/containers/systemd/litellm.container

```ini
[Unit]
Description=LiteLLM Proxy Server
Documentation=man:podman-systemd.unit(5)
After=network-online.target
Wants=network-online.target

[Container]
AddHost=host.containers.internal:host-gateway
Image=ghcr.io/berriai/litellm:main-stable
ContainerName=litellm
AutoUpdate=registry
Network=host
Volume=%h/.litellm:/app/.litellm:z
Exec=--config /app/.litellm/config.yaml --port 4000 --host 0.0.0.0
EnvironmentFile=%h/.config/litellm.env

[Service]
Restart=on-failure
TimeoutStartSec=120

[Install]
WantedBy=default.target
```

**CRITICAL**: `EnvironmentFile` must be in `[Container]` section, NOT `[Service]`.

### /etc/fstab (HDD mount)

```
# HDD mount (use actual UUID from: sudo blkid /dev/sdX1)
UUID=your-actual-uuid-here /mnt/hdd ext4 defaults,nofail 0 2
```

**Get UUID**:
```bash
sudo blkid /dev/sda1  # Replace with your HDD partition
```

---

## API Endpoints

### LiteLLM

**Base URL**: `http://localhost:4000`

**Authentication**: Bearer token
```
Authorization: Bearer sk-YOUR_LITELLM_MASTER_KEY
```

**Endpoints**:
```
GET  /health                     # Health check
GET  /v1/models                  # List available models
POST /v1/chat/completions        # Chat completion (OpenAI-compatible)
GET  /metrics                    # Prometheus metrics (if enabled)
```

**Example chat request**:
```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer ${LITELLM_MASTER_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "smollm2",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "What is 2+2?"}
    ],
    "temperature": 0.7,
    "max_tokens": 500
  }'
```

### Ollama

**Base URL**: `http://localhost:11434`

**No authentication required** (localhost only)

**Endpoints**:
```
GET  /api/tags                   # List models
POST /api/generate               # Generate completion
POST /api/chat                   # Chat completion
POST /api/pull                   # Pull model
DELETE /api/delete               # Delete model
POST /api/show                   # Show model info
```

**Example generate request**:
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "smollm2",
  "prompt": "What is 2+2?",
  "stream": false
}'
```

### AnythingLLM

**Base URL**: `http://localhost:3001`

**Access**: Via SSH tunnel only

**Authentication**: User login via web UI

**Features**:
- Chat interface
- Document upload
- Workspace management
- Model configuration
- RAG (Retrieval Augmented Generation)

---

## Network Ports

| Port | Service | Protocol | Firewall | Access |
|------|---------|----------|----------|--------|
| 22 | SSH | TCP | Open | LAN + Tailscale |
| 139 | Samba NetBIOS | TCP/UDP | LAN only | LAN |
| 445 | Samba | TCP | LAN only | LAN |
| 3001 | AnythingLLM | TCP | Blocked | Localhost |
| 4000 | LiteLLM | TCP | Blocked | Localhost |
| 8443 | Caddy HTTPS | TCP | Blocked | Localhost |
| 11434 | Ollama | TCP | Blocked | Localhost |
| 41641 | Tailscale | UDP | Open | VPN |

**Security note**: All AI services (3001, 4000, 8443, 11434) are localhost-only. Access via SSH tunnel.

---

## Troubleshooting Quick Reference

### Service Won't Start

```bash
# Check service status
systemctl --user status <service>

# Check logs
journalctl --user -u <service> -n 50

# Reload systemd after file changes
systemctl --user daemon-reload

# Check file permissions
ls -l ~/.config/systemd/user/<service>.service

# For Podman
podman logs <container> --tail 50
```

### API Not Responding

```bash
# Check port listening
sudo ss -tlnp | grep <port>

# Check firewall
sudo firewall-cmd --list-all

# Test locally
curl http://localhost:<port>/health

# Check environment variables
podman exec <container> printenv | grep <VAR>
```

### Storage Issues

```bash
# Check HDD mounted
mount | grep /mnt/hdd

# Check fstab
cat /etc/fstab

# Check UUID matches
sudo blkid | grep <uuid>

# Check permissions
ls -la /mnt/hdd
```

### SSH Issues

```bash
# Check SSH service
systemctl status sshd

# Check SSH key permissions
ls -la ~/.ssh/
# Should be: 700 for .ssh/, 600 for authorized_keys

# Check SSH config
sudo sshd -t  # Test config syntax

# View SSH logs
journalctl -u sshd -f
```

For complete troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

---

**Related Documentation**:
- [OPERATIONS.md](OPERATIONS.md) - Daily management tasks
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Problem diagnosis
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design details
- [DEPLOYMENT.md](DEPLOYMENT.md) - Installation procedures

**Status**: Current reference for v2026.02  
**Last Updated**: February 2026  
**Maintained**: Updated with each version release
