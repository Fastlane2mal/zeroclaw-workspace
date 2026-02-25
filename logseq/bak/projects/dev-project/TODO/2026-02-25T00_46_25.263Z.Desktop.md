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

### Installation
- [ ] Install Logseq on Windows 11 (if not already)
- [ ] Add Graph → point to \\silverblue-ai\zeroclaw\workspace
- [ ] Verify Logseq reads existing files (personas/, projects/, shared/)
- [ ] Configure graph settings (prefer markdown mode)

### Verify edit cycle
- [ ] Edit a test file in Logseq
- [ ] Confirm git auto-commit picks it up within 15 minutes
- [ ] Confirm file readable on Silverblue after edit

### Fill in shared profiles (the main reason Logseq is first)
- [ ] shared/dietary-profile.md — Malcolm + Jen preferences, dislikes, any health-related diet needs
- [ ] shared/location.md — South Shields, NE England, seasonal produce notes
- [ ] shared/health-profile.md — local only, never committed (gitignored)
- [ ] shared/music-profile.md — genres, artists, gig preferences
- [ ] shared/travel-profile.md — travel style, budget, past trips, preferences
- [ ] shared/user-profile.md — general Malcolm + Jen household profile

### Also fill in via Logseq
- [ ] projects/meal-planner/pantry.md — what's actually in the kitchen

---

## Phase 9: Frank (Meal Planner) Full Implementation

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

## Future / Nice-to-Have

- [ ] Weekly digest generation (Len)
- [ ] Scheduled gig roundup (Ziggy)
- [ ] Travel deal alerts (Joy)
- [ ] Joy + Ziggy trip coordination
- [ ] Ziggy API integrations (Songkick etc.)
- [ ] workspace-backup/ cleanup
