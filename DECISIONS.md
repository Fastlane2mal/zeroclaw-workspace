# Silverblue AI Workspace — Decisions Log

This document records key decisions made during the design and implementation 
of the Silverblue AI Workspace. Update this as new decisions are made.

---

## Decisions Made

### Infrastructure

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-02-28 | OpenRouter auto router as primary LLM for ZeroClaw | Only provider confirmed compatible with ZeroClaw tool calling on free tier; routes to best available free model automatically |
| 2026-02-28 | Groq and Gemini demoted to fallback only | Both incompatible with ZeroClaw tool calling — output raw tool syntax instead of executing; fine for conversational fallback only |
| 2026-02-28 | Simplified to Bob-only persona; others archived to personas/archive/ | Focus on getting one persona fully working before reactivating others; reduces complexity during platform stabilisation |
| 2026-02-28 | Profile population deferred until other personas reactivated | Profiles serve Frank, Ziggy, Joy etc — no value populating them while those personas are shelved |
| 2026-02-28 | If OpenRouter free tier unreliable, switch primary to Claude Haiku via OpenRouter | Haiku is Claude-compatible (confirmed working), cheap (fractions of a cent per message), available via existing OpenRouter key |
| 2026-02-28 | Final LiteLLM fallback chain: openrouter/auto → groq → gemini | OpenRouter primary for tool calling; Groq fast conversational fallback; Gemini last resort |
| 2026-02-26 | Node.js installation method deferred — decision pending (Session 8) | Three options evaluated: rpm-ostree (reboot required, cleanest for systemd), nvm (no reboot, Silverblue prefix issue), toolbox (needs wrapper script); rpm-ostree recommended |
| 2026-02-25 | MCP server choice: nspady/google-calendar-mcp (@cocal/google-calendar-mcp npm) | 964 stars, most actively maintained, read-only support via enabled_tools, npx-based (no global install), persistent OAuth tokens |
| 2026-02-25 | Google Calendar via MCP for Joy, Ziggy, Frank (Phase 15) | Real-time calendar access; personas learn from past events; native ZeroClaw MCP support; secure OAuth; extensible to other Google services |
| 2026-02-25 | Calendar tokens stored in ~/.zeroclaw/secrets/ (gitignored) | Keep OAuth tokens local and secure; never committed to GitHub |
| 2026-02-25 | Read-only calendar access (calendar.readonly scope) initially | Safety: personas can't accidentally modify calendar; users retain full control |
| 2026-02-24 | Drop food.db, schema.sql, seed_data.sql — use pantry.md instead | file_read can't read SQLite binary format; markdown is simpler, human-editable, git-diffable |
| 2026-02-24 | Persona file_read paths must be relative to workspace root | ZeroClaw resolves file_read via workspace_dir.join(path) — absolute paths don't work |
| 2026-02-24 | Use explicit file_read syntax + MANDATORY heading for on-activation reads | Descriptive instructions alone not sufficient — model skips reads without explicit tool call syntax |
| 2026-02-24 | Hybrid persona approach: neutral SOUL.md + single personas skill | Token-efficient; all six personas in one skill avoids conflicts; personas loaded on demand |
| 2026-02-24 | Trigger pattern: "Hey [Name]" / "@[name]" / "[Name]:" for persona activation | Natural Telegram phrasing; consistent across all personas |
| 2026-02-24 | [[tools]] section not needed in SKILL.toml for ZeroClaw built-in tools | Built-ins don't require declaration; adding [[tools]] without command field causes skill to be skipped |
| 2026-02-24 | SOUL.md goes at workspace root, not in personas/ | Loaded by load_openclaw_bootstrap_files() from workspace_dir |
| 2026-02-23 | Use systemd timers (not cron) for auto-commit and push | Cron not available by default on Fedora Silverblue |
| 2026-02-23 | Auto-commit every 15 minutes, push to GitHub hourly | Balance between granularity and network overhead |
| 2026-02-23 | SSH key authentication for GitHub (not personal access tokens) | More secure, no plaintext credentials |
| 2026-02-23 | All workspace at /var/home/mal/.zeroclaw/workspace | Single source of truth, git-backed |
| 2026-02-23 | Samba share as bridge to Windows desktop tools | No file copying needed — VS Code and AnythingLLM read directly |
| 2026-02-23 | Upgraded ZeroClaw v0.1.1 → v0.1.6 | Security improvements, better Telegram support, new features |
| 2026-02-23 | Build ZeroClaw from git tags (not main branch) | main branch can have unreleased/buggy code; tags are stable releases |

