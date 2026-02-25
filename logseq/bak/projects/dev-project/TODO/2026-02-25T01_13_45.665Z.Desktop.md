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

## Phase 8: Logseq Setup ⬅️ YOU ARE HERE

**Status:** Documentation complete, ready for user implementation

**Guides available:**
- logseq-fresh-start.md
- profile-templates.md

### Wipe Old Logseq Config
- [ ] Close Logseq completely (check system tray)
- [ ] Delete %APPDATA%\Logseq folder
- [ ] Delete %LOCALAPPDATA%\Logseq folder
- [ ] Restart computer

### Fresh Logseq Setup
- [ ] Launch Logseq
- [ ] Add graph → \\silverblue-ai\zeroclaw\workspace
- [ ] Configure: Markdown format
- [ ] Configure: Disable journals

### Test Edit Cycle
- [ ] Create test file in Logseq
- [ ] Verify file appears on Silverblue
- [ ] Wait 15 minutes for auto-commit
- [ ] Check git log for commit
- [ ] Delete test file
- [ ] Verify deletion commits

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
- [ ] Git commits show 6 new files (health-profile.md NOT committed)
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

### Research & Setup (30 mins)
- [ ] Research available Google Calendar MCP servers
- [ ] Choose: Official / Community / Custom build
- [ ] Document choice in DECISIONS.md

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
