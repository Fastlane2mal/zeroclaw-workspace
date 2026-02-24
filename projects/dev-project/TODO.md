# Silverblue AI Workspace — Task List

**Priority order — work top to bottom.**  
Check off items as completed. Update STATE.md after each session.

---

## Phase 5: Persona Switching ⬅️ YOU ARE HERE

### Research
- [ ] Read ZeroClaw Skills system documentation
- [ ] Find example SKILL.toml files in ZeroClaw repo
- [ ] Read AIEOS identity framework specification
- [ ] Examine identity.format = "openclaw" behaviour in detail
- [ ] Research whether Skills and SOUL.md can be combined

### Decision
- [ ] Compare approaches: Skills vs SOUL.md vs hybrid
- [ ] Record decision in root DECISIONS.md
- [ ] Document rationale in research/phase5-persona-switching.md

### Implementation
- [ ] Write test SKILL.toml for Frank
- [ ] Test manual persona activation via Telegram
- [ ] Verify persona reads correct context files (dietary-profile.md, food.db)
- [ ] Test persona switching mid-session if applicable
- [ ] Document final approach

### Proof of Concept
- [ ] Activate Frank via Telegram
- [ ] Verify he reads shared/dietary-profile.md
- [ ] Verify he reads projects/meal-planner/food.db
- [ ] Test meal plan generation
- [ ] Confirm output saved to correct location

---

## Phase 6: Frank (Meal Planner)

### Setup
- [ ] Verify food.db in projects/meal-planner/
- [ ] Test SQLite database access from ZeroClaw
- [ ] Create pantry reading function/skill
- [ ] Test dietary profile reading

### Core Function
- [ ] Implement meal plan generation
- [ ] Test shopping list format
- [ ] Verify 7-day plan structure (breakfast, lunch, dinner)
- [ ] Add cooking tips feature

### Automation
- [ ] Create Sunday 3:30pm cron job in ZeroClaw
- [ ] Test scheduled execution
- [ ] Verify Telegram notification on completion
- [ ] Test on-demand trigger

---

## Phase 7: Logseq Setup

- [ ] Fresh Logseq installation on Windows 11 desktop
- [ ] Point graph to workspace/logseq/ via Samba (\\silverblue-ai\zeroclaw)
- [ ] Configure graph settings
- [ ] Test file sync (Logseq writes → git auto-commits)
- [ ] Create initial folder/page structure

---

## Phase 8: AnythingLLM Integration

- [ ] Confirm AnythingLLM installed on Windows 11
- [ ] Connect workspace directory via Samba
- [ ] Configure to index projects/content-library/
- [ ] Test indexing with sample content
- [ ] Test query functionality

---

## Phase 9: Len (Content Curator)

- [ ] Implement Telegram content forwarding workflow
- [ ] Test URL fetching via http_request
- [ ] Verify categorisation logic
- [ ] Test file saving to content-library/[category]/[date]-[title].md
- [ ] Verify AnythingLLM picks up new files
- [ ] Test query: "What have I saved about X?"

---

## Phase 10: Ziggy (Gig Finder)

- [ ] Complete shared/music-profile.md with real data
- [ ] Test web_search for gig listings (DuckDuckGo)
- [ ] Create projects/live-music/watchlist.md
- [ ] Test recommendation logic
- [ ] Verify distance/travel considerations from South Shields
- [ ] Set up optional weekly roundup

---

## Phase 11: Penny (Song Tutor)

- [ ] Review existing projects/song-tutor/role.md
- [ ] Initialise progress-log.md
- [ ] Test session continuity (Penny reads progress log at start)
- [ ] Create first lesson structure
- [ ] Test song draft versioning
- [ ] Verify exercise generation

---

## Phase 12: Joy (Travel Planner)

- [ ] Complete shared/travel-profile.md with real data
- [ ] Test destination research workflow
- [ ] Create sample itinerary output
- [ ] Test budget calculation
- [ ] Verify packing list generation
- [ ] Explore Joy + Ziggy coordination (trips around concerts)

---

## Phase 13: Bob (Other Dev Projects)

- [ ] Bob handles other coding projects as needed
- [ ] Create dev-project/docs/ structure
- [ ] Define process for new coding projects

---

## Future / Nice-to-Have

- [ ] Weekly digest generation (Len)
- [ ] Scheduled gig roundup (Ziggy)
- [ ] Travel deal alerts (Joy)
- [ ] Joy + Ziggy trip coordination feature
- [ ] Branch workflow for significant changes
- [ ] Ziggy API integrations (Songkick, etc.) — evaluate after DuckDuckGo quality check
- [ ] GitHub Actions integration
- [ ] Multiple ZeroClaw instance evaluation
- [ ] workspace-backup/ cleanup (delete once confident nothing missed)
