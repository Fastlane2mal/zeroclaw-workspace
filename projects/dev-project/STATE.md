# Silverblue AI Workspace — Development State

**Last updated:** 2026-02-24  
**Current phase:** Phase 5 — Persona switching mechanism  
**Status:** Research phase

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
- Clean folder layout: personas/, projects/, shared/
- All six personas defined (FRANK, PENNY, BOB, LEN, ZIGGY, JOY)
- Shared profile templates created (user, dietary, music, location, travel)
- Project folders initialised for all personas
- health-profile.md gitignored (local only)

### Configuration ✅
- config.toml: max_tokens=4096
- http_request allowed_domains = ["*"] (wildcard — fixed from https://bbc.co.uk)
- SSH key auth for GitHub
- systemd timers for auto-commit/push

---

## What's Not Working / In Progress

### Phase 5: Persona Switching ⬅️ CURRENT FOCUS
- [ ] Read ZeroClaw Skills system documentation (SKILL.toml)
- [ ] Find example SKILL.toml files in ZeroClaw repo
- [ ] Read AIEOS identity framework specs (SOUL.md / IDENTITY.md)
- [ ] Examine identity.format = "openclaw" behaviour
- [ ] Compare approaches: Skills vs SOUL.md vs hybrid
- [ ] Write test SKILL.toml for Frank
- [ ] Test proof-of-concept — activate Frank via Telegram
- [ ] Document chosen approach in DECISIONS.md

### Phase 6: Frank (Meal Planner) — BLOCKED on Phase 5
- [ ] Verify food.db accessible in projects/meal-planner/
- [ ] Test SQLite database access from ZeroClaw
- [ ] Create pantry reading capability
- [ ] Test meal plan generation
- [ ] Set up Sunday 3:30pm cron trigger
- [ ] Verify shopping list format and output location

### Not Yet Started
- Phase 7: Logseq setup
- Phase 8: AnythingLLM connection
- Phases 9–12: Len, Penny, Ziggy, Joy activation

---

## Current Blockers

**Phase 5 blocker:** Persona switching mechanism not yet researched or implemented.
- Don't know if Skills (SKILL.toml), SOUL.md/IDENTITY.md, or a combination is correct
- This blocks all persona implementations (Phases 6–12)

**Action required:** Read ZeroClaw repo documentation before making any decisions.

---

## Recent Changes

### 2026-02-24
- Created all six persona definitions (FRANK, PENNY, BOB, LEN, ZIGGY, JOY)
- Created shared profile templates (music, travel, dietary, location, user)
- Added Joy as sixth persona (travel planner)
- Added projects/travel-planning/ with /trips, /ideas, /research structure
- Decided to use dev-project/ for platform development tracking (meta-project)
- Created dev-project/ folder structure (STATE.md, TODO.md, SESSIONS.md)

### 2026-02-23
- Upgraded ZeroClaw v0.1.1 → v0.1.6 (built from git tag, not main)
- Fixed config.toml allowed_domains (removed https:// prefix, changed to wildcard)
- Completed workspace restructure (clean slate)
- Migrated food.db, schema.sql, seed_data.sql to projects/meal-planner/
- Migrated FRANK_PERSONA.md to personas/
- Migrated Song Tutor/role.md to projects/song-tutor/

---

## Next Session Tasks

1. SSH into Silverblue, navigate to ~/.zeroclaw/workspace/projects/dev-project/
2. Confirm this file structure is in place
3. Read ZeroClaw Skills documentation (`zeroclaw skills --help` or repo docs)
4. Find and examine example SKILL.toml files in ZeroClaw repo
5. Read AIEOS identity format specification
6. Compare: Skills vs SOUL.md — which fits six-persona use case better?
7. Document findings in research/phase5-persona-switching.md
8. Record decision in root DECISIONS.md

---

## Open Questions

- Skills vs SOUL.md vs hybrid approach for persona switching?
- Can personas share conversation context or must each start fresh?
- Is there a default persona, or is activation always explicit?
- Do scheduled tasks (Frank's Sunday cron) use the persona system?
- How do we test personas without spamming the Telegram channel?
- Can Joy and Ziggy coordinate (trip + concert planning)?
