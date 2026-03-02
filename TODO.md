# Silverblue AI Workspace — Task List

**Priority order — work top to bottom.**  
Check off items as completed. Update STATE.md after each session.

---

## Immediate — Bob Robustness ⬅️ YOU ARE HERE

- [ ] Investigate `systemctl` policy block in ZeroClaw config.toml
- [ ] Test Bob's standard diagnostic routine end-to-end
- [ ] Test Bob's session start routine in a fresh session
- [ ] Verify Bob can read RUNBOOK.md
- [ ] Update SOUL.md — reflect Bob as default, others archived
- [ ] Add OPENROUTER_API_KEY_2 to LiteLLM config and ~/.silverblue-ai-config
- [ ] Write Last.fm/Setlist.fm Python ingestion script for shared/music-profile.md
- [ ] Test Bob running ingestion script on demand

---

## LiteLLM ✅ COMPLETE

- [x] Three Gemini API keys as round-robin pool
- [x] Two Groq API keys as fallback pool
- [x] Fix quoted API keys in ~/.silverblue-ai-config
- [x] Named model groups with explicit fallbacks
- [x] Simplified to three-tier fallback: openrouter free → groq → gemini
- [x] Discovered and resolved ZeroClaw tool calling incompatibility with Groq/Gemini
- [x] OpenRouter gpt-oss-20b/120b:free confirmed working with ZeroClaw tool calling
- [x] OpenRouter privacy settings enabled for free models
- [x] LiteLLM upgraded to v1.81.12; auto-update timer enabled

---

## Persona System ✅ BOB OPERATIONAL

- [x] SOUL.md persona switching framework
- [x] All six persona files created
- [x] Bob confirmed operational with tool calling
- [x] Other personas archived to personas/archive/
- [x] Bob promoted to system orchestrator
- [x] BOB.md optimised — trimmed, diagnostic routine, secret hygiene
- [x] RUNBOOK.md created
- [x] QUICK-REFERENCE.md created and updated

---

## GitHub ✅ CLEAN

- [x] Secrets purged from git history using git-filter-repo
- [x] Groq and Anthropic API keys rotated
- [x] Force push succeeded — no secrets violation
- [x] projects/dev-project/docs/config.yaml added to .gitignore

---

## Phase 8: Profile Population — DEFERRED

Reason: Other personas shelved. Resume when personas are reactivated.

- [ ] shared/dietary-profile.md
- [ ] shared/location.md
- [ ] shared/health-profile.md (local only — verify gitignored first)
- [ ] shared/music-profile.md (via Last.fm/Setlist.fm script)
- [ ] shared/travel-profile.md
- [ ] shared/user-profile.md
- [ ] projects/meal-planner/pantry.md

---

## Phase 9: Frank (Meal Planner) — DEFERRED

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

## Phases 11-14: Other Personas — DEFERRED

- [ ] Restore and test Len (Content Curator)
- [ ] Restore and test Ziggy (Gig Finder)
- [ ] Restore and test Penny (Song Tutor)
- [ ] Restore and test Joy (Travel Planner)

---

## Phase 15: Google Calendar Integration — DEFERRED

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
- [ ] Add Anthropic Haiku to explicit fallback if free tier unreliable
