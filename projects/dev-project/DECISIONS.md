# Silverblue AI Workspace — Decisions Log

This document records key decisions made during the design and implementation 
of the Silverblue AI Workspace. Update this as new decisions are made.

---

## Decisions Made

### Infrastructure

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-02-25 | Node.js installation method deferred — decision pending (Session 8) | Three options evaluated: rpm-ostree (reboot required, cleanest for systemd), nvm (no reboot, Silverblue prefix issue), toolbox (needs wrapper script); rpm-ostree recommended |
| 2026-02-25 | MCP server choice: nspady/google-calendar-mcp (@cocal/google-calendar-mcp npm) | 964 stars, most actively maintained, read-only support via enabled_tools, npx-based (no global install), persistent OAuth tokens |
| 2026-02-25 | Google Calendar via MCP for Joy, Ziggy, Frank (Phase 15) | Real-time calendar access; personas learn from past events; native ZeroClaw MCP support; secure OAuth; extensible to other Google services |
| 2026-02-25 | Calendar tokens stored in ~/.zeroclaw/secrets/ (gitignored) | Keep OAuth tokens local and secure; never committed to GitHub |
| 2026-02-25 | Read-only calendar access (calendar.readonly scope) initially | Safety: personas can't accidentally modify calendar; users retain full control; can add write access later if needed |
| 2026-02-24 | Drop food.db, schema.sql, seed_data.sql — use pantry.md instead | file_read can't read SQLite binary format; markdown is simpler, human-editable, git-diffable, and fits the workspace pattern |
| 2026-02-24 | Persona file_read paths must be relative to workspace root | ZeroClaw resolves file_read via workspace_dir.join(path) — absolute paths don't work |
| 2026-02-24 | Use explicit file_read syntax + MANDATORY heading for on-activation reads | Descriptive instructions alone not sufficient — model skips reads without explicit tool call syntax and strong heading |
| 2026-02-24 | Hybrid persona approach: neutral SOUL.md + single personas skill | Token-efficient; all six personas in one skill avoids conflicts; personas loaded on demand via file_read |
| 2026-02-24 | Trigger pattern: "Hey [Name]" / "@[name]" / "[Name]:" for persona activation | Natural Telegram phrasing; consistent across all personas |
| 2026-02-24 | [[tools]] section not needed in SKILL.toml for ZeroClaw built-in tools | Built-ins (file_read, file_write, web_search) don't require declaration; adding [[tools]] without command field causes skill to be skipped entirely |
| 2026-02-24 | SOUL.md goes at workspace root, not in personas/ | Loaded by load_openclaw_bootstrap_files() from workspace_dir — confirmed from ZeroClaw source |
| 2026-02-23 | Use systemd timers (not cron) for auto-commit and push | Cron not available by default on Fedora Silverblue |
| 2026-02-23 | Auto-commit every 15 minutes, push to GitHub hourly | Balance between granularity and network overhead |
| 2026-02-23 | SSH key authentication for GitHub (not personal access tokens) | More secure, no plaintext credentials |
| 2026-02-23 | All workspace at /var/home/mal/.zeroclaw/workspace | Single source of truth, git-backed |
| 2026-02-23 | Samba share as bridge to Windows desktop tools | No file copying needed — Logseq and AnythingLLM read directly |
| 2026-02-23 | Upgraded ZeroClaw v0.1.1 → v0.1.6 | Security improvements, better Telegram support, new features |
| 2026-02-23 | Build ZeroClaw from git tags (not main branch) | main branch can have unreleased/buggy code; tags are stable releases |

