# Development Sessions — Silverblue AI Workspace

Log of Claude sessions working on the platform. Most recent session first.

---

## Session 9 — 2026-02-26

**Focus:** LiteLLM multi-key configuration and debugging

### Completed
- Added three Gemini API keys (GOOGLE_API_KEY_1/2/3) as round-robin pool
- Added two Groq API keys (GROQ_API_KEY_1/2) as fallback pool
- Diagnosed root cause of all key failures: quoted values in ~/.silverblue-ai-config causing %22 URL encoding
- Confirmed os.environ/ is correct LiteLLM format — quotes were the root cause, not the format
- Fixed duplicate general_settings sections in config.yaml (port and master_key were in separate blocks)
- Fixed YAML syntax error in fallbacks (missing - prefix before gemini-flash)
- Fixed master_key not loading — added to general_settings in config.yaml
- Replaced separate default model entry with model_group_alias mapping default → gemini-flash pool
- Added explicit fallback entries for both gemini-flash and default model groups
- Moved rate limiting to per-deployment rpm/tpm in litellm_params (rate_limits is not valid top-level key)
- Increased Ollama timeout to 120s (default 30s too short under load)
- Confirmed all three gemini-flash entries loading correctly ✅
- Confirmed 200 OK responses working via Groq/Ollama while Gemini quota exhausted ✅
- Gemini 2.5 Flash adopted (upgraded from 2.0 Flash)

### Key Decisions
- API key values must have no quotes in ~/.silverblue-ai-config
- os.environ/ format is correct for config.yaml — confirmed by official docs
- model_group_alias maps default → gemini-flash but fallbacks still need explicit default entry
- rate_limits is not a valid top-level config key; use rpm/tpm per deployment instead
- Ollama struggles under load with long contexts — last resort only
- Both gemini-flash and default need explicit fallback chain entries

### Issues Encountered
- Quoted API keys → %22 URL encoding → all providers failing with invalid key
- Duplicate general_settings → master_key not loaded → 400 auth errors
- YAML syntax error in fallbacks → intermittent failures
- model_group_alias alone insufficient — explicit fallback entry needed per model group
- Gemini and Groq quotas exhausted during debugging session — reset next day

### Next Session
1. Verify all three Gemini keys working after quota reset
2. Continue Phase 8 — populate remaining profile files via VS Code
3. Decide Node.js install method for Phase 15 Calendar MCP
4. Write Last.fm / Setlist.fm Python ingestion script for music-profile.md

---

## Session 8 — 2026-02-25

**Focus:** Phase 15 — Google Calendar MCP research, Node.js planning, and Logseq → VS Code switch

### Completed
- Researched available Google Calendar MCP servers; selected `nspady/google-calendar-mcp` (@cocal/google-calendar-mcp)
- Confirmed ZeroClaw v0.1.6 supports MCP servers natively
- Confirmed Node.js not installed on Silverblue (`node: command not found`)
- Evaluated three Node.js installation options for Silverblue + systemd service use case:
  - rpm-ostree: reboot required, cleanest for systemd (recommended)
  - nvm: no reboot, but Silverblue npm prefix conflict needs workaround
  - toolbox: clean install, but needs wrapper script for systemd service
- Debugged and fixed LiteLLM config — identified 401 auth error (LITELLM_MASTER_KEY not in ZeroClaw config), missing GEMINI_API_KEY in container env, and model name mismatch
- Confirmed fallback chain working — Gemini hit free tier rate limit (429), Groq handled requests automatically
- Identified Last.fm and Setlist.fm as rich data sources for music-profile.md — Python ingestion script planned
- Replaced Logseq with VS Code as workspace markdown editor
- Confirmed AnythingLLM covers knowledge base — Logseq's knowledge base features were never needed

### Key Decisions
- MCP server: `@cocal/google-calendar-mcp` (nspady, 964 stars, most maintained)
- Joy and Ziggy prioritised for calendar access first (Frank to follow)
- Node.js installation method: pending (rpm-ostree recommended)
- Full path to `npx` must be used in config.toml (ZeroClaw systemd service PATH issue)
- ZeroClaw MCP config syntax to verify with `zeroclaw config schema | grep -A 20 mcp`
- VS Code replaces Logseq — open `\\silverblue-ai\zeroclaw\workspace` as a folder
- Knowledge base = AnythingLLM; editor = VS Code; no overlap needed
- LiteLLM fallback chain: Gemini 2.0 Flash → Groq → Claude Haiku → Ollama
- LITELLM_MASTER_KEY must be set in ZeroClaw config.toml `api_key` field
- Gemini free tier rate limit hit — resolution (1.5 Flash or billing) deferred
- Music profile to be populated via Last.fm + Setlist.fm Python ingestion script

