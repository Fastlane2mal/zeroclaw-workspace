# Current Context

**⚡ What's happening right now - Read this for active work status**

Last Updated: 2026-02-20 (Session 22 - ZeroClaw Deployed)

---

## Current Status: ZeroClaw AI Agent Operational ✅

**Achievement**: AnythingLLM removed from server, model stack upgraded, ZeroClaw deployed as 24/7 AI agent  
**Stack**: Ollama + LiteLLM + ZeroClaw + Groq cloud + Caddy + Tailscale  
**Next Step**: Monitor ZeroClaw stability, optionally add Discord/Telegram channel

---

## Session 22 Summary

### What We Accomplished

1. ✅ **Research: OpenClaw Ecosystem Assessment**
   - Reviewed all major derivatives: ZeroClaw, NanoClaw, PicoClaw, IronClaw, NanoBot, memU, bitdoze-bot
   - Assessed PicoLM/PicoClaw (interesting but targets lower-spec hardware)
   - Selected ZeroClaw as best fit for i5-8250U hardware profile
   - OpenClaw original still not recommended (400MB runtime, CVEs, uncertain governance)

2. ✅ **AnythingLLM Removed from Server**
   - User has AnythingLLM running on Windows 11 PC (better experience, more resources)
   - Server container stopped, removed, image deleted
   - Data preserved at `/mnt/hdd/projects/anythingllm-storage`
   - Windows AnythingLLM connected to server LiteLLM via Tailscale

3. ✅ **Model Stack Upgraded**
   - Pulled qwen2.5:3b (better for agentic tool use)
   - Removed smollm2 (insufficient for agent instruction-following)
   - Updated LiteLLM config (6 models: 2 local, 2 Groq, 2 Claude)

4. ✅ **ZeroClaw Deployed**
   - Installed via `cargo install zeroclaw --locked`
   - Configured with Ollama (primary) + LiteLLM gateway (cloud fallback)
   - Memory database at `/mnt/hdd/projects/zeroclaw/memory.db`
   - Running as user systemd service, auto-starts on boot
   - Security: sandbox, allowlists, localhost-only gateway

5. ✅ **Documentation Updated**
   - ZEROCLAW_DEPLOYMENT.md — full step-by-step deployment guide
   - CHANGELOG.md — updated to v2026.02b
   - STATE_CURRENT_CONTEXT.md — this file
   - DECISIONS.md — ZeroClaw decision + AnythingLLM migration rationale

---

## System Status

### Working Services ✅
- **Ollama**: Active, models: qwen2.5:3b (primary), qwen2.5:1.5b (fallback)
- **LiteLLM**: Active, routing to 6 models
- **ZeroClaw**: Active, user systemd service, port 8080 localhost
- **Caddy HTTPS**: Available (start with `podman start caddy-https`)
- **Tailscale VPN**: Connected (100.110.112.76)
- **Samba**: Active (LAN file sharing)
- **SSH**: Active (key-based)

### Removed Services
- **AnythingLLM (server)**: Removed — moved to Windows PC
  - Data preserved: `/mnt/hdd/projects/anythingllm-storage`
  - Windows instance: running, connected to LiteLLM via Tailscale

### Available Models via LiteLLM (localhost:4000)
- **Local (FREE, no limits)**:
  - qwen2.5:3b (~15-25s, primary agent model) ✅
  - qwen2.5:1.5b (~10-15s, fast fallback) ✅
- **Groq Cloud (FREE, rate limited)**:
  - llama-3.3-70b (1-2s response, 12k TPM)
  - llama-3.1-8b (1s response, 6k TPM)
- **Claude Cloud (PAID)**:
  - claude-haiku-4 (instant, efficient)
  - claude-sonnet-4 (instant, highest quality)

---

## Current Architecture (Verified Working)

```
User Access Layer
    ├─ ZeroClaw (Telegram / Discord / CLI)
    ├─ API Clients (curl, Continue.dev, Cursor, scripts)
    ├─ Windows AnythingLLM (via Tailscale → LiteLLM)
    └─ SSH Access (via Tailscale VPN from anywhere)
         ↓
LiteLLM API Gateway (localhost:4000)
    ├─→ Ollama (localhost:11434) - Local Models [FREE]
    │    ├─ qwen2.5:3b (15-25s, agent primary)
    │    └─ qwen2.5:1.5b (10-15s, fast fallback)
    │
    ├─→ Groq (cloud via LiteLLM) - Fast Cloud [FREE]
    │    ├─ llama-3.3-70b (1-2s)
    │    └─ llama-3.1-8b (1s)
    │
    └─→ Claude (cloud) - Premium [PAID]
         ├─ claude-haiku-4
         └─ claude-sonnet-4

Agent Layer
    └─ ZeroClaw (localhost:8080) → Ollama / LiteLLM

Supporting Services
    ├─ Caddy HTTPS (localhost:8443)
    ├─ Tailscale (100.110.112.76)
    └─ Samba (\\silverblue-ai\share)
```

---

## System Resources

**Hardware**: Intel i5-8250U (4 cores, 8 threads), 11GB RAM, 916GB HDD

**Current Usage (Estimated)**:
- RAM: ~4-5GB / 11GB (36-45% used, improved after AnythingLLM removal)
- HDD: ~5-7GB / 916GB (models + ZeroClaw memory)
- CPU: 5-10% idle, 80-90% during inference

**Headroom**:
- ✅ ~6GB RAM free — comfortable for 24/7 operation
- ✅ Could add qwen2.5:7b if needed (~4GB model, feasible with current RAM)
- ✅ ZeroClaw uses <5MB RAM (negligible)

---

## Next Steps

### Immediate (Optional)
1. Add Telegram or Discord channel to ZeroClaw config (if desired)
2. Test ZeroClaw persistent memory across sessions
3. Connect Windows AnythingLLM to server LiteLLM if not already done

### Near Term
4. Monitor ZeroClaw for stability and upstream updates (new project)
5. Evaluate qwen2.5:7b for better quality local inference if RAM allows
6. Consider Continue.dev or Cursor integration using LiteLLM endpoint

### Medium Term
7. Evaluate ZeroClaw Discord integration for team use
8. Consider Pi 5 sidecar with PicoClaw for dedicated low-power inference node

---

## Key File Locations

| Item | Path |
|------|------|
| ZeroClaw binary | `~/.cargo/bin/zeroclaw` |
| ZeroClaw config | `~/.zeroclaw/config.json` |
| ZeroClaw memory DB | `/mnt/hdd/projects/zeroclaw/memory.db` |
| ZeroClaw service | `~/.config/systemd/user/zeroclaw.service` |
| AnythingLLM data | `/mnt/hdd/projects/anythingllm-storage` |
| LiteLLM config | `~/.litellm/config.yaml` |
| Master config | `~/.silverblue-ai-config` |

---

## Quick Commands

```bash
# Check all AI services
systemctl --user status ollama litellm zeroclaw

# ZeroClaw quick test
zeroclaw agent -m "Hello, are you working?"

# ZeroClaw logs
journalctl --user -u zeroclaw -f

# Resource check
free -h && df -h /mnt/hdd

# Models available
ollama list
```