### Personas

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-02-24|Added Joy (travel planner) as sixth persona|Clear use case for research-heavy planning with budget tracking and itinerary generation; natural fit with other lifestyle assistants
| 2026-02-24|Joy's project folder: workspace/projects/travel-planning/ with /trips, /ideas, /research subfolders|Organizes by trip stage: research (exploring options) → ideas (saved for later) → trips (confirmed/completed)
| 2026-02-24|Created shared/travel-profile.md for Joy's reference|Captures travel style, preferences, budget ranges, constraints, and past trip learnings; helps Joy learn from experience
| 2026-02-24|Joy uses web_search and http_request tools for live pricing|Flight and hotel prices change constantly; needs real-time data for accurate budget planning
| 2026-02-23 | Five named personas: Frank, Penny, Bob, Len, Ziggy | Named characters maintain consistent personality better than generic roles |
| 2026-02-23 | Personas stored as .md files in workspace/personas/ | Easy to edit, version controlled, ZeroClaw can read them as context |
| 2026-02-23 | Use SOUL.md / IDENTITY.md format for personas (not system prompt) | ZeroClaw's identity.format = "openclaw" supports this natively — cleaner than embedding in config.toml |
| 2026-02-23 | Investigate Skills system (SKILL.toml) for persona switching | Skills inject prompts/tools at runtime — potentially the right mechanism for switching between Frank, Penny, Bob, Len, Ziggy |
| 2026-02-23 | Frank is the first persona to activate fully | Most work already done; meal planner is clearest use case |

### LiteLLM

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-02-26 | Three Gemini API keys configured as pool (GOOGLE_API_KEY_1/2/3) | Triples free tier to ~4,500 req/day; LiteLLM round-robins across keys automatically |
| 2026-02-26 | Two Groq API keys configured as pool (GROQ_API_KEY_1/2) | Doubles Groq free tier to ~200,000 TPD before Ollama fallback |
| 2026-02-26 | API keys stored without quotes in ~/.silverblue-ai-config | LiteLLM URL-encodes quoted values (%22) causing invalid key errors — bare values required |
| 2026-02-26 | os.environ/ format confirmed correct for LiteLLM config.yaml | Quotes in env file were root cause of key resolution failures, not the format itself |
| 2026-02-26 | Rate limits defined per-deployment via rpm/tpm in litellm_params | rate_limits is not a valid top-level config key; per-deployment limits prevent 429s proactively |
| 2026-02-26 | Ollama timeout set to 120s | Default 30s too short for local model under load; Ollama is last resort only |
| 2026-02-26 | model_group_alias maps default → gemini-flash pool | ZeroClaw requests model=default; alias routes to 3-key Gemini pool for round-robin |
| 2026-02-26 | Fallbacks defined for both gemini-flash and default | model_group_alias alone insufficient; explicit fallback entry needed for each model group name |
| 2026-02-26 | general_settings must have single block with both port and master_key | Duplicate general_settings blocks cause later block to override earlier; master_key was being silently dropped |
| 2026-02-26 | Gemini 2.0 Flash as primary LLM via LiteLLM | Fast, cheap, free tier available; fits personal use case |
| 2026-02-26 | Fallback chain: Groq pool → Ollama | Groq is fast/free; Ollama works offline; Haiku moved to explicit-only (not auto fallback) |
| 2026-02-26 | LITELLM_MASTER_KEY required in ZeroClaw config.toml | LiteLLM proxy enforces auth; ZeroClaw must send key in api_key field |

### Music Profile

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-02-26 | Populate music-profile.md via Last.fm and Setlist.fm APIs rather than manually | 16,476 scrobbles and full gig history available via free APIs — far richer than manual entry |
| 2026-02-26 | Use a Python script run by Bob to ingest Last.fm/Setlist.fm data | No Node.js required; Bob can refresh on demand; writes structured summary to music-profile.md |
| 2026-02-26 | Deezer deferred — lower priority | Likely redundant given Last.fm coverage; requires OAuth for user data |

### Content Curator (Len)

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-02-23 | WhatsApp content forwarded to Telegram for Len to process | No new infrastructure needed; ZeroClaw already monitors Telegram |
| 2026-02-23 | Structured notes saved to projects/content-library/ by category | Makes AnythingLLM search more effective; consistent format aids retrieval |

