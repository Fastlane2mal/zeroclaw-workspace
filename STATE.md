# Silverblue AI Workspace — Platform State

**Last updated:** 2026-02-28  
**Owner:** Bob (primary persona and system orchestrator)  
**Current focus:** Platform stable — Bob operational, ready for productive work  
**Status:** Tool calling confirmed working via OpenRouter. Bob is default persona.

---

## What's Working

### Infrastructure ✅
- Fedora Silverblue 40 base system
- Ollama (qwen2.5:3b, qwen2.5:1.5b, nomic-embed-text)
- LiteLLM (Podman quadlet, port 4000) — OpenRouter/Groq/Gemini config
- ZeroClaw v0.1.6 (systemd user service running)
- Git workspace with auto-commit (15 min) and auto-push (1 hour)
- Samba share (Windows access for VS Code/AnythingLLM)
- GitHub private repo (Fastlane2mal/zeroclaw-workspace)
- SSH key auth for GitHub

### LiteLLM Configuration ✅
- Version: 1.81.12 (auto-update enabled via podman-auto-update.timer)
- Primary (default): gpt-oss-20b:free + gpt-oss-120b:free via OpenRouter — free, ZeroClaw compatible
- Fallback 1 (groq): 2x Groq llama-3.3-70b-versatile — round-robin pool
- Fallback 2 (gemini): 3x Gemini 2.5 Flash — round-robin pool, last resort
- Fallback chain: openrouter free → groq → gemini
- NOTE: Groq and Gemini incompatible with ZeroClaw tool calling
- NOTE: OpenRouter privacy settings must have free endpoint options enabled
- port/host: set in container Exec command (--port 4000 --host 0.0.0.0)
- master_key: auto-read from LITELLM_MASTER_KEY environment variable

### Persona System ✅
- SOUL.md at workspace root — neutral coordinator with persona switching
- Bob is the only active persona — all others archived to personas/archive/
- Bob's persona file: personas/BOB.md ✅
- Tool calling confirmed working via OpenRouter ✅
- Bob can read/write workspace files via Telegram ✅

---

## Key Learnings This Session

- Groq (llama-3.3-70b) incompatible with ZeroClaw tool calling — outputs raw tool syntax instead of executing
- Gemini incompatible with ZeroClaw tool calling for the same reason
- ZeroClaw tool calling requires Claude-compatible format
- OpenRouter auto router confirmed working — routes to free models that support tool calling
- OpenRouter free tier requires $10 lifetime credit purchase for 1000 req/day limit
- Gemini free tier rate limits are per project (~250 req/day) — 3 keys across 3 projects = ~750/day but fragile
- Groq is better than Gemini as a fallback but neither can execute ZeroClaw tools
- If OpenRouter free tier becomes unreliable, Claude Haiku via OpenRouter is the fix (~fractions of a penny per message)

---

## What's Next

### Immediate — Bob Productive Work
- [ ] Verify projects/dev-project/STATE.md and TODO.md contents
- [ ] Update dev-project state files to reflect current platform status
- [ ] Use Bob for Phase 8 tasks that don't require other personas

### Phase 8: Profile Population — DEFERRED
**Reason:** Other personas shelved. Profiles only needed when Frank, Ziggy, Joy etc. are reactivated.  
**Exception:** shared/user-profile.md is useful for Bob context but not essential.

### When Ready to Reactivate Personas
- Restore persona files from personas/archive/
- Populate shared profile files via VS Code
- Run Last.fm/Setlist.fm ingestion script for music-profile.md
- Phase 9 onwards resumes

### Phase 15: Google Calendar Integration
**Status:** Research complete, Node.js install pending  
**Prerequisites:** Phases 8-14 complete — deferred

---

## Current Blockers

None. Bob is operational and ready for work.

---

## Recent Changes

### 2026-02-28 (Session 11)
- Simplified strategy: Bob-only persona, all others archived
- Discovered Groq/Gemini incompatible with ZeroClaw tool calling
- Switched to openrouter/auto as primary — tool calling confirmed working
- Simplified LiteLLM config: removed desktop PC Ollama, local Ollama
- Final fallback chain: openrouter/auto → groq → gemini
- Resolved Bob persona file path issue (personas/BOB.md, uppercase)
- Profile population deferred — not needed until other personas reactivated
- Bob confirmed reading/writing files correctly via Telegram ✅

### 2026-02-27 (Session 10)
- Desktop PC Ollama added as primary (since removed — simplified)
- Named model groups: ollama-pc, cloud, local (since replaced)
- LiteLLM upgraded to v1.81.12; auto-update timer enabled

### 2026-02-26 (Session 9)
- Three Gemini API keys configured as round-robin pool
- Two Groq API keys configured as fallback pool
- Root cause fixed: quoted API key values causing %22 URL encoding
- Fixed duplicate general_settings in config.yaml

---

## Next Session Tasks

**For User:**
1. Save updated project files and ask Bob to read them
2. Give Bob a real task — Last.fm/Setlist.fm ingestion script is a good first job

**For Claude (next session):**
1. Verify Bob reading updated project files correctly
2. Assign Bob productive work

---

## Key Learnings (Cumulative)

- ZeroClaw tool calling requires Claude-compatible format — Groq/Gemini/Llama models output raw syntax
- OpenRouter auto router works with ZeroClaw tool calling on free tier
- API key values must be unquoted in ~/.silverblue-ai-config
- os.environ/ is correct format for config.yaml env var references
- Duplicate general_settings blocks — later block silently overrides earlier
- model_group_alias alone doesn't resolve fallbacks — explicit entry needed
- rate_limits is not a valid top-level LiteLLM config key
- file_read paths are relative to workspace root — never absolute
- SOUL.md loads from workspace root
- [[tools]] not needed in SKILL.toml for ZeroClaw built-ins
- Explicit file_read syntax + MANDATORY heading required for reliable on-activation reads
- health-profile.md must be gitignored (never committed to GitHub)
- Gemini free tier quota is per project (~250 req/day) — fragile for heavy use
- OpenRouter $10 lifetime credit unlocks 1000 free req/day
