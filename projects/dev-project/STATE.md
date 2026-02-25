# Silverblue AI Workspace — Development State

**Last updated:** 2026-02-25  
**Current phase:** Phase 8 (profile population) partially complete / Phase 15 (Calendar MCP) in progress  
**Status:** Node.js install decision pending; Google Cloud setup not yet started

---

## What's Working

### Infrastructure ✅
- Fedora Silverblue 40 base system
- Ollama (qwen2.5:3b, qwen2.5:1.5b, nomic-embed-text)
- LiteLLM (Claude Haiku via API gateway, Podman quadlet, port 4000)
- ZeroClaw v0.1.6 (systemd user service running)
- Git workspace with auto-commit (15 min) and auto-push (1 hour)
- Samba share (Windows access for VS Code/AnythingLLM)
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

### Phase 8: Profile Population ⬅️ CURRENT FOCUS

**Status:** Partially complete — some profiles filled, remainder to be done via VS Code

**Editor change:** Logseq replaced with VS Code (open source, intuitive, works directly on Samba share)
**Knowledge base:** AnythingLLM covers this — Logseq's knowledge base features were never needed

**User Tasks:**
- [ ] Install VS Code on Windows (if not already installed)
- [ ] Open `\\silverblue-ai\zeroclaw\workspace` as a folder in VS Code
- [ ] Complete shared/dietary-profile.md (Malcolm & Jen preferences)
- [ ] Complete shared/location.md (South Shields, seasonal produce)
- [ ] Verify health-profile.md gitignored, then populate (local only)
- [ ] Complete shared/music-profile.md (for Penny & Ziggy)
- [ ] Complete shared/travel-profile.md (for Joy)
- [ ] Complete shared/user-profile.md (household info)
- [ ] Complete projects/meal-planner/pantry.md (current kitchen inventory)

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

## Phase 15: Google Calendar Integration ⬅️ ALSO IN PROGRESS

**Status:** Research complete, Node.js install pending, then ready to implement

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

### 2026-02-25 (Session 8)
- **Session 8 complete** — Phase 15 MCP server researched, Node.js options evaluated
- Selected `@cocal/google-calendar-mcp` as MCP server (nspady, 964 stars)
- Confirmed Node.js not installed; evaluated rpm-ostree vs nvm vs toolbox
- rpm-ostree recommended (cleanest for systemd service); decision deferred
- Full implementation plan documented in SESSIONS.md

### 2026-02-25 (Session 7)
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

**For User (next session):**
1. Install VS Code, open workspace via `\\silverblue-ai\zeroclaw\workspace`
2. Complete remaining profile files
3. Decide on Node.js install method for Phase 15

**For Claude (next session):**
1. Verify profiles populated
2. Begin Phase 15 Node.js + Google Cloud setup

## Key Learnings

- file_read paths are relative to workspace root — never absolute
- SOUL.md loads from workspace root
- [[tools]] not needed in SKILL.toml for ZeroClaw built-ins
- Explicit file_read syntax + MANDATORY heading required for reliable on-activation reads
- Bob can self-correct his own persona file
- VS Code is the right editor for the workspace — open Samba share as a folder, no app-specific concepts
- MCP servers are the proper way to integrate external data sources (calendar, Gmail, etc.)
- health-profile.md must be gitignored (never committed to GitHub)