### Next Session
1. Install VS Code on Windows, open workspace via Samba share
2. Populate remaining profile files using VS Code
3. Decide on and install Node.js (rpm-ostree recommended — reboot required)
4. Set up Google Cloud project and download OAuth credentials JSON
5. Create `~/.zeroclaw/secrets/`, store credentials, run OAuth flow
6. Add MCP config to config.toml, verify with `zeroclaw doctor`, restart
7. Test calendar access via Bob in Telegram
8. Update JOY.md and ZIGGY.md with calendar integration instructions

---

## Session 7 — 2026-02-25

**Focus:** Logseq setup planning & Google Calendar integration design

### Completed
- Created comprehensive Logseq fresh start guide (wipe old config, clean setup)
- Created all 7 profile templates:
  - shared/dietary-profile.md
  - shared/location.md
  - shared/health-profile.md (local only, gitignored)
  - shared/music-profile.md
  - shared/travel-profile.md
  - shared/user-profile.md
  - projects/meal-planner/pantry.md
- Designed Phase 15: Google Calendar Integration via MCP
  - Joy learns from past holidays (destinations, timing patterns)
  - Ziggy learns from past gig attendance (artists, venues)
  - Frank checks for restaurant bookings and dinner parties
  - ~3 hour implementation estimate
- Documented complete MCP setup: OAuth, server installation, persona updates
- Identified future extensions: Gmail, Drive, Contacts, Spotify (same MCP pattern)
- Updated all project files (DECISIONS.md, SESSIONS.md, STATE.md, TODO.md)

### Key Decisions
- Logseq via Samba is proper editing interface for shared profiles
- Fresh Logseq start: wipe %APPDATA%\Logseq and %LOCALAPPDATA%\Logseq
- Google Calendar via MCP (Phase 15) for Joy, Ziggy, Frank
- Calendar tokens in ~/.zeroclaw/secrets/ (gitignored)
- Read-only calendar access initially (calendar.readonly scope)
- MCP pattern proven extensible to other Google services

### Outputs Created
1. `logseq-fresh-start.md` — Step-by-step Logseq reset and workspace connection
2. `profile-templates.md` — All 7 profile templates with detailed guidance
3. `google-calendar-integration.md` — Overview of calendar integration options
4. `phase-15-calendar-implementation.md` — Complete MCP implementation plan

### Next Session (User)
- Wipe old Logseq config on Windows
- Connect Logseq to \\silverblue-ai\zeroclaw\workspace
- Test edit → git auto-commit cycle
- Populate all 7 profile files with real data
- Verify profiles committed to git (except health-profile.md)

---

## Session 6 — 2026-02-24

**Focus:** Phase 7 — MANDATORY FIRST STEP protocol, all personas updated

### Completed
- Fixed on-activation read issue: explicit file_read syntax + MANDATORY heading required
- Bob updated all five remaining persona files via Telegram
- All six personas now read domain files before every response ✅

---

## Session 5 — 2026-02-24

**Focus:** Bob confirmed operational, dual-mode workflow live

### Completed
- Diagnosed file_read path issue (relative to workspace root)
- Bob read STATE.md, created directories, wrote SESSIONS.md ✅
- Bob self-corrected BOB.md ✅
- Dual-mode workflow confirmed live

---

## Session 4 — 2026-02-24

**Focus:** Bob operational + priority switch to Bob before Frank

---

## Session 3 — 2026-02-24

**Focus:** Phase 5 — persona switching fully implemented and tested

---

## Session 2 — 2026-02-24

**Focus:** dev-project/ folder structure created

---

## Session 1 — 2026-02-24

**Focus:** All six persona definitions and shared profile templates created

---

## Session 0 — 2026-02-23

**Focus:** Infrastructure — ZeroClaw upgrade, workspace restructure, git automation
