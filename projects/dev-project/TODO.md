# Silverblue AI Workspace — Task List

**Priority order — work top to bottom.**  
Check off items as completed. Update STATE.md after each session.

---

## Phase 5: Persona Switching ✅ COMPLETE
## Phase 6: Bob Operational ✅ COMPLETE
## Phase 7: Remaining Persona Operational Instructions ✅ COMPLETE

- [x] MANDATORY FIRST STEP protocol added to BOB.md ✅
- [x] MANDATORY FIRST STEP protocol added to FRANK.md ✅
- [x] MANDATORY FIRST STEP protocol added to PENNY.md ✅
- [x] MANDATORY FIRST STEP protocol added to LEN.md ✅
- [x] MANDATORY FIRST STEP protocol added to ZIGGY.md ✅
- [x] MANDATORY FIRST STEP protocol added to JOY.md ✅

---

## Phase 8: Frank (Meal Planner) ⬅️ YOU ARE HERE

### Resolve open questions first (Claude session)
- [ ] Investigate: can ZeroClaw file_read handle SQLite (food.db) directly?
- [ ] If not: create pantry.md markdown export, update Frank's instructions
- [ ] Investigate: ZeroClaw cron payload format — how is message body set?

### Shared profiles (fill in real data)
- [ ] Complete shared/dietary-profile.md — Malcolm + Jen preferences and dislikes
- [ ] Complete shared/location.md — South Shields, seasonal produce context

### Frank core
- [ ] Test Frank reading pantry data (food.db or pantry.md)
- [ ] Test full meal plan generation end-to-end
- [ ] Verify meal_plan.md saved to projects/meal-planner/
- [ ] Verify shopping_list.md saved to projects/meal-planner/

### Automation
- [ ] Set up Sunday 3:30pm cron job in ZeroClaw
- [ ] Test scheduled execution
- [ ] Verify Telegram notification on completion

---

## Phase 9: Logseq Setup

- [ ] Fresh Logseq installation on Windows 11
- [ ] Point graph to workspace/logseq/ via Samba
- [ ] Configure graph settings and test file sync

---

## Phase 10: AnythingLLM Integration

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

- [ ] Complete shared/music-profile.md with real data
- [ ] Test gig search and recommendation workflow
- [ ] Create projects/live-music/watchlist.md

---

## Phase 13: Penny (Song Tutor)

- [ ] Initialise projects/song-tutor/progress-log.md
- [ ] Test session continuity and song draft versioning

---

## Phase 14: Joy (Travel Planner)

- [ ] Complete shared/travel-profile.md with real data
- [ ] Test destination research, itinerary, and budget workflows

---

## Future / Nice-to-Have

- [ ] Weekly digest generation (Len)
- [ ] Scheduled gig roundup (Ziggy)
- [ ] Travel deal alerts (Joy)
- [ ] Joy + Ziggy trip coordination
- [ ] Ziggy API integrations (Songkick etc.)
- [ ] workspace-backup/ cleanup
