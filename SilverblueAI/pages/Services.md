# Services

## Service Overview
All services start automatically on boot. Managed via user-level systemd.

---

## Ollama
- **Purpose**: Runs local AI models on the CPU
- **Port**: 11434
- **Manages**: systemctl --user (ollama.service)
- **Models loaded**: smollm2, qwen2.5-1.5b
- **Data stored at**: `/mnt/hdd/llms/` (model files)
- **Key config**: Bound to `0.0.0.0` so containers can reach it

**Start/stop**:
```bash
systemctl --user start ollama
systemctl --user stop ollama
systemctl --user status ollama
```

---

## LiteLLM
- **Purpose**: Unified API gateway — one endpoint for all models (local and cloud)
- **Port**: 4000
- **Manages**: Podman container via systemd quadlet
- **Config file**: `~/.litellm/config.yaml`
- **API keys**: `~/.config/litellm.env`

**Models it routes to**:
- `smollm2` → Ollama local
- `qwen2.5-1.5b` → Ollama local
- `llama-3.3-70b` → Groq cloud (free, rate limited)
- `llama-3.1-8b` → Groq cloud (free, rate limited)
- `mixtral-8x7b` → Groq cloud (free, rate limited)
- `claude-haiku-4` → Anthropic cloud (paid)
- `claude-sonnet-4` → Anthropic cloud (paid)

**Start/stop**:
```bash
systemctl --user start litellm
systemctl --user stop litellm
systemctl --user status litellm
```

**Test it's working**:
```bash
curl -s http://localhost:4000/health -H "Authorization: Bearer ${LITELLM_MASTER_KEY}"
```

---

## AnythingLLM
- **Purpose**: Web-based chat UI with document upload and RAG (Q&A over your own documents)
- **Version**: latest (updated to v1.11.0 — Session 22)
- **Port**: 3001
- **Image**: `docker.io/mintplexlabs/anythingllm:latest`
- **App data stored at**: `/mnt/hdd/projects/anythingllm/` (workspaces, settings, chat history, uploaded documents)
- **Access**: Direct via Tailscale — `http://100.110.112.76:3001` (no SSH tunnel needed)

### Volume Mounts
| Host Path | Container Path | Purpose |
|---|---|---|
| `/mnt/hdd/projects/anythingllm` | `/app/server/storage` | AnythingLLM app data |

### Important Notes
- The `STORAGE_DIR` environment variable **must** be set — without it AnythingLLM warns of data loss on restart
- The hotdir folder (`/mnt/hdd/projects/anythingllm/hotdir/`) exists but does **not** auto-sync in the Docker version — files must be uploaded manually via the web UI
- Live Document Sync is a **Desktop-only** feature — not available in Docker
- LLM settings are **reset on container upgrade** — reconfigure after every update

### LiteLLM Connection Settings (reconfigure after upgrades)
| Setting | Value |
|---|---|
| Provider | Generic OpenAI |
| Base URL | `http://100.110.112.76:4000/v1` |
| API Key | Your LITELLM_MASTER_KEY from `~/.silverblue-ai-config` |
| Model | `llama-3.3-70b` |
| Context Window | 8,192 |

### Full Container Launch Command
```bash
podman run -d \
  --name anythingllm \
  --network host \
  --restart=always \
  -e STORAGE_DIR=/app/server/storage \
  -v /mnt/hdd/projects/anythingllm:/app/server/storage:Z \
  docker.io/mintplexlabs/anythingllm:latest
```

### Relaunch Procedure (if container config needs changing)
```bash
# Stop and remove container (data on HDD is safe)
podman stop anythingllm
podman rm anythingllm

# Relaunch
podman run -d \
  --name anythingllm \
  --network host \
  --restart=always \
  -e STORAGE_DIR=/app/server/storage \
  -v /mnt/hdd/projects/anythingllm:/app/server/storage:Z \
  docker.io/mintplexlabs/anythingllm:latest

# Verify
podman ps | grep anythingllm
podman logs anythingllm --tail 20
```

### Upgrading AnythingLLM
```bash
# Pull latest image
podman pull docker.io/mintplexlabs/anythingllm:latest

# Stop and remove current container
podman stop anythingllm
podman rm anythingllm

# Relaunch with latest image (same command as above)
# ⚠️ Remember to reconfigure LLM settings in the web UI after upgrading
```

### Start/stop
```bash
podman start anythingllm
podman stop anythingllm
podman restart anythingllm
podman logs anythingllm --tail 50
podman logs anythingllm -f
```

### Document Sync Workflow (Manual)
AnythingLLM does not auto-sync with Logseq in Docker mode. The workflow is:
1. Edit pages in Logseq on Windows (saved to `F:\Projects\SilverblueAI\pages\`)
2. When pages change, open AnythingLLM at `http://100.110.112.76:3001`
3. Go to your workspace → document icon → upload the changed file(s)
4. AnythingLLM re-processes and updates the workspace

### Adding a New Project
1. Create a new Logseq graph saved to a folder on F:\
2. In AnythingLLM, create a new workspace
3. Upload the project's Logseq pages via the web UI
4. Assign them to the new workspace

---

## Caddy (HTTPS Proxy)
- **Purpose**: Provides HTTPS access to AnythingLLM (optional, not always running)
- **Port**: 8443
- **Status**: Available but not set to auto-start
- **Start manually**: `podman start caddy-https`

---

## Tailscale (VPN)
- **Purpose**: Secure remote access without exposing ports to the internet
- **Tailscale IP**: 100.110.112.76
- **Manages**: System-level service (tailscaled)
- **Install on other devices**: https://tailscale.com

**Check status**:
```bash
tailscale status
```

---

## Samba (File Sharing)
- **Purpose**: Access the HDD from Windows as a mapped network drive
- **Manages**: System-level service (smb + nmb)
- **Share path on server**: `/mnt/hdd/share/`
- **Windows mapped drive**: F:\
- **Access from Windows**: Map network drive to `\\silverblue-ai\share` or `\\100.110.112.76\share`

**Note**: This is the same folder AnythingLLM reads documents from. Files saved to F:\ on Windows are immediately visible to AnythingLLM on the server.

---

## SSH
- **Purpose**: Remote terminal access to the server
- **Port**: 22
- **Auth**: Key-based only (no password)
- **Access**: `ssh silverblue-ai` (if configured in ~/.ssh/config on Windows)

---

## Quick Health Check (Run This Each Session)
```bash
# Are core services up?
systemctl --user status ollama litellm

# Is the API responding?
curl -s http://localhost:4000/health -H "Authorization: Bearer ${LITELLM_MASTER_KEY}"

# What models are available?
curl -s http://localhost:4000/v1/models -H "Authorization: Bearer ${LITELLM_MASTER_KEY}" | jq -r '.data[].id'

# How is RAM and disk?
free -h | grep Mem
df -h /mnt/hdd

# Is AnythingLLM running?
podman ps | grep anythingllm
```

## Related
- [[Architecture]] — how services connect
- [[Commands Reference]] — all useful commands
- [[Known Issues]] — things that have gone wrong
