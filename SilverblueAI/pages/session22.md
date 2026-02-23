# Decisions — Session 22 Additions

**Purpose**: New decisions made in Session 22 — append to DECISIONS.md  
**Date**: 2026-02-20  
**Version**: v2026.02b

Add the following entries to the relevant sections of DECISIONS.md.

---

## New Decision: ZeroClaw as Agent Framework

**Date**: 2026-02-20 (Session 22)  
**Decision**: Deploy ZeroClaw as primary AI agent interface  
**Status**: ✅ Active — deployed and running

**Rationale**:
- OpenClaw original: 400MB runtime, CVEs unresolved, uncertain governance (creator joined OpenAI, project handed to foundation)
- ZeroClaw: ~3.4MB binary, <5MB RAM, Rust-based (memory safe), built-in security model
- ZeroClaw token usage (~2-4k/request) compatible with Groq free tier, unlike OpenClaw (13k+)
- Native Ollama integration — no LiteLLM required for local inference
- Active development, 14k+ GitHub stars, MIT license

**Alternatives considered**:
- **NanoClaw**: Good security model, Telegram-only, routes via OpenRouter (cloud cost). Rejected — no native Ollama.
- **PicoClaw + PicoLM**: Excellent for $10 SBC hardware, 1B model limit, 1-10 tok/s. Rejected — designed for lower-spec hardware than we have.
- **IronClaw**: Heavy (PostgreSQL + pgvector), complex. Rejected — adds dependencies we don't need.
- **NanoBot**: 21.6k stars but Python, basic security. Not selected — ZeroClaw's security model is stronger.

**Trade-offs**:
- ✅ Negligible RAM impact (<5MB)
- ✅ Compatible with Groq free tier (leaner prompts)
- ✅ Security: sandbox, allowlists, pairing approval
- ✅ Multi-channel (Telegram, Discord, CLI, webhook)
- ⚠️ New project (Feb 2026) — less battle-tested than older options
- ⚠️ Rust build required (3-8 min compile, one-time)

**Outcome**: Deployed successfully. See ZEROCLAW_DEPLOYMENT.md.

---

## New Decision: AnythingLLM Moved to Windows PC

**Date**: 2026-02-20 (Session 22)  
**Decision**: Remove AnythingLLM from server, run on Windows 11 PC instead  
**Status**: ✅ Complete

**Rationale**:
- User already has AnythingLLM installed on Windows 11
- Windows instance is superior: more RAM, faster SSD, GPU for embeddings, closer to user
- Server AnythingLLM used ~300-800MB RAM for a service better suited to the client machine
- Freeing that RAM gives ZeroClaw and LiteLLM more headroom

**Implementation**:
- Server container stopped and removed (data preserved)
- Windows AnythingLLM connected to server LiteLLM via Tailscale (100.110.112.76:4000)
- Server data at `/mnt/hdd/projects/anythingllm-storage` — reinstall anytime if needed

**Trade-offs**:
- ✅ ~300-800MB RAM freed on server
- ✅ Better AnythingLLM experience on Windows (GPU embeddings, faster)
- ✅ Server data preserved (not deleted)
- ⚠️ AnythingLLM no longer available headless from server alone
- ⚠️ Requires Windows PC to be on for AnythingLLM access (acceptable — that's the primary workstation)

**Outcome**: Clean removal, Windows instance working, server resources improved.

---

## New Decision: qwen2.5:3b as Primary Agent Model

**Date**: 2026-02-20 (Session 22)  
**Decision**: Replace smollm2 (1.7B) with qwen2.5:3b as primary local model  
**Status**: ✅ Active

**Rationale**:
- smollm2 optimised for speed/size, not instruction-following
- Agent frameworks require reliable tool calling and multi-step reasoning
- qwen2.5:3b significantly better at instruction-following, tool use, JSON output
- Fits comfortably in available RAM after AnythingLLM removal
- qwen2.5 series specifically trained for agentic tasks

**Trade-offs**:
- ✅ Much better tool use and instruction following
- ✅ More reliable JSON output (critical for agent tool calling)
- ⚠️ Slower: 15-25s vs 10-15s for smollm2
- ⚠️ Larger: ~2GB vs ~1GB model file

**Speed fallback**: qwen2.5:1.5b retained for simple/fast queries where response quality is less critical.

**Outcome**: Deployed and tested. LiteLLM config updated.

---

## Updated Decision: OpenClaw Derivatives Assessment

**Date**: 2026-02-20 (Session 22)  
**Decision**: ZeroClaw selected from OpenClaw derivative ecosystem  
**Status**: ✅ Documented

**Ecosystem summary (Feb 2026)**:
- OpenClaw original: 430k lines, 400MB, CVEs, Steinberger joined OpenAI (project future uncertain)
- ZeroClaw: Rust, 3.4MB, <5MB RAM, built-in security, Ollama native → **SELECTED**
- NanoClaw: Python, 3k lines, good security (FileGuard/ShellSandbox/PromptGuard), Telegram+OpenRouter
- PicoClaw + PicoLM: Go+C, for $10 SBC hardware, 1-10 tok/s, interesting but underpowered for our use
- IronClaw: Rust, PostgreSQL+pgvector, heavy dependencies
- NanoBot: Python, 21.6k stars, multi-platform (Telegram/Discord/WhatsApp/Slack)
- memU: Memory-focused framework, not an agent itself
- bitdoze-bot: Agno teams, multi-agent, small community

**PicoLM note**: Technically impressive (~80KB C binary, 45MB RAM for 1B model via memory-mapped layers). Designed for embedded/IoT use. Worth monitoring for Pi 5 sidecar use case in future. Not suitable as primary agent on i5-8250U — model quality too limited.

---

*Append these entries to DECISIONS.md — under "Interface Decisions" for ZeroClaw/AnythingLLM entries, and under "AI Stack Decisions" for the model selection entry.*
