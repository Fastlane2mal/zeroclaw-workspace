# Silverblue AI Platform

**Self-hosted AI inference server with local and cloud models**

[![Status](https://img.shields.io/badge/status-production--ready-green)]()
[![Version](https://img.shields.io/badge/version-2026.02-blue)]()
[![Platform](https://img.shields.io/badge/platform-Fedora%20Silverblue-294172)]()

---

## What is This?

A production-ready, headless AI platform that runs local LLMs with cloud fallback, deployed on Fedora Silverblue (immutable OS). Built for 24/7 operation, this system provides:

- **Local-first AI inference** - Run models like Llama, Qwen, SmolLM2 privately and offline
- **Unified API gateway** - Single endpoint routes to local (free) or cloud (paid) models
- **Web-based chat interface** - AnythingLLM provides modern web UI with document RAG
- **Containerized services** - Isolated, reproducible, easy to maintain
- **Remote access** - Secure SSH and Tailscale VPN access from anywhere

## Current Status (v2026.02)

🟢 **Production** - Running 24/7 on physical hardware

### Active Services
- ✅ **Ollama** - Local LLM inference (smollm2, qwen2.5-1.5b)
- ✅ **LiteLLM** - API gateway routing local/cloud models
- ✅ **Groq Cloud** - Free cloud inference via LiteLLM (llama-3.3-70b)
- ✅ **AnythingLLM** - Web UI with RAG capabilities (Phase 5 - In Progress)
- ✅ **Caddy** - HTTPS reverse proxy
- ✅ **Tailscale** - VPN for secure remote access
- ✅ **Samba** - Network file sharing (LAN)

### System Info
- **Hardware**: Intel i5-8250U, 11GB RAM, 916GB HDD
- **OS**: Fedora Silverblue 40 (immutable, atomic updates)
- **Access**: SSH via Tailscale VPN (100.110.112.76)
- **Uptime**: 24/7 headless operation

## Quick Start

```bash
# 1. SSH into server
ssh mal@silverblue-ai.your-tailnet.ts.net

# 2. Check service health
systemctl --user status ollama litellm
podman ps

# 3. Access AnythingLLM web UI (via SSH tunnel)
# From Windows: ssh -L 3001:localhost:3001 silverblue-ai
# Then browse: http://localhost:3001
```

**First time?** → See [GETTING_STARTED.md](GETTING_STARTED.md)

## Key Features

### 🏠 **Local-First Computing**
- Run LLMs on your hardware - no cloud required for most tasks
- Privacy-focused - your data stays local
- Cost-effective - free local inference, pay only for premium cloud tasks

### 🔄 **Intelligent Model Routing**
- Single API endpoint (`localhost:4000`) routes all requests
- Automatic fallback: local models → cloud models
- Manual override for specific model selection

### 🌐 **Modern Web Interface**
- AnythingLLM provides chat UI with document upload
- RAG (Retrieval Augmented Generation) with your documents
- Multi-workspace support for different projects

### 🛡️ **Production-Grade Infrastructure**
- Immutable OS (Silverblue) - atomic updates, automatic rollback
- Containerized services - isolated, reproducible
- User-level systemd - no root required, survives OS updates
- 24/7 operation - power management disabled, auto-start services

### 🔐 **Security & Access**
- SSH key-based authentication only
- Tailscale VPN for secure remote access
- No public internet exposure - all services localhost-only
- Firewall hardened - only SSH and Samba on LAN

## Documentation

### Getting Started
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - First-time deployment walkthrough
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Complete step-by-step deployment guide
- **[HARDWARE_PROFILE.md](HARDWARE_PROFILE.md)** - System specifications

### Operating the System
- **[OPERATIONS.md](OPERATIONS.md)** - Daily management and common tasks
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Known issues and solutions
- **[REFERENCE.md](REFERENCE.md)** - Commands, configs, quick lookup

### Understanding the Design
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and component relationships
- **[DECISIONS.md](DECISIONS.md)** - Architectural decisions and rationale
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and major changes

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      User Applications                       │
│  (AnythingLLM Web UI, API clients, coding assistants)       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │   LiteLLM API Gateway          │
        │   (localhost:4000)             │
        │   OpenAI-compatible endpoint   │
        └────────┬───────────────┬───────┘
                 │               │
        ┌────────▼─────┐  ┌─────▼──────────┐
        │ Ollama       │  │ Cloud APIs      │
        │ (local CPU)  │  │ (Groq, Claude)  │
        │              │  │                 │
        │ - smollm2    │  │ - llama-3.3-70b │
        │ - qwen2.5    │  │ - claude-haiku  │
        │              │  │                 │
        │ FREE         │  │ FREE/PAID       │
        └──────────────┘  └─────────────────┘
```

**Data Flow**:
1. User interacts via AnythingLLM web UI (http://localhost:3001)
2. AnythingLLM sends requests to LiteLLM (localhost:4000)
3. LiteLLM routes to local models (Ollama) or cloud (Groq/Claude)
4. Responses return through LiteLLM to AnythingLLM

## Model Selection Guide

### Local Models (FREE - CPU Only)
- **smollm2** (1.7B) - Fast responses (~10-15s), good for chat
- **qwen2.5-1.5b** - Better for coding (~20-30s), detailed responses

### Cloud Models via Groq (FREE - Rate Limited)
- **llama-3.3-70b** - High quality, fast (1-2s), 12k TPM limit
- **llama-3.1-8b** - Very fast (1s), 6k TPM limit

### Cloud Models via Claude (PAID)
- **claude-haiku-4** - Fast, efficient, ~$0.0001 per message
- **claude-sonnet-4** - Highest quality, ~$0.001 per message

**Recommendation**: Use local models for most tasks, cloud for premium/urgent needs.

## Performance Expectations

| Model | Response Time | Quality | Cost | Use Case |
|-------|---------------|---------|------|----------|
| smollm2 | 10-15s | Good | FREE | Chat, simple tasks |
| qwen2.5-1.5b | 20-30s | Better | FREE | Coding, detailed work |
| llama-3.3-70b (Groq) | 1-2s | High | FREE* | Fast complex tasks |
| claude-haiku-4 | 1-3s | High | $0.0001 | Premium tasks |

*Free tier rate limited: 12k tokens/min (Groq llama-3.3-70b)

## Cost Estimates

**Electricity**: ~$5-10/month (24/7 operation, 65W TDP CPU)

**API Usage**:
- Local models: $0 (unlimited)
- Groq models: $0 (rate limited)
- Claude Haiku: ~$1-2/month (50 messages/day)
- Claude Sonnet: ~$10-15/month (50 messages/day)

**Total**: $5-27/month depending on cloud model usage

## Use Cases

- 🤖 **Personal AI Assistant** - Chat, brainstorm, learn via web UI
- 💻 **Coding Assistant** - Code completion, documentation, debugging
- 📚 **Document Q&A** - Upload PDFs/docs, ask questions (RAG)
- 🔬 **LLM Experimentation** - Test prompts, compare models, develop locally
- 🏠 **Self-Hosted Infrastructure** - Full control, privacy, no vendor lock-in

## System Requirements

### Minimum
- CPU: Intel i5-8250U or equivalent (4C/8T)
- RAM: 8GB (11GB recommended)
- Storage: 256GB SSD + 500GB HDD
- Network: Wired ethernet (WiFi not covered)

### Recommended
- RAM: 16GB+ for faster local inference
- Storage: 1TB+ HDD for model collection
- Network: Gigabit ethernet for file sharing

## Contributing

This is a personal learning/lab deployment, but contributions welcome:

1. **Report Issues** - File issues in TROUBLESHOOTING.md format
2. **Share Improvements** - Submit config optimizations, new models
3. **Document Findings** - Add to DECISIONS.md or TROUBLESHOOTING.md

**Contribution Guidelines**:
- Test changes on your own system first
- Update relevant documentation (OPERATIONS.md, REFERENCE.md)
- Follow existing formatting and style
- Explain "why" not just "what"

## Security Notice

⚠️ **This is a LEARNING/LAB deployment** - Not hardened for production use with sensitive data.

**Security measures in place**:
- ✅ SSH key authentication only
- ✅ Tailscale VPN for remote access
- ✅ All AI services localhost-only (no public exposure)
- ✅ Firewall hardened (SSH and Samba only)

**NOT suitable for**:
- ❌ Processing sensitive/confidential data
- ❌ Public-facing services
- ❌ Multi-tenant environments
- ❌ Compliance-required workloads (HIPAA, PCI, etc.)

## Project History

- **v2026.02 (Current)** - AnythingLLM web UI, GDM disabled, stable baseline
- **v2026.01** - OpenClaw removed (security concerns), Groq integration
- **v2025.12** - Initial deployment, LiteLLM + Ollama

See [CHANGELOG.md](CHANGELOG.md) for detailed history.

## License

This project documentation is provided as-is for educational purposes.

Software components retain their original licenses:
- Fedora Silverblue - Multiple (GPL, MIT, etc.)
- Ollama - MIT License
- LiteLLM - MIT License
- AnythingLLM - MIT License

## Support

- **Documentation**: Start with [GETTING_STARTED.md](GETTING_STARTED.md)
- **Issues**: Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Questions**: Review [ARCHITECTURE.md](ARCHITECTURE.md) and [DECISIONS.md](DECISIONS.md)

---

**Status**: Production-ready, 24/7 operation since January 2026  
**Last Updated**: February 2026 (v2026.02)  
**Maintainer**: Personal project, single-node deployment
