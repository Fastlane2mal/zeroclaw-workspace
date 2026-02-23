# Session Log

Use this page as an index. Each session links to (or is recorded directly below) what was done.

---

## Session Template
Copy this at the start of each new session in your Logseq daily journal:

```
### Session [NUMBER] — [DATE]
**Goal**: 
**Duration**: 

**Completed**:
- 

**Commands run**:
- 

**Issues encountered**:
- 

**Decisions made**:
- 

**Next steps**:
- 
```

---

## Session History Summary

### Sessions 1–5 — Initial VM Deployment
**What happened**: Proved the concept worked in a VirtualBox virtual machine before touching real hardware.
- Installed Fedora Silverblue in VM
- Got Ollama running with local AI models
- Established the container-based service pattern
- Learned: immutable OS requires containers, not package installs

### Sessions 6–8 — Hardware Migration
**What happened**: Moved from VM to the physical laptop server.
- Installed Silverblue on the SSD
- Configured HDD mount using UUID (critical lesson learned here)
- Set up SSH key authentication
- Set up Samba file sharing
- Learned: always use UUIDs in fstab, never device names

### Sessions 9–11 — LiteLLM Integration
**What happened**: Added the unified API gateway so one endpoint works for all models.
- Installed LiteLLM as a Podman container
- Connected Ollama through LiteLLM
- Set up Tailscale VPN for remote access
- Learned: EnvironmentFile must be in [Container] section of quadlet, not [Service]

### Sessions 12–14 — OpenClaw Failure (Database Deadlock)
**What happened**: Attempted to deploy OpenClaw (an AI agent framework with Telegram bot). Failed badly.
- Added Postgres database to LiteLLM for cost tracking
- Database caused a deadlock in the `update_spend` background job
- Every LiteLLM request hung indefinitely
- Three sessions lost to debugging before root cause found
- Fix: removed database entirely. LiteLLM now stateless.
- Learned: never add a database to LiteLLM

### Session 15 — Security Removal + Bug Fix
**What happened**: Discovered serious security CVEs in OpenClaw, removed it. Fixed the EnvironmentFile bug.
- CVEs found: remote code execution, SSH injection, container escape (CVSS 7.8–8.8)
- OpenClaw removed for security reasons
- EnvironmentFile location bug fixed (moved to [Container] section)
- Groq API integration added for free fast cloud models

### Sessions 16–18 — OpenClaw Re-deployment Attempt
**What happened**: Tried re-deploying OpenClaw with security hardening (VPN, firewall, patched version).
- Successfully deployed hardened OpenClaw in Session 18
- Stack was briefly fully operational
- But Groq rate limits discovered as next blocker

### Session 19 — Groq Rate Limit Discovery
**What happened**: Discovered Groq free tier is incompatible with OpenClaw's token usage.
- OpenClaw sends 13,000+ tokens per request
- Groq free tier limits: 6,000–12,000 tokens per minute
- Every interaction failed with 429 rate limit error
- Tried switching models — all too low
- Learned: agent frameworks need far more tokens than free tiers allow

### Session 20 — Stable Baseline Achieved ✅
**What happened**: Removed OpenClaw permanently, declared stable baseline.
- OpenClaw removed (complexity + CVEs + rate limits = not worth it)
- Comprehensive test suite run — all systems verified working
- 7/10 success criteria met
- System declared production-ready
- Next step identified: AnythingLLM as web UI replacement

### Session 21 — AnythingLLM Research + GDM Fix
**Date**: 2026-02-15
**What happened**: Researched AnythingLLM's newer features, planned tutorial, fixed suspend issue.
- Researched AnythingLLM (February 2026): now has MCP support, streaming, real-time URL ingestion
- Compared AnythingLLM vs Claude Projects — both useful, different purposes
- Designed hands-on tutorial plan for AnythingLLM workspaces
- Fixed GDM suspend issue: disabled GDM entirely (headless server doesn't need it)
- Freed ~200-300MB RAM as side benefit
- Next step: Complete the AnythingLLM workspace tutorial

### Session 22 — Logseq + AnythingLLM Workflow Setup
**Date**: 2026-02-19
**Status**: ✅ Completed

**What happened**:
- Reviewed all project documentation and produced a definitive project overview covering the full history from Sessions 1-21
- Designed and created 8 core Logseq pages for the project knowledge base (hub, hardware, architecture, services, commands, decisions, known issues, session log)
- Corrected Samba share path throughout all documentation (`/mnt/hdd/share/` not `/mnt/hdd/`)
- Upgraded AnythingLLM to latest version (v1.11.0) by pulling updated Docker image
- Discovered the correct container launch command requires `-e STORAGE_DIR=/app/server/storage` — without it AnythingLLM warns of data loss
- Discovered hotdir automatic folder watching does not work in the Docker version
- Discovered Live Document Sync is a Desktop-only feature — not available in Docker
- Resolved document upload by using AnythingLLM's web UI upload — all 10 Logseq pages uploaded and assigned to the "Silverblue AI Platform" workspace
- Confirmed RAG is working correctly — tested with "Why was OpenClaw removed?" query, received accurate detailed answer from Decisions.md
- Confirmed AnythingLLM is accessible directly via Tailscale at `http://100.110.112.76:3001` — no SSH tunnel needed
- Discovered LLM settings are reset on container upgrade (v1.11.0 breaking change) — reconfigured LiteLLM connection after upgrade

**Key decisions**:
- Accept manual upload workflow for document sync — pages change infrequently so this is manageable
- Logseq is the source of truth — write there first, upload to AnythingLLM second
- STORAGE_DIR env var must always be set in container launch command
- Future option: install AnythingLLM Desktop on Windows PC for automatic Live Document Sync

**Issues encountered**:
- `ghcr.io/mintplex-labs/anythingllm:master` image pull returned 403 — network access blocked for containers pulling new images. Used existing local image `docker.io/mintplexlabs/anythingllm:latest` instead
- Hotdir mount caused container startup error (`ERR_INVALID_ARG_TYPE`) — removed the mount, hotdir approach abandoned
- LLM settings wiped after upgrade — known breaking change in v1.11.0, reconfigured manually

**Next steps**:
- Consider installing AnythingLLM Desktop on Windows PC for automatic document sync
- Explore AnythingLLM's MCP support for potential future integrations
- Continue building out Logseq knowledge base as project evolves

---

## Related
- [[Decisions]] — major decisions made across sessions
- [[Known Issues]] — issues discovered and resolved across sessions