### Workspace Editor

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-02-25 | Replace Logseq with VS Code as workspace markdown editor | Logseq not intuitive; VS Code is open source, familiar, works directly on Samba share as a folder — no app-specific concepts to learn |
| 2026-02-25 | Knowledge base function confirmed as AnythingLLM's role — not Logseq | AnythingLLM handles RAG/indexing; Logseq was only ever a markdown editor in this stack |
| 2026-02-25 | Drop workspace/logseq/ folder — no longer needed | Logseq graph folder redundant now VS Code is the editor; workspace root is the graph |
| 2026-02-25 | Logseq setup prioritized before Frank (Phase 8) | Shared profiles need real data; editing markdown tables in terminal impractical; Logseq via Samba is proper editing interface |
| 2026-02-25 | Fresh Logseq start: wipe %APPDATA%\Logseq and %LOCALAPPDATA%\Logseq | Previous Logseq attempts left stale config; clean slate ensures proper workspace connection — superseded by VS Code decision |
| 2026-02-23 | Start Logseq fresh — discard previous graph attempts | Previous setup was experimental and inconsistent — superseded by VS Code decision |
| 2026-02-23 | Logseq graph at workspace/logseq/ | Superseded — VS Code opens workspace root directly |

### AnythingLLM

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-02-23 | AnythingLLM reads workspace via Samba share | No file sync needed; reads directly from server |
| 2026-02-23 | Content-library/ is primary AnythingLLM workspace initially | Len's outputs are the most natural fit for RAG querying |

### Workspace Structure

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-02-24|Added projects/travel-planning/ with /trips, /ideas, /research structure|Joy's domain for holiday planning; /ideas = wish list, /research = active planning, /trips = confirmed/completed trips
| 2026-02-23 | Clean folder structure with personas/, projects/, logseq/, shared/ | Prevents the inconsistent mess that developed during initial dabbling |
| 2026-02-23 | shared/ folder for cross-persona reference files | User profile, dietary profile, music taste — personalises all assistants |
| 2026-02-23 | Start workspace restructure from scratch rather than reorganise | Old structure too inconsistent; clean slate faster and safer |
| 2026-02-23 | Discard pre-ZeroClaw Python scripts from food/ | Scripts predate persona/ZeroClaw approach; not compatible with new architecture |
| 2026-02-23 | Preserve food.db, schema.sql, seed_data.sql from food/ | Actual pantry data worth keeping; can be used when Frank is implemented |
| 2026-02-23 | Remove logseq/ folder for fresh setup | Previous graph misconfigured; easier to start clean than fix |

---

## Pending Decisions

These need to be resolved as we build:

| Question | Options | Notes |
|----------|---------|-------|
| Node.js installation method for MCP | rpm-ostree (reboot, cleanest) / nvm (no reboot, prefix issue) / toolbox (wrapper script needed) | rpm-ostree recommended; decision deferred to next session |
| Phase 15 calendar access scope | Just primary calendar / Multiple calendars (work, personal) | Start with primary; add others if needed |
| Phase 15 historical data range | Last 1-2 years / Last 3 years / All time | 3 years likely sufficient for Joy and Ziggy patterns |
| Phase 15 calendar write access | Read-only / Allow event creation (meal plans, gig bookings) | Start read-only; add write if valuable |
| Future Google services | Gmail (Len) / Drive (storage) / Photos / Contacts | MCP pattern proven; easy to add incrementally |
| Joy's integration with Ziggy|Coordinate trips around concerts / Keep separate|Potential synergy: "Plan weekend in Berlin for this gig" combining both personas
| Joy's booking capabilities|Advisory only / Can make bookings with approval|Start advisory only; booking integration requires payment/auth complexity
| Travel profile privacy|Included in git / Local only like health-profile|Contains less sensitive data than health-profile; safe to commit but review first
| How does Penny maintain session continuity? | Progress log file / memory_save tool / combination | Memory tool has 7-day archive — progress log more reliable for long-term |
| Ziggy's data sources for gigs | DuckDuckGo web search / dedicated gig APIs (Songkick etc.) | DuckDuckGo simplest to start; evaluate quality before adding API complexity |
| Bob's paused project | Unknown until reactivated | Record project details in DECISIONS.md when resumed |
| AnythingLLM model | Ollama local (qwen2.5) / Claude Haiku via LiteLLM | Local preferred for privacy; test quality on real content |
| Logseq sync back to workspace | Logseq writes directly to logseq/ via Samba | Logseq on Windows writes directly to Samba share — no extra sync needed |

