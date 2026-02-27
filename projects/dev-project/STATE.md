# Silverblue AI Workspace — Development State

**Last updated:** 2026-02-26  
**Current phase:** Phase 8 (profile population) — ready to proceed  
**Status:** LiteLLM multi-key config complete; Gemini/Groq quotas reset tomorrow

---

## What's Working

### Infrastructure ✅
- Fedora Silverblue 40 base system
- Ollama (qwen2.5:3b, qwen2.5:1.5b, nomic-embed-text)
- LiteLLM (Podman quadlet, port 4000) — multi-key pool config
- ZeroClaw v0.1.6 (systemd user service running)
- Git workspace with auto-commit (15 min) and auto-push (1 hour)
- Samba share (Windows access for VS Code/AnythingLLM)
- GitHub private repo (Fastlane2mal/zeroclaw-workspace)
- SSH key auth for GitHub

### LiteLLM Configuration ✅
- Version: 1.81.12 (auto-update enabled via podman-auto-update.timer)
- Primary (ollama-pc): qwen2.5:7b-instruct on desktop PC at 192.168.0.10:11434
- Fallback 1 (cloud): 3x Gemini 2.5 Flash + 2x Groq llama-3.3-70b — round-robin pool
- Fallback 2 (local): qwen2.5:3b + qwen2.5:1.5b on localhost Ollama
- Haiku available explicitly but not in auto fallback chain
- model_group_alias: default → ollama-pc
- Fallback chain: ollama-pc → cloud → local
- port/host: set in container Exec command (--port 4000 --host 0.0.0.0)
- master_key: auto-read from LITELLM_MASTER_KEY environment variable

### Persona System ✅
- SOUL.md at workspace root — neutral coordinator
- workspace/skills/personas/ — single skill, all six personas
- All six personas operational with MANDATORY FIRST STEP protocol
- Frank, Ziggy, neutral mode confirmed working in testing
- Bob self-managing project from workspace via Telegram ✅

### Dual-Mode Workflow ✅
- Bob (Telegram): day-to-day tasks, file edits, quick commands, status updates
- Claude (claude.ai): planning, architecture, generating larger content

---

## What's Next

### Phase 8: Profile Population ⬅️ CURRENT FOCUS

**Status:** Ready — VS Code setup complete, profiles need populating

**Editor:** VS Code (open `\\silverblue-ai\zeroclaw\workspace` as a folder)
**Knowledge base:** AnythingLLM covers this — no Logseq needed

**User Tasks:**
- [ ] shared/dietary-profile.md — Malcolm & Jen preferences
- [ ] shared/location.md — South Shields, seasonal produce
- [ ] Verify health-profile.md gitignored, then populate (local only)
- [ ] shared/music-profile.md — musical taste, gig preferences
- [ ] shared/travel-profile.md — travel style, budget, past trips
- [ ] shared/user-profile.md — general household info
- [ ] projects/meal-planner/pantry.md — current kitchen inventory

### Phase 9: Frank (Meal Planner) Full Implementation

**Prerequisites:** Phase 8 complete

#### Core
- [ ] Test Frank reading pantry.md
- [ ] Test Frank reading dietary-profile.md
- [ ] Test full meal plan generation end-to-end
- [ ] Verify meal_plan.md saved to meal-planner/
- [ ] Verify shopping_list.md saved to meal-planner/

#### Recipe Research (new feature)
- [ ] Add recipe research workflow to FRANK.md
- [ ] Frank fetches from diabetes.org.uk/living-with-diabetes/eating/recipes
- [ ] Frank fetches from bbc.co.uk/food
- [ ] Cross-reference with dietary-profile.md
- [ ] Filter disliked ingredients (Malcolm: raw tomatoes / Jen: uncooked cheese)
- [ ] Save shortlist to projects/meal-planner/new-recipes.md

#### Automation
- [ ] Investigate ZeroClaw cron payload format
- [ ] Set up Sunday 3:30pm cron job
- [ ] Test scheduled execution end-to-end

---

## Phase 15: Google Calendar Integration

**Status:** Research complete, Node.js install pending

**Guide:** phase-15-calendar-implementation.md

**Prerequisites:** Phases 8-14 complete

---

## Not Yet Started
- Phase 10: AnythingLLM connection
- Phases 11-14: Len, Ziggy, Penny, Joy full activation
- Phase 15: Google Calendar Integration

---

## Current Blockers

