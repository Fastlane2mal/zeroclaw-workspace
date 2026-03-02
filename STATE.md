# Silverblue AI Workspace — Platform State

**Last updated:** 2026-03-01  
**Owner:** Bob (primary persona and system orchestrator)  
**Current focus:** Platform stable — Bob operational, GitHub clean, ready for productive work  
**Status:** Tool calling confirmed working via OpenRouter free tier. Bob is default persona.

---

## What's Working

### Infrastructure ✅
- Fedora Silverblue 40 base system
- Ollama (qwen2.5:3b, qwen2.5:1.5b, nomic-embed-text)
- LiteLLM v1.81.12 (Podman quadlet, port 4000, auto-update enabled)
- ZeroClaw v0.1.6 (systemd user service running)
- Git workspace with auto-commit (15 min) and auto-push (1 hour)
- Samba share (\\silverblue-ai\zeroclaw — Windows access)
- GitHub private repo (Fastlane2mal/zeroclaw-workspace) — clean, no secrets
- SSH key auth for GitHub

### LiteLLM Configuration ✅
- Primary (default): gpt-oss-20b:free + gpt-oss-120b:free via OpenRouter — free, ZeroClaw tool calling compatible
- Fallback 1 (groq): 2x Groq llama-3.3-70b-versatile — conversational fallback only
- Fallback 2 (gemini): 3x Gemini 2.5 Flash — last resort
- Fallback chain: openrouter free → groq → gemini
- NOTE: Groq and Gemini incompatible with ZeroClaw tool calling
- NOTE: OpenRouter privacy settings must have free endpoint options enabled
- NOTE: Multiple OpenRouter accounts can be pooled — add OPENROUTER_API_KEY_2 entries to config

### Persona System ✅
- Bob is default persona and system orchestrator
- SOUL.md updated — Bob is default, not neutral coordinator
- Other personas archived to personas/archive/
- Tool calling confirmed working ✅
- Bob reading/writing workspace files via Telegram ✅

### Bob Optimisation ✅
- BOB.md trimmed and updated with standard diagnostic, session start git check, secret hygiene rules
- RUNBOOK.md created — 10 procedures covering all common platform tasks
- QUICK-REFERENCE.md updated with key rotation command

### GitHub ✅
- Secrets purged from history using git-filter-repo via toolbox
- Force push succeeded — no secrets violation
- Groq and Anthropic API keys rotated
- projects/dev-project/docs/config.yaml added to .gitignore

---

## Current Blockers

- Bob cannot execute `systemctl` commands — policy blocked in ZeroClaw config
  - Needs investigation: check config.toml for command restrictions
  - Impacts: standard diagnostic routine, session start health check

---

## What's Next

### Immediate
- [ ] Investigate `systemctl` policy block in ZeroClaw config.toml
- [ ] Test Bob's standard diagnostic routine end-to-end
- [ ] Test Bob's session start routine (fresh session)
- [ ] Verify Bob can read RUNBOOK.md
- [ ] Update SOUL.md to reflect Bob as default with others archived
- [ ] Add second OpenRouter account key to LiteLLM config (OPENROUTER_API_KEY_2)

### Phase 8: Profile Population — DEFERRED
Reason: Other personas shelved. Resume when personas are reactivated.

### When Ready to Reactivate Personas
- Restore persona files from personas/archive/
- Populate shared profile files via VS Code
- Run Last.fm/Setlist.fm ingestion script for music-profile.md

---

## Personas

| Persona | Status | Location |
|---------|--------|----------|
| Bob | ✅ Active (default) | personas/BOB.md |
| Frank | Archived | personas/archive/FRANK.md |
| Penny | Archived | personas/archive/PENNY.md |
| Len | Archived | personas/archive/LEN.md |
| Ziggy | Archived | personas/archive/ZIGGY.md |
| Joy | Archived | personas/archive/JOY.md |

---

## Platform Phases

| Phase | Description | Status |
|-------|-------------|--------|
| 0-7 | Infrastructure, personas, LiteLLM | ✅ Complete |
| 8 | Profile population | ⏸ Deferred |
| 9 | Frank full implementation | ⏸ Deferred |
| 10 | AnythingLLM integration | ⏸ Deferred |
| 11-14 | Len, Ziggy, Penny, Joy | ⏸ Deferred |
| 15 | Google Calendar MCP | ⏸ Deferred |