---

## Completed Tasks

### Session 9: LiteLLM Multi-Key Configuration (2026-02-26)

**Result:** LiteLLM fully configured with key pooling and correct fallback chain

**Completed:**
- Three Gemini API keys configured as round-robin pool
- Two Groq API keys configured as fallback pool
- Root cause of all key failures identified and fixed (quoted values in env file)
- config.yaml restructured: single general_settings block, correct fallback syntax
- model_group_alias routing default → gemini-flash pool
- Rate limits moved to per-deployment rpm/tpm
- Ollama timeout increased to 120s

**Key learnings:**
- API key values must be unquoted in ~/.silverblue-ai-config
- os.environ/ is correct format — quotes were the problem
- Duplicate general_settings blocks silently drop the first block's values
- model_group_alias alone doesn't resolve fallbacks — explicit entry needed per group
- rate_limits is not a valid top-level LiteLLM config key

---

### Session 7: Logseq Setup Planning & Calendar Integration Design (2026-02-25)

**Result:** Phase 8 (Logseq) fully documented, Phase 15 (Calendar) planned

**Completed:**
- Created comprehensive Logseq fresh start guide
- Created all 7 profile templates for population via Logseq
- Designed Phase 15 Google Calendar integration via MCP
- Documented complete implementation plan (~3 hours estimated)
- Updated project files (DECISIONS.md, SESSIONS.md, STATE.md, TODO.md)

**Key outputs:**
1. `logseq-fresh-start.md` — Step-by-step Logseq reset and setup
2. `profile-templates.md` — Templates for all shared profiles and pantry.md
3. `phase-15-calendar-implementation.md` — Complete MCP calendar guide
4. `google-calendar-integration.md` — Overview of integration options

**Calendar integration features:**
- Joy learns from past holidays (destinations, timing, duration patterns)
- Ziggy learns from past gig attendance (artists, venues, frequency)
- Frank checks for restaurant bookings and dinner parties
- Extensible to Gmail, Drive, Contacts, Spotify via same MCP pattern

**Next session:** User implements Logseq setup, populates profiles

---

### Session 6 (2026-02-24)

**Result:** Phase 7 — MANDATORY FIRST STEP protocol, all personas updated

**Completed:**
- Fixed on-activation read issue: explicit file_read syntax + MANDATORY heading required
- Bob updated all five remaining persona files via Telegram
- All six personas now read domain files before every response ✅

---

### Session 5 (2026-02-24)

**Result:** Bob confirmed operational, dual-mode workflow live

**Completed:**
- Diagnosed file_read path issue (relative to workspace root)
- Bob read STATE.md, created directories, wrote SESSIONS.md ✅
- Bob self-corrected BOB.md ✅
- Dual-mode workflow confirmed live

---

### ZeroClaw Upgrade (2026-02-23)

**Result:** Successfully upgraded from v0.1.1 to v0.1.6

**Process:**
```bash
cd ~/zeroclaw
git pull                                    # Fetched latest code
git checkout v0.1.6                         # Switched to release tag (not main)
cargo build --release --locked              # Built from source
systemctl --user stop zeroclaw              # Stopped service to unlock binary
cp target/release/zeroclaw ~/.local/bin/    # Replaced binary
systemctl --user start zeroclaw             # Restarted service
```

**Key Learning:** Build from git tags (v0.1.6), not main branch - main had unreleased code with compilation errors (leak_detector.rs). Tags are stable releases.

**Verification:**
- `zeroclaw --version` → 0.1.6 ✅
- Telegram responding to messages ✅
- Service running without errors ✅