### LiteLLM

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-02-28 | openrouter/auto as primary — ZeroClaw tool calling compatible | ZeroClaw uses Claude-compatible tool call format; Groq/Gemini/Llama models incompatible |
| 2026-02-28 | Groq demoted to fallback — conversational only | Tool calling broken with ZeroClaw; fast and reliable for plain responses |
| 2026-02-28 | Gemini demoted to last resort | Tool calling broken; quota fragile (~250 req/day/project); useful only as emergency fallback |
| 2026-02-28 | OpenRouter $10 lifetime credit unlocks 1000 free req/day | One-time cost; balance can drop below $10 after purchase and limit is retained |
| 2026-02-28 | Claude Haiku via OpenRouter as upgrade path if free tier unreliable | Confirmed Claude-compatible; ~fractions of a cent per message; same API key as free tier |
| 2026-02-27 | Final config uses three named model groups: ollama-pc, cloud, local | Since superseded by simplified openrouter/groq/gemini config |
| 2026-02-26 | Three Gemini API keys configured as pool (GOOGLE_API_KEY_1/2/3) | Rate limits per project not per key — only multiplies quota if different projects |
| 2026-02-26 | Two Groq API keys configured as pool (GROQ_API_KEY_1/2) | Doubles Groq free tier capacity |
| 2026-02-26 | API keys stored without quotes in ~/.silverblue-ai-config | LiteLLM URL-encodes quoted values (%22) causing invalid key errors |
| 2026-02-26 | os.environ/ format confirmed correct for LiteLLM config.yaml | Quotes in env file were root cause of key resolution failures |
| 2026-02-26 | general_settings must have single block | Duplicate blocks cause later block to override earlier; master_key was being silently dropped |
| 2026-02-26 | LITELLM_MASTER_KEY required in ZeroClaw config.toml | LiteLLM proxy enforces auth; ZeroClaw must send key in api_key field |

### Personas

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-02-28 | Bob as sole active persona; others archived | Simplify platform — get one persona fully working before expanding |
| 2026-02-28 | Persona files at personas/BOB.md (uppercase) | Confirmed correct path; SKILL.toml must reference this exact path |
| 2026-02-24 | Added Joy (travel planner) as sixth persona | Clear use case for research-heavy planning — deferred until platform stable |
| 2026-02-23 | Five named personas: Frank, Penny, Bob, Len, Ziggy | Named characters maintain consistent personality better than generic roles |
| 2026-02-23 | Personas stored as .md files in workspace/personas/ | Easy to edit, version controlled, ZeroClaw can read them as context |

### Workspace Editor

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-02-25 | Replace Logseq with VS Code as workspace markdown editor | Logseq not intuitive; VS Code familiar, works directly on Samba share as folder |
| 2026-02-25 | Knowledge base function confirmed as AnythingLLM's role | AnythingLLM handles RAG/indexing; VS Code is just the editor |

---

## Pending Decisions

| Question | Options | Notes |
|----------|---------|-------|
| Node.js installation method for MCP | rpm-ostree (reboot, cleanest) / nvm / toolbox | rpm-ostree recommended; deferred to Phase 15 |
| OpenRouter free tier reliability | Keep auto / Switch to Claude Haiku | Monitor in use; Haiku is upgrade path if needed |
| Phase 15 calendar access scope | Just primary calendar / Multiple calendars | Start with primary |
| Phase 15 calendar write access | Read-only / Allow event creation | Start read-only |
| Future Google services | Gmail / Drive / Photos / Contacts | After calendar MCP proven |

