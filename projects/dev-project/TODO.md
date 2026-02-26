# Silverblue AI Workspace — Task List

**Priority order — work top to bottom.**  
Check off items as completed. Update STATE.md after each session.

---

## Phases 5, 6, 7 ✅ COMPLETE

- [x] Persona switching (SOUL.md + skills)
- [x] Bob operational and self-managing
- [x] All six personas with MANDATORY FIRST STEP protocol
- [x] food.db → pantry.md switch
- [x] Decisions recorded

---

## LiteLLM — Outstanding Items

- [ ] Decide on Gemini rate limit resolution: switch to `gemini-1.5-flash` OR enable billing on Google AI Studio
- [ ] Write Last.fm / Setlist.fm Python ingestion script for `shared/music-profile.md`
- [ ] Test Bob running the ingestion script on demand

---

## Phase 8: Profile Population ⬅️ YOU ARE HERE

**Editor:** VS Code (replaces Logseq — open source, open `\\silverblue-ai\zeroclaw\workspace` as a folder)
**Note:** Knowledge base is AnythingLLM's job — no Logseq needed

### Setup VS Code
- [ ] Install VS Code on Windows (code.visualstudio.com)
- [ ] File → Open Folder → `\\silverblue-ai\zeroclaw\workspace`
- [ ] Install "Markdown All in One" extension (optional but handy for table editing)

### Populate Profiles (Main Task)
- [ ] shared/dietary-profile.md — Malcolm + Jen food preferences, dislikes
- [ ] shared/location.md — South Shields, seasonal produce
- [ ] Verify health-profile.md gitignored first
- [ ] shared/health-profile.md — health conditions (LOCAL ONLY)
- [ ] shared/music-profile.md — musical taste, gig preferences
- [ ] shared/travel-profile.md — travel style, budget, past trips
- [ ] shared/user-profile.md — general household info
- [ ] projects/meal-planner/pantry.md — current kitchen inventory

### Verification
- [ ] All profiles have real data (not placeholder [Fill in] text)
- [ ] Git commits show profile files (health-profile.md NOT committed)
- [ ] health-profile.md exists locally but not in git log

---

## Phase 9: Frank (Meal Planner) Full Implementation

**Prerequisites:** Phase 8 complete (all profiles populated)

### Core
- [ ] Test Frank reading pantry.md
- [ ] Test Frank reading dietary-profile.md
- [ ] Test full meal plan generation end-to-end
- [ ] Verify meal_plan.md saved to projects/meal-planner/
- [ ] Verify shopping_list.md saved to projects/meal-planner/

### Recipe Research (new feature)
- [ ] Add recipe research workflow to FRANK.md
- [ ] Frank fetches from diabetes.org.uk/living-with-diabetes/eating/recipes
- [ ] Frank fetches from bbc.co.uk/food
- [ ] Cross-reference with dietary-profile.md preferences
- [ ] Filter disliked ingredients (Malcolm: raw tomatoes / Jen: uncooked cheese)
- [ ] Save shortlist to projects/meal-planner/new-recipes.md
- [ ] Decide: on-demand only, or part of Sunday routine?

### Automation
- [ ] Investigate ZeroClaw cron payload format
- [ ] Set up Sunday 3:30pm cron job
- [ ] Test scheduled execution end-to-end

---

## Phase 10: AnythingLLM Integration

- [ ] Confirm AnythingLLM installed on Windows 11
- [ ] Connect workspace via Samba
- [ ] Configure to index content-library/
- [ ] Test indexing and query functionality

---

## Phase 11: Len (Content Curator)

- [ ] Implement Telegram content forwarding workflow
- [ ] Test URL fetching, categorisation, file saving
- [ ] Verify AnythingLLM indexes new files

---

## Phase 12: Ziggy (Gig Finder)

- [ ] Complete shared/music-profile.md (done in Phase 8)
- [ ] Test gig search and recommendation workflow
- [ ] Create projects/live-music/watchlist.md

---

## Phase 13: Penny (Song Tutor)

- [ ] Initialise projects/song-tutor/progress-log.md
- [ ] Test session continuity and song draft versioning

---

## Phase 14: Joy (Travel Planner)

- [ ] Complete shared/travel-profile.md (done in Phase 8)
- [ ] Test destination research, itinerary, and budget workflows

---

## Phase 15: Google Calendar Integration

**Status:** Fully designed, ready to implement (~3 hours)

**Prerequisites:** Phases 8-14 complete

**Guide:** phase-15-calendar-implementation.md

### Research & Setup
- [ ] **DECISION: Choose Node.js install method** (rpm-ostree recommended — needs reboot)
- [ ] Install Node.js using chosen method
- [ ] Verify: `node --version` (need v18+) and `npx --version`
- [ ] Note full path to npx: `which npx` (needed for config.toml)
- [ ] Check ZeroClaw MCP config syntax: `zeroclaw config schema | grep -A 20 mcp`
- [ ] Confirm MCP server: `@cocal/google-calendar-mcp` (nspady/google-calendar-mcp)

### Google Cloud Setup (20 mins)
- [ ] Create Google Cloud project "ZeroClaw Calendar Access"
- [ ] Enable Google Calendar API
- [ ] Configure OAuth consent screen
- [ ] Create OAuth credentials (Desktop app)
- [ ] Download credentials.json

### MCP Server Installation (30 mins)
- [ ] Create ~/.zeroclaw/mcp-servers/ directory
- [ ] Create ~/.zeroclaw/secrets/ directory (chmod 700)
- [ ] Install chosen MCP server
- [ ] Store credentials securely
- [ ] Run initial OAuth flow
- [ ] Test MCP server standalone

### ZeroClaw Integration (20 mins)
- [ ] Add secrets/ to .gitignore
- [ ] Add MCP configuration to config.toml
- [ ] Validate configuration (zeroclaw doctor)
- [ ] Restart ZeroClaw
- [ ] Check logs for MCP server connection

### Test Calendar Access (15 mins)
- [ ] Test via Bob: list recent events
- [ ] Test via Bob: search for "holiday"
- [ ] Test error handling

### Update Personas (30 mins)
- [ ] Add calendar integration to JOY.md
- [ ] Add calendar integration to ZIGGY.md
- [ ] Add calendar integration to FRANK.md

### Test Persona Integration (30 mins)
- [ ] Test Joy with calendar (trip recommendations)
- [ ] Test Ziggy with calendar (gig recommendations)
- [ ] Test Frank with calendar (meal planning)

### Documentation (15 mins)
- [ ] Update DECISIONS.md
- [ ] Update STATE.md
- [ ] Update TODO.md
- [ ] Mark Phase 15 complete

---

## Future / Nice-to-Have

- [ ] Gmail MCP integration (for Len)
- [ ] Google Drive MCP (store meal plans, itineraries)
- [ ] Contacts MCP (personalize recommendations)
- [ ] Spotify MCP (enhance Ziggy)
- [ ] Weekly digest generation (Len)
- [ ] Scheduled gig roundup (Ziggy)
- [ ] Travel deal alerts (Joy)
- [ ] Joy + Ziggy trip coordination (concerts + travel)
- [ ] workspace-backup/ cleanup