**New v0.1.6 Features Available:**
- Better encryption (ChaCha20-Poly1305 vs XOR)
- Telegram `mention_only` mode for group chats
- Improved Gemini thinking model support
- Security improvements

### Config.toml Fixes (2026-02-23)

**Result:** All critical config issues resolved

| Issue | Was | Now | Status |
|-------|-----|-----|--------|
| max_tokens | 512 | 4096 | ✅ Already correct in config |
| workspace path | /mnt/hdd/share/claw-projects | /var/home/mal/.zeroclaw/workspace | ✅ Already correct in config |
| http_request.allowed_domains | ["https://bbc.co.uk"] | ["*"] | ✅ Fixed - removed https:// prefix, changed to wildcard |

**Fix Applied:**
```bash
# Backup
cp config.toml config.toml.backup

# Fix allowed_domains
sed -i 's/allowed_domains = \["https:\/\/bbc.co.uk"\]/allowed_domains = ["*"]/' config.toml

# Restart to apply
systemctl --user restart zeroclaw
```

**Note:** Domain format must be bare domain names (e.g. "bbc.co.uk") or "*" - not URLs with https:// prefix.

**Impact:**
- Len can now fetch any web content for curation ✅
- Ziggy can search for gig information across any site ✅
- Local/private IPs still blocked for security ✅

### Workspace Restructure (2026-02-23)

**Result:** Clean folder layout established from scratch

**Final structure:**
```
workspace/
├── personas/               ← FRANK_PERSONA.md migrated from food/
├── projects/
│   ├── meal-planner/       ← food.db, schema.sql, seed_data.sql, meal_plan.md migrated from food/
│   ├── song-tutor/         ← role.md migrated from Song Tutor/
│   ├── dev-project/
│   ├── content-library/
│   └── live-music/
├── shared/
├── memory/                 ← ZeroClaw internal, untouched
├── state/                  ← ZeroClaw internal, untouched
└── cron/                   ← ZeroClaw internal, untouched
```

**What was discarded:**
- All pre-ZeroClaw Python scripts (food/, pantry scripts scattered in root)
- logseq/ (to be set up fresh)
- Test/scratch files (claw-test.txt, timer-test.txt, system-test.md, etc.)
- telegram_files/, journals/, pages/
- Miscellaneous root-level docs (exercise-tips.md, hydration-research.md, etc.)

**What was preserved:**
- `food.db` → projects/meal-planner/ (pantry data)
- `schema.sql`, `seed_data.sql` → projects/meal-planner/ (DB structure)
- `meal_plan.md` → projects/meal-planner/ (existing meal plan)
- `FRANK_PERSONA.md` → personas/ (persona definition work)
- `Song Tutor/role.md` → projects/song-tutor/role.md (Penny groundwork)
- `memory/`, `state/`, `cron/` — untouched (ZeroClaw internals)
- `.gitignore`, `GITASSISTANT.md` — kept at root

**Backup location:** `/var/home/mal/.zeroclaw/workspace-backup/` (safe to delete once satisfied)

---

## Things Deliberately Left For Later

| Item | Reason |
|------|--------|
| Branch workflow for significant changes | Current direct-to-main approach is fine for outputs |
| Multiple ZeroClaw instances | Too complex; persona file approach is sufficient |
| GitHub Actions integration | Nice to have; not needed for core workflow |
| Bob's dev project | On pause; activate when ready |
| Ziggy API integrations (Songkick etc.) | DuckDuckGo first; evaluate quality before adding complexity |
| Frank persona implementation | Phase 9 after Logseq (Phase 8) complete |
| workspace-backup/ cleanup | Delete once confident nothing was missed |
| Spotify MCP integration | After calendar MCP proven in Phase 15 |
| Gmail MCP integration | After calendar MCP proven in Phase 15 |
| Google Drive MCP integration | After calendar MCP proven in Phase 15 |
| Anthropic Haiku in auto fallback chain | Moved to explicit-only; Ollama preferred for cost/privacy |
