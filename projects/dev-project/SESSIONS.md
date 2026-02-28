# Development Sessions — Silverblue AI Workspace

Log of Claude sessions working on the platform. Most recent session first.

---

## Session 11 — 2026-02-28

**Focus:** Simplification — Bob-only persona, LiteLLM stripped back, tool calling fixed

### Completed
- Reassessed strategy — decided to focus on single working persona (Bob) before expanding
- Simplified LiteLLM config — removed desktop PC Ollama and local Ollama tiers
- Started with Groq as primary — confirmed tool calling broken (raw syntax output)
- Investigated Gemini — confirmed same tool calling incompatibility
- Identified root cause: ZeroClaw requires Claude-compatible tool call format; Llama-based models incompatible
- Switched to OpenRouter auto router as primary — free models with tool calling support
- Confirmed OpenRouter $10 lifetime credit unlocks 1000 free req/day permanently
- Confirmed tool calling working — Bob reading/writing files via Telegram ✅ (slightly slow but functional)
- Resolved Bob persona file path issue — file is at personas/BOB.md (uppercase)
- Confirmed other personas archived to personas/archive/ by Bob
- Deferred profile population — not needed until other personas reactivated
- Updated all project files

### Key Decisions
- openrouter/auto as primary — only confirmed ZeroClaw-compatible free option
- Groq/Gemini demoted to fallback — conversational only, no tool calling
- Bob-only persona until platform fully stable
- Profile population deferred — no value without other personas active
- Claude Haiku via OpenRouter is upgrade path if free tier becomes unreliable

### Issues Encountered
- Groq llama-3.3-70b outputs raw tool call syntax — ZeroClaw tool calling broken
- Gemini same issue — not Claude-compatible tool format
- Bob persona file uppercase (BOB.md) caused path resolution failure
- OpenRouter auto router slightly slow — expected on free shared infrastructure

### Final config.yaml structure
- Primary (default): openrouter/auto via OpenRouter API
- Fallback 1 (groq): 2x Groq llama-3.3-70b-versatile
- Fallback 2 (gemini): 3x Gemini 2.5 Flash
- Fallback chain: openrouter/auto → groq → gemini

### Additional Findings (Session 11 continued)
- openrouter/auto charges — routes to paid models
- openrouter/free invalid model ID format
- Kimi K2 has no free tier on OpenRouter
- gpt-oss-120b:free and gpt-oss-20b:free exist but blocked by OpenRouter privacy settings
- Enabling "free endpoints that may train on inputs" and "free endpoints that may publish prompts" in OpenRouter privacy settings unlocked free models
- gpt-oss-20b:free confirmed working — cost:0, OpenAI-format tool calling, ZeroClaw compatible
- Final config: gpt-oss-20b:free + gpt-oss-120b:free in default group, groq + gemini as fallbacks

### Next Session
1. Assign Bob first productive task — Last.fm/Setlist.fm ingestion script for shared/music-profile.md
2. Use Bob for ongoing platform work and troubleshooting
3. Trim BOB.md — too large, causing Groq token limit errors on fallback

---

## Session 10 — 2026-02-27

**Focus:** LiteLLM config finalisation — desktop PC as primary, named groups, fallback chain

### Completed
- Added desktop PC Ollama (qwen2.5:7b-instruct at 192.168.0.10:11434) as primary
- Switched to named model groups (ollama-pc, cloud, local) with explicit fallbacks
- Combined Gemini 3-key pool and Groq 2-key pool into single cloud group
- Upgraded LiteLLM to v1.61.12; enabled podman-auto-update.timer
- *(Config since superseded by Session 11 simplification)*

---

## Session 9 — 2026-02-26

**Focus:** LiteLLM multi-key configuration and debugging

### Completed
- Added three Gemini API keys as round-robin pool
- Added two Groq API keys as fallback pool
- Diagnosed root cause: quoted values in ~/.silverblue-ai-config causing %22 URL encoding
- Fixed duplicate general_settings sections in config.yaml
- Confirmed 200 OK responses working ✅

---

## Session 8 — 2026-02-25

**Focus:** Phase 15 Calendar MCP research, Node.js planning, Logseq → VS Code switch

### Completed
- Selected @cocal/google-calendar-mcp as MCP server
- Evaluated Node.js installation options; rpm-ostree recommended
- Replaced Logseq with VS Code as workspace editor
- Fixed LiteLLM config — resolved 401 auth error
- Identified Last.fm + Setlist.fm as music-profile.md data sources

---

## Session 7 — 2026-02-25

**Focus:** Logseq setup planning & Google Calendar integration design

### Completed
- Created all 7 profile templates
- Designed Phase 15 Google Calendar integration via MCP
- Created logseq-fresh-start.md, profile-templates.md, phase-15-calendar-implementation.md

---

## Session 6 — 2026-02-24

**Focus:** Phase 7 — MANDATORY FIRST STEP protocol, all personas updated

### Completed
- Fixed on-activation read issue: explicit file_read syntax + MANDATORY heading required
- All six personas now read domain files before every response ✅

---

## Session 5 — 2026-02-24

**Focus:** Bob confirmed operational, dual-mode workflow live

### Completed
- Diagnosed file_read path issue (relative to workspace root)
- Bob read STATE.md, created directories, wrote SESSIONS.md ✅
- Dual-mode workflow confirmed live

---

## Session 4 — 2026-02-24

**Focus:** Bob operational + priority switch to Bob before Frank

---

## Session 3 — 2026-02-24

**Focus:** Phase 5 — persona switching fully implemented and tested

---

## Session 2 — 2026-02-24

**Focus:** dev-project/ folder structure created

---

## Session 1 — 2026-02-24

**Focus:** All six persona definitions and shared profile templates created

---

## Session 0 — 2026-02-23

**Focus:** Infrastructure — ZeroClaw upgrade, workspace restructure, git automation
