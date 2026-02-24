# Silverblue AI Workspace — Development State

**Last updated:** 2026-02-24  
**Current phase:** Phase 6 (reordered) — Bob operational, project self-managed from workspace  
**Status:** In progress

---

## What's Working

### Infrastructure ✅
- Fedora Silverblue 40 base system
- Ollama (qwen2.5:3b, qwen2.5:1.5b, nomic-embed-text)
- LiteLLM (Claude Haiku via API gateway, Podman quadlet, port 4000)
- ZeroClaw v0.1.6 (upgraded from v0.1.1, systemd user service running)
- Git workspace with auto-commit (15 min) and auto-push (1 hour)
- Samba share (Windows access for Logseq/AnythingLLM)
- GitHub private repo (Fastlane2mal/zeroclaw-workspace)
- SSH key auth for GitHub

### Workspace Structure ✅
- Clean folder layout: personas/, projects/, shared/, skills/
- All six personas defined (FRANK, PENNY, BOB, LEN, ZIGGY, JOY)
- Shared profile templates created (user, dietary, music, location, travel)
- Project folders initialised for all personas
- health-profile.md gitignored (local only)

### Configuration ✅
- config.toml: max_tokens=4096
- http_request allowed_domains = ["*"]
- SSH key auth for GitHub
- systemd timers for auto-commit/push

### Phase 5: Persona Switching ✅
- SOUL.md at workspace root — neutral coordinator base identity
- workspace/skills/personas/ — single skill handling all six personas
- Trigger phrases working: "Hey Frank", "@ziggy", "Back to normal", etc.
- Frank activates, reads persona file, responds in character ✅
- Ziggy activates, auto-triggers web_search, responds in character ✅
- "Back to normal" returns to neutral coordinator ✅

### Bob (Dev Assistant) ✅
- BOB.md operational instructions added (reads STATE.md, TODO.md on activation)
- Bob can now manage this project from within the workspace via Telegram

---

## What's In Progress

### Current Focus — Bob operational + project self-managed ⬅️

- [ ] Create dev-project/docs/ and dev-project/scripts/ subdirectories on Silverblue
- [ ] Test Bob via Telegram: "Hey Bob" → verify he reads STATE.md and TODO.md
- [ ] Confirm Bob can update STATE.md and SESSIONS.md directly
- [ ] Establish dual-mode workflow: Bob via Telegram for day-to-day, Claude for complex sessions

### Deferred — Remaining persona operational instructions
- [ ] Add operational instructions block to PENNY.md
- [ ] Add operational instructions block to LEN.md
- [ ] Add operational instructions block to ZIGGY.md
- [ ] Add operational instructions block to JOY.md

### Deferred — Frank core implementation (original Phase 6)
- [ ] Complete shared/dietary-profile.md with real Malcolm + Jen data
- [ ] Verify food.db accessible and readable by ZeroClaw
- [ ] Test full meal plan generation end-to-end
- [ ] Set up Sunday 3:30pm cron trigger

### Not Yet Started
- Phase 7: Logseq setup
- Phase 8: AnythingLLM connection
- Phases 9–12: Len, Penny, Ziggy, Joy full activation

---

## Current Blockers

None.

---

## Dual-Mode Workflow

This project is now managed from two places:

| Tool | Best for |
|------|----------|
| Bob via Telegram (ZeroClaw) | Day-to-day tasks, quick file edits, running commands, updating STATE.md/SESSIONS.md |
| Claude (claude.ai) | Complex planning, architecture decisions, generating larger files, multi-step reasoning |

Bob reads STATE.md and TODO.md on every activation — always knows where things stand.
Claude sessions should start by pasting SESSION_OPENER.md for full context.

---

## Recent Changes

### 2026-02-24
- **Phase 5 complete** — persona switching fully implemented and tested
- Created workspace/SOUL.md
- Created workspace/skills/personas/SKILL.toml and SKILL.md
- Added operational instructions to FRANK.md and BOB.md
- Switched priority: Bob operational before Frank implementation
- Decided to run Bob (Telegram) and Claude in parallel — complementary, not competing

### 2026-02-23
- Upgraded ZeroClaw v0.1.1 → v0.1.6
- Fixed config.toml allowed_domains
- Completed workspace restructure
- Migrated meal planner files

---

## Next Session Tasks

1. Create dev-project/docs/ and dev-project/scripts/ on Silverblue
2. Test Bob via Telegram — "Hey Bob, read STATE.md and tell me what's next"
3. Verify Bob can write back to STATE.md and SESSIONS.md
4. If working: hand off day-to-day tracking to Bob
5. Return here (Claude) for Frank implementation planning