---

## Completed Tasks

### Session 11: Simplification & Tool Calling Fix (2026-02-28)

**Result:** Bob operational with working tool calling via OpenRouter

**Completed:**
- Simplified LiteLLM config — removed desktop PC Ollama and local Ollama
- Discovered Groq/Gemini incompatible with ZeroClaw tool calling
- Identified OpenRouter auto router as solution — free models with tool calling support
- Confirmed tool calling working — Bob reading/writing files via Telegram ✅
- Resolved Bob persona file path issue (personas/BOB.md uppercase)
- Archived other personas to personas/archive/
- Deferred profile population until other personas reactivated
- Updated fallback chain: openrouter/auto → groq → gemini

**Key learnings:**
- ZeroClaw tool calling requires Claude-compatible format
- Groq and Gemini (Llama-based models) output raw tool syntax — incompatible
- OpenRouter auto router correctly routes to free models that support tool calling
- OpenRouter $10 lifetime credit unlocks 1000 req/day on free models permanently

---

### Session 10: LiteLLM Multi-Provider Config (2026-02-27)

**Result:** Desktop PC Ollama added as primary; named groups with fallbacks  
*(Since superseded by Session 11 simplification)*

---

### Session 9: LiteLLM Multi-Key Configuration (2026-02-26)

**Result:** LiteLLM fully configured with key pooling and correct fallback chain

**Key learnings:**
- API key values must be unquoted in ~/.silverblue-ai-config
- os.environ/ is correct format — quotes were the problem
- Duplicate general_settings blocks silently drop first block's values
- model_group_alias alone insufficient — explicit entry needed per group name
- rate_limits is not a valid top-level LiteLLM config key

---

### Session 7: Logseq Setup Planning & Calendar Integration Design (2026-02-25)

**Result:** Phase 8 documented, Phase 15 planned, Logseq replaced by VS Code

---

### Session 6: MANDATORY FIRST STEP Protocol (2026-02-24)

**Result:** All personas updated with explicit file_read syntax on activation

---

### Sessions 1-5 (2026-02-23 to 2026-02-24)

**Result:** Infrastructure, workspace restructure, persona system, Bob operational

---

## Things Deliberately Left For Later

| Item | Reason |
|------|--------|
| Other personas (Frank, Penny, Len, Ziggy, Joy) | Archived — reactivate once Bob workflow proven |
| Profile population (Phase 8) | Not needed until other personas reactivated |
| Phase 15 Google Calendar MCP | Deferred — prerequisites not met |
| Spotify MCP | After calendar MCP proven |
| Gmail/Drive MCP | After calendar MCP proven |
| workspace-backup/ cleanup | Delete once confident nothing missed |
| Branch workflow for significant changes | Direct-to-main fine for current stage |

---

### Session 11 Additional Decisions (2026-03-01)

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-03-01 | gpt-oss-20b/120b:free via OpenRouter as primary | Only confirmed free models compatible with ZeroClaw tool calling; OpenAI-format tool use |
| 2026-03-01 | OpenRouter privacy settings must have free endpoints enabled | Free models blocked by default — enable "free endpoints that may train on inputs" and "free endpoints that may publish prompts" |
| 2026-03-01 | Multiple OpenRouter accounts can be pooled in LiteLLM | Rate limits are per account not per key — separate accounts multiply free tier capacity |
| 2026-03-01 | git-filter-repo via toolbox is correct history cleanup method on Silverblue | pip not available on host; toolbox provides mutable container; same home directory accessible |
| 2026-03-01 | RUNBOOK.md added to workspace root | Bob needs explicit procedures to follow — reduces hallucination and prevents incidents like secrets in git |
| 2026-03-01 | projects/dev-project/docs/config.yaml added to .gitignore | Prevent recurrence of secrets being committed |
