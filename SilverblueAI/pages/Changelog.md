# Changelog

**Purpose**: Version history and major changes  
**Format**: Date-based versioning (vYYYY.MM)  
**Last Updated**: February 2026

---

## Version History

### v2026.02b (February 2026) - ZeroClaw Deployment

**Release Date**: 2026-02-20  
**Session**: 22  
**Status**: 🟢 Current

**Major Changes**:
- ✅ **AnythingLLM Removed from Server**
  - Windows 11 PC now hosts AnythingLLM (better fit — closer to user, more resources)
  - Server data preserved at `/mnt/hdd/projects/anythingllm-storage`
  - ~300-800MB RAM freed on server
  - Windows AnythingLLM connects to server LiteLLM via Tailscale (100.110.112.76:4000)
- ✅ **Model Stack Upgraded for Agentic Use**
  - smollm2 (1.7B) replaced by qwen2.5:3b — better instruction-following for tool use
  - qwen2.5:1.5b retained as lightweight fast fallback
  - LiteLLM config updated, mixtral removed for simplicity
- ✅ **ZeroClaw AI Agent Deployed**
  - Rust-based agent (~3.4MB binary, <5MB RAM)
  - Resolves OpenClaw CVE/complexity/rate-limit issues
  - Connects natively to Ollama + LiteLLM
  - User-level systemd service (auto-starts on boot)
  - Channels: CLI + Telegram/Discord (configurable)
  - Memory: SQLite at `/mnt/hdd/projects/zeroclaw/memory.db`
  - Security: gateway pairing, sandbox, allowlists, localhost-only

**System Status**:
- Ollama: Running (qwen2.5:3b, qwen2.5:1.5b)
- LiteLLM: Running (local + Groq + Claude)
- ZeroClaw: Running (port 8080 localhost)
- Caddy: Available (port 8443)
- Tailscale: Active (100.110.112.76)
- AnythingLLM (server): Removed (data preserved on HDD)
- AnythingLLM (Windows): Running, connected to server LiteLLM

**RAM Profile**: ~4-5GB idle (improved from ~5-6GB)

**Known Issues**:
- Groq rate limits still apply (12k TPM for llama-3.3-70b)
- qwen2.5:3b is slower than smollm2 (better quality tradeoff)
- ZeroClaw is a new project — monitor for upstream updates

---

### v2026.02 (February 2026) - AnythingLLM + Stable Baseline

**Release Date**: 2026-02-15  
**Session**: 21  
**Status**: 🟡 Superseded by v2026.02b

**Major Changes**:
- ✅ AnythingLLM Web UI deployed (Phase 5)
- ✅ GDM disabled (~250MB RAM freed)
- ✅ Groq cloud integration stable
- ✅ Documentation consolidated (8 core docs)

---

### v2026.01 (January 2026) - Security Hardening

**Sessions**: 15-20 | **Status**: 🔴 Deprecated

- ❌ OpenClaw removed (CVE-2026-25253, CVE-2026-25157, CVE-2026-24763)
- ✅ Firewall hardened (removed 1025-65535 port range)
- ✅ LiteLLM EnvironmentFile fix ([Container] section)
- ✅ Groq API integration

---

### v2025.12 (December 2025) - Database Stack Removal

**Sessions**: 12-14 | **Status**: 🔴 Deprecated

- ❌ Postgres removed from LiteLLM (deadlock issue)
- **Key decision**: Never use `database_url` in LiteLLM config

---

### v2025.11 (November 2025) - Initial Deployment

**Sessions**: 1-11 | **Status**: 🔴 Deprecated

- ✅ Silverblue + Ollama + LiteLLM initial deployment
- ✅ UUID-based storage, SSH, Samba, Tailscale

---

## Component Version History

### Ollama
- **Current**: Latest — stable local inference
- **Models**: qwen2.5:3b (primary), qwen2.5:1.5b (fallback)
- **Removed**: smollm2 (v2026.02b)

### LiteLLM
- **Current**: main-stable (Podman quadlet)
- **Config**: 6 models — 2 local Ollama, 2 Groq, 2 Claude
- **Setting**: drop_params: true

### ZeroClaw
- **Current**: Latest from crates.io
- **Status**: ✅ Active — deployed v2026.02b
- **Service**: User systemd, auto-start on boot
- **Memory**: SQLite on HDD

### AnythingLLM
- **Server**: Removed (data at /mnt/hdd/projects/anythingllm-storage)
- **Windows**: Active, connected to server LiteLLM via Tailscale

### Caddy
- **Current**: Latest — HTTPS reverse proxy, port 8443

### Tailscale
- **Current**: Latest — active VPN, IP 100.110.112.76

---

## Migration Guide: v2026.02 → v2026.02b

```bash
# 1. Remove AnythingLLM from server
podman stop anythingllm && podman rm anythingllm
podman rmi ghcr.io/mintplex-labs/anythingllm:master

# 2. Pull new primary agent model
ollama pull qwen2.5:3b
ollama rm smollm2   # optional

# 3. Update LiteLLM config (see ZEROCLAW_DEPLOYMENT.md Phase 1)
# Replace smollm2 with qwen2.5:3b in ~/.litellm/config.yaml
systemctl --user restart litellm

# 4. Deploy ZeroClaw (see ZEROCLAW_DEPLOYMENT.md Phases 2-8)
cargo install zeroclaw --locked
zeroclaw onboard --provider ollama --interactive
systemctl --user enable --now zeroclaw

# 5. Connect Windows AnythingLLM to server LiteLLM
# Settings → LLM Provider → LiteLLM
# URL: http://100.110.112.76:4000
# API Key: your LITELLM_MASTER_KEY
```

---

## Roadmap

**Near term**: Monitor ZeroClaw stability, evaluate Discord channel, consider qwen2.5:7b if RAM allows.

**Medium term**: ZeroClaw persistent memory for cross-session context, evaluate Pi 5 sidecar with PicoClaw for embedded inference.

**Deferred**: OpenClaw (security/governance unclear post-Feb 2026), GPU acceleration (requires hardware upgrade).

---

**See also**: [ZEROCLAW_DEPLOYMENT.md](ZEROCLAW_DEPLOYMENT.md) | [DECISIONS.md](DECISIONS.md) | [OPERATIONS.md](OPERATIONS.md)

**Last Updated**: February 2026 (v2026.02b)
