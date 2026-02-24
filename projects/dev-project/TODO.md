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
- [x] Neutral mode works ✅
- [x] Decisions recorded

---

## Phase 6: Bob Operational ✅ COMPLETE

- [x] Add operational instructions to BOB.md
- [x] Fix file_read paths — relative to workspace root, not absolute
- [x] Create dev-project/docs/ and dev-project/scripts/ directories
- [x] Test Bob reads STATE.md and TODO.md on activation ✅
- [x] Test Bob writes to SESSIONS.md ✅
- [x] Bob self-corrects BOB.md path instructions ✅
- [x] Dual-mode workflow confirmed live ✅

---

## Phase 7: Remaining Persona Operational Instructions ⬅️ BOB HANDLING VIA TELEGRAM

- [ ] Add operational instructions to PENNY.md
- [ ] Add operational instructions to LEN.md
- [ ] Add operational instructions to ZIGGY.md
- [ ] Add operational instructions to JOY.md

---

## Phase 8: Frank (Meal Planner) Full Implementation ⬅️ NEXT CLAUDE SESSION

### Shared profiles
- [ ] Complete shared/dietary-profile.md with real Malcolm + Jen data
- [ ] Complete shared/location.md

### Frank core
- [ ] Determine if ZeroClaw reads SQLite directly or needs markdown export
- [ ] If markdown needed: create pantry.md and update Frank's instructions
- [ ] Test full meal plan generation
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

- [ ] Connect workspace via Samba
- [ ] Configure to index content-library/
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
- [ ] Create watchlist.md

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

---

## Future / Nice-to-Have

- [ ] Weekly digest generation (Len)
- [ ] Scheduled gig roundup (Ziggy)
- [ ] Travel deal alerts (Joy)
- [ ] Joy + Ziggy trip coordination
- [ ] Ziggy API integrations (Songkick etc.)
- [ ] workspace-backup/ cleanup
