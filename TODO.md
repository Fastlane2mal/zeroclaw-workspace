# Silverblue AI Workspace — Task List

**Priority order — work top to bottom.**  
Check off items as completed. Update STATE.md after each session.

---

## LiteLLM ✅ COMPLETE (Sessions 9, 10 & 11)

- [x] Three Gemini API keys as round-robin pool
- [x] Two Groq API keys as fallback pool
- [x] Fix quoted API keys in ~/.silverblue-ai-config
- [x] Fix duplicate general_settings in config.yaml
- [x] Named model groups with explicit fallbacks
- [x] Simplified to three-tier fallback: openrouter/auto → groq → gemini
- [x] Discovered and resolved ZeroClaw tool calling incompatibility with Groq/Gemini
- [x] OpenRouter auto router confirmed working with ZeroClaw tool calling
- [x] LiteLLM upgraded to v1.81.12; auto-update timer enabled
- [ ] Monitor OpenRouter free tier reliability — upgrade to Claude Haiku if needed

---

## Persona System ✅ BOB OPERATIONAL

- [x] SOUL.md persona switching framework
- [x] All six persona files created
- [x] Bob confirmed operational with tool calling
- [x] Other personas archived to personas/archive/
- [x] Bob's file path issue resolved (personas/BOB.md)

---

## Bob — Immediate Tasks ⬅️ YOU ARE HERE

- [ ] Read updated STATE.md and TODO.md
- [ ] Update projects/dev-project/STATE.md with current platform status
- [ ] Write Last.fm/Setlist.fm Python ingestion script for shared/music-profile.md
- [ ] Test ingestion script on demand

---

## Phase 8: Profile Population — DEFERRED

**Reason:** Other personas shelved. Resume when personas are reactivated.

- [ ] shared/dietary-profile.md
- [ ] shared/location.md
- [ ] shared/health-profile.md (local only — verify gitignored first)
- [ ] shared/music-profile.md (via Last.fm/Setlist.fm script)
- [ ] shared/travel-profile.md
- [ ] shared/user-profile.md
- [ ] projects/meal-planner/pantry.md

---

## Phase 9: Frank (Meal Planner) — DEFERRED

**Prerequisites:** Phase 8 complete, Frank restored from archive

- [ ] Restore FRANK.md from personas/archive/
- [ ] Test Frank reading pantry.md and dietary-profile.md
- [ ] Test full meal plan generation end-to-end
- [ ] Add recipe research workflow
- [ ] Set up Sunday 3:30pm cron job

---

## Phase 10: AnythingLLM Integration — DEFERRED

- [ ] Connect workspace via Samba
- [ ] Configure to index content-library/
- [ ] Test indexing and query functionality

---

## Phase 11: Len (Content Curator) — DEFERRED

- [ ] Restore LEN.md from personas/archive/
- [ ] Implement Telegram content forwarding workflow

---

## Phase 12: Ziggy (Gig Finder) — DEFERRED

- [ ] Restore ZIGGY.md from personas/archive/
- [ ] Complete shared/music-profile.md
- [ ] Test gig search and recommendation workflow

---

## Phase 13: Penny (Song Tutor) — DEFERRED

- [ ] Restore PENNY.md from personas/archive/
- [ ] Initialise projects/song-tutor/progress-log.md

---

## Phase 14: Joy (Travel Planner) — DEFERRED

- [ ] Restore JOY.md from personas/archive/
- [ ] Complete shared/travel-profile.md

---

## Phase 15: Google Calendar Integration — DEFERRED

**Prerequisites:** Phases 8-14 complete

- [ ] Decide Node.js install method (rpm-ostree recommended)
- [ ] Install Node.js, verify npx path
- [ ] Google Cloud project setup and OAuth credentials
- [ ] Install and configure @cocal/google-calendar-mcp
- [ ] Update Joy, Ziggy, Frank persona files
- [ ] Test calendar access via Bob

---

## Future / Nice-to-Have

- [ ] Gmail MCP integration (for Len)
- [ ] Google Drive MCP
- [ ] Spotify MCP (enhance Ziggy)
- [ ] Joy + Ziggy trip coordination
- [ ] workspace-backup/ cleanup
- [ ] Weekly digest generation (Len)