None. Gemini/Groq quotas exhausted today from debugging — reset tomorrow morning.

---

## Recent Changes

### 2026-02-27 (Session 10)
- Desktop PC Ollama added as primary model (qwen2.5:7b-instruct at 192.168.0.10:11434)
- Windows Firewall rule added for port 11434; OLLAMA_HOST=0.0.0.0 set on Windows
- Switched to named model groups: ollama-pc, cloud, local
- Gemini and Groq combined into single cloud pool
- Removed redundant default fallback entry and invalid fallback_on_rate_limit parameter
- Confirmed port/master_key handled externally — server_settings not needed
- LiteLLM upgraded to v1.81.12; auto-update timer enabled

### 2026-02-26 (Session 9)
- Three Gemini API keys configured as round-robin pool (GOOGLE_API_KEY_1/2/3)
- Two Groq API keys configured as fallback pool (GROQ_API_KEY_1/2)
- Root cause fixed: quoted API key values in ~/.silverblue-ai-config causing %22 URL encoding
- Confirmed os.environ/ is correct LiteLLM format
- Fixed duplicate general_settings in config.yaml
- Fixed YAML syntax error in fallbacks section
- model_group_alias maps default → gemini-flash pool
- Explicit fallback entries for both gemini-flash and default
- Rate limits moved to per-deployment rpm/tpm in litellm_params
- Ollama timeout increased to 120s
- All three gemini-flash entries confirmed loading ✅
- 200 OK responses confirmed ✅

### 2026-02-26 (Session 8)
- Session 8 complete — Calendar MCP researched, Node.js options evaluated, Logseq replaced, LiteLLM fixed
- Selected `@cocal/google-calendar-mcp` as MCP server (nspady, 964 stars)
- Confirmed Node.js not installed; rpm-ostree recommended; decision deferred
- Replaced Logseq with VS Code; confirmed AnythingLLM covers knowledge base
- Fixed LiteLLM config: added Gemini 2.0 Flash as primary, Groq/Haiku/Ollama fallback chain
- Resolved 401 auth error — LITELLM_MASTER_KEY now wired into ZeroClaw config.toml
- Gemini free tier rate limit hit during testing — fallback to Groq confirmed working
- Identified Last.fm + Setlist.fm as music-profile.md data sources; Python script planned

### 2026-02-25 (Session 7)
- Created logseq-fresh-start.md with step-by-step reset instructions
- Created profile-templates.md with all 7 file templates
- Designed Phase 15 Google Calendar integration via MCP (~3 hours)
- Documented Joy/Ziggy/Frank calendar capabilities
- Identified future MCP extensions (Gmail, Drive, Contacts, Spotify)
- Updated all project files

### 2026-02-24
- Phases 5, 6, 7 complete — persona switching, Bob operational, all personas updated
- Promoted Logseq to Phase 8 (before Frank) — needed for editing shared profiles
- Added Frank recipe research feature to Phase 9 plan
- Switched pantry from SQLite (food.db) to markdown (pantry.md)
- Deleted food.db, schema.sql, seed_data.sql
- Frank's MANDATORY FIRST STEP updated to reference pantry.md
- All decisions recorded in root DECISIONS.md

---

## Next Session Tasks

**For User:**
1. Verify Gemini keys working after quota reset (send message to Bob in Telegram)
2. Populate remaining profile files via VS Code
3. Decide Node.js install method for Phase 15

**For Claude (next session):**
1. Verify profiles populated
2. Write Last.fm/Setlist.fm Python ingestion script for music-profile.md
3. Begin Phase 15 Node.js + Google Cloud setup

## Key Learnings

- API key values must be unquoted in ~/.silverblue-ai-config — LiteLLM URL-encodes quoted values
- os.environ/ is the correct format for config.yaml env var references
- Duplicate general_settings blocks — later block silently overrides earlier
- model_group_alias alone doesn't resolve fallbacks — explicit entry needed per group name
- rate_limits is not a valid top-level LiteLLM config key — use rpm/tpm per deployment
- file_read paths are relative to workspace root — never absolute
- SOUL.md loads from workspace root
- [[tools]] not needed in SKILL.toml for ZeroClaw built-ins
- Explicit file_read syntax + MANDATORY heading required for reliable on-activation reads
- Bob can self-correct his own persona file
- VS Code is the right editor for the workspace — open Samba share as a folder
- MCP servers are the proper way to integrate external data sources
- health-profile.md must be gitignored (never committed to GitHub)
