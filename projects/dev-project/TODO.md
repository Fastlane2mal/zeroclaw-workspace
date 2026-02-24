# Silverblue AI Workspace — Task List

**Priority order — work top to bottom.**  
Check off items as completed. Update STATE.md after each session.

---

## Phase 5: Persona Switching ✅ COMPLETE

- [x] Research ZeroClaw Skills and openclaw identity system
- [x] Created workspace/SOUL.md (neutral coordinator)
- [x] Created workspace/skills/personas/SKILL.toml and SKILL.md
- [x] Frank activates and responds in character ✅
- [x] Ziggy activates and uses web_search ✅
- [x] Neutral mode ("Back to normal") works ✅
- [x] Decisions recorded

---

## Phase 6 (reordered): Bob Operational ⬅️ YOU ARE HERE

### Setup
- [x] Add operational instructions to BOB.md
- [ ] Create dev-project/docs/ subdirectory on Silverblue
- [ ] Create dev-project/scripts/ subdirectory on Silverblue

### Testing
- [ ] Test Bob via Telegram: "Hey Bob" → verify he reads STATE.md and TODO.md
- [ ] Ask Bob to summarise current project status (confirm he reads files correctly)
- [ ] Ask Bob to append a test entry to SESSIONS.md (confirm he can write files)
- [ ] Confirm file is committed by git auto-commit timer

### Workflow established
- [ ] Dual-mode workflow confirmed working: Bob (Telegram) + Claude (claude.ai)
- [ ] Hand off day-to-day STATE.md / SESSIONS.md updates to Bob

---

## Phase 7: Remaining Persona Operational Instructions

- [ ] Add operational instructions block to PENNY.md
- [ ] Add operational instructions block to LEN.md
- [ ] Add operational instructions block to ZIGGY.md
- [ ] Add operational instructions block to JOY.md

---

## Phase 8: Frank (Meal Planner) Full Implementation

### Shared profiles
- [ ] Complete shared/dietary-profile.md with real Malcolm + Jen data
- [ ] Complete shared/location.md (South Shields, NE England)

### Frank core
- [ ] Verify food.db in projects/meal-planner/ and test Frank can read it
- [ ] Determine if ZeroClaw reads SQLite directly or needs markdown export
- [ ] Test full meal plan generation — ask Frank to plan the week
- [ ] Verify meal_plan.md and shopping_list.md saved correctly

### Automation
- [ ] Investigate ZeroClaw cron payload format
- [ ] Create Sunday 3:30pm cron job
- [ ] Test scheduled execution end-to-end

---

## Phase 9: Logseq Setup

- [ ] Fresh Logseq installation on Windows 11
- [ ] Point graph to workspace/logseq/ via Samba
- [ ] Configure graph settings and test file sync

---

## Phase 10: AnythingLLM Integration

- [ ] Confirm AnythingLLM installed on Windows 11
- [ ] Connect workspace via Samba, configure to index content-library/
- [ ] Test indexing and query functionality

---

## Phase 11: Len (Content Curator)

- [ ] Operational instructions added (Phase 7)
- [ ] Implement Telegram content forwarding workflow
- [ ] Test URL fetching, categorisation, file saving
- [ ] Verify AnythingLLM indexes new files

---

## Phase 12: Ziggy (Gig Finder)

- [ ] Operational instructions added (Phase 7)
- [ ] Complete shared/music-profile.md with real data
- [ ] Test gig search and recommendation workflow
- [ ] Create watchlist.md, set up optional weekly roundup

---

## Phase 13: Penny (Song Tutor)

- [ ] Operational instructions added (Phase 7)
- [ ] Initialise progress-log.md
- [ ] Test session continuity and song draft versioning

---

## Phase 14: Joy (Travel Planner)

- [ ] Operational instructions added (Phase 7)
- [ ] Complete shared/travel-profile.md with real data
- [ ] Test destination research, itinerary, and budget workflows
- [ ] Explore Joy + Ziggy coordination

---

## Future / Nice-to-Have

- [ ] Weekly digest generation (Len)
- [ ] Scheduled gig roundup (Ziggy)
- [ ] Travel deal alerts (Joy)
- [ ] Joy + Ziggy trip coordination
- [ ] Ziggy API integrations (Songkick etc.)
- [ ] workspace-backup/ cleanup
