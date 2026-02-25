# Silverblue AI Workspace — Development State

**Last updated:** 2026-02-25  
**Current phase:** Phase 8 — Logseq setup  
**Status:** Ready to start (guides complete)

---

## What's Working

### Infrastructure ✅
- Fedora Silverblue 40 base system
- Ollama (qwen2.5:3b, qwen2.5:1.5b, nomic-embed-text)
- LiteLLM (Claude Haiku via API gateway, Podman quadlet, port 4000)
- ZeroClaw v0.1.6 (systemd user service running)
- Git workspace with auto-commit (15 min) and auto-push (1 hour)
- Samba share (Windows access for Logseq/AnythingLLM)
- GitHub private repo (Fastlane2mal/zeroclaw-workspace)
- SSH key auth for GitHub

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

### Phase 8: Logseq Setup ⬅️ CURRENT FOCUS

**Status:** Documentation complete, ready for user implementation

**Why Logseq First:**
- Shared profiles need filling in with real data
- Editing markdown tables in terminal is impractical
- Logseq on Windows reads/writes workspace via Samba
- Frank's recipe research needs dietary-profile.md populated
- Once profiles filled, all personas can reference them

**Available Guides:**
1. **logseq-fresh-start.md** — Wipe old config, connect to workspace, test cycle
2. **profile-templates.md** — All 7 files with templates and guidance

**User Tasks:**
- [ ] Wipe old Logseq config (%APPDATA%\Logseq, %LOCALAPPDATA%\Logseq)
- [ ] Launch Logseq, add graph → \\silverblue-ai\zeroclaw\workspace
- [ ] Configure: Markdown format, disable journals
- [ ] Test: create file → verify appears on Silverblue → wait 15 min → confirm git commit
- [ ] Populate shared/dietary-profile.md (Malcolm & Jen preferences)
- [ ] Populate shared/location.md (South Shields, seasonal produce)
- [ ] Verify health-profile.md gitignored, then populate (local only)
- [ ] Populate shared/music-profile.md (for Penny & Ziggy)
- [ ] Populate shared/travel-profile.md (for Joy)
- [ ] Populate shared/user-profile.md (household info)
- [ ] Populate projects/meal-planner/pantry.md (current kitchen inventory)

### Phase 9: Frank Full Implementation

**Prerequisites:** Phase 8 complete (profiles populated)

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
- [ ] Decide: on-demand only, or part of Sunday routine?

#### Automation
- [ ] Investigate ZeroClaw cron payload format
- [ ] Set up Sunday 3:30pm cron job
- [ ] Test scheduled execution end-to-end

---

## Phase 15: Google Calendar Integration (Future)

**Status:** Fully designed, ready to implement after Phases 8-14

**Implementation time:** ~3 hours

**What It Enables:**

**Joy (Travel Planner):**
- Queries past holidays from calendar
- Learns destination preferences, timing patterns, trip duration
- Avoids suggesting recently visited places
- Checks calendar for commitments affecting trip dates

**Ziggy (Gig Finder):**
- Queries past gig attendance from calendar
- Learns favourite artists, venues, gig frequency
- References past attendance: "You saw [Artist] in 2019 — they're back!"
- Checks calendar for availability on recommended gig dates

**Frank (Meal Planner):**
- Checks calendar for restaurant bookings
- Skips meal planning for nights with dinner plans
- Notes dinner parties needing extra shopping
- Suggests quick meals before late events

**Method:** MCP (Model Context Protocol) server
- Native ZeroClaw support
- Secure OAuth tokens in ~/.zeroclaw/secrets/ (gitignored)
- Read-only access (calendar.readonly scope)
- Extensible to Gmail, Drive, Contacts, Spotify later

**Available Guide:** phase-15-calendar-implementation.md

---

## Not Yet Started
- Phase 10: AnythingLLM connection
- Phases 11-14: Len, Ziggy, Penny, Joy full activation (without calendar)
- Phase 15: Google Calendar Integration

---

## Current Blockers

None. Phase 8 ready for user implementation.

---

## Recent Changes

### 2026-02-25
- **Session 7 complete** — Logseq setup fully documented, Phase 15 calendar designed
- Created logseq-fresh-start.md with step-by-step reset instructions
- Created profile-templates.md with all 7 file templates
- Designed Phase 15 Google Calendar integration via MCP (~3 hours)
- Documented Joy/Ziggy/Frank calendar capabilities
- Identified future MCP extensions (Gmail, Drive, Contacts, Spotify)
- Updated all project files

### 2026-02-24
- **Phases 5, 6, 7 complete** — persona switching, Bob operational, all personas updated
- Promoted Logseq to Phase 8 (before Frank) — needed for editing shared profiles
- Added Frank recipe research feature to Phase 9 plan
- Switched pantry from SQLite (food.db) to markdown (pantry.md)
- Deleted food.db, schema.sql, seed_data.sql
- Frank's MANDATORY FIRST STEP updated to reference pantry.md
- All decisions recorded in root DECISIONS.md

---

## Next Session Tasks

**For User:**
1. Follow logseq-fresh-start.md guide
2. Wipe old Logseq config folders
3. Connect to workspace via Samba
4. Test edit → git commit cycle
5. Populate all 7 profiles using templates
6. Verify profiles (except health-profile.md) committed to git

**For Claude (next session):**
1. Verify Logseq setup successful
2. Confirm all profiles populated
3. Begin Frank implementation (Phase 9)

## Key Learnings

- file_read paths are relative to workspace root — never absolute
- SOUL.md loads from workspace root
- [[tools]] not needed in SKILL.toml for ZeroClaw built-ins
- Explicit file_read syntax + MANDATORY heading required for reliable on-activation reads
- Bob can self-correct his own persona file
- Logseq via Samba is the right way to edit workspace markdown — not terminal
- MCP servers are the proper way to integrate external data sources (calendar, Gmail, etc.)
- health-profile.md must be gitignored (never committed to GitHub)
