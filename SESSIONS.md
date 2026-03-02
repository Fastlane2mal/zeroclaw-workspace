# Development Sessions — Silverblue AI Workspace

Log of Claude sessions working on the platform. Most recent session first.

---

## Session 11 — 2026-02-28 / 2026-03-01

**Focus:** Simplification, tool calling fix, Bob optimisation, GitHub cleanup

### Completed
- Simplified LiteLLM config — removed desktop PC Ollama and local Ollama tiers
- Discovered Groq/Gemini incompatible with ZeroClaw tool calling
- Tried multiple free options: openrouter/auto (charges), openrouter/free (invalid ID), Kimi K2 (no free tier), gpt-oss models blocked by privacy settings
- Fixed OpenRouter privacy settings — enabled free endpoint options
- Confirmed gpt-oss-20b:free working — cost:0, OpenAI-format tool calling, ZeroClaw compatible
- Confirmed gpt-oss-120b:free available as second pool entry
- Multiple OpenRouter accounts confirmed poolable in LiteLLM config
- Bob confirmed as default persona and system orchestrator
- SOUL.md updated — Bob is default, not neutral coordinator
- BOB.md optimised — trimmed, standard diagnostic added, session start git check added, secret hygiene rules added
- RUNBOOK.md created — 10 procedures covering all common platform tasks
- QUICK-REFERENCE.md updated with key rotation command
- Bob weekly report produced — correctly identified git push failures
- Discovered secrets (Groq + Anthropic API keys) committed in projects/dev-project/docs/config.yaml
- Keys rotated immediately
- Git history cleaned using git-filter-repo via toolbox container
- Force push succeeded — GitHub clean, no secrets violation
- projects/dev-project/docs/config.yaml added to .gitignore
- Identified Bob cannot execute systemctl commands — policy blocked

### Key Decisions
- openrouter/auto charges — routes to paid models, not free
- gpt-oss-20b/120b:free confirmed as only reliable free ZeroClaw-compatible models
- OpenRouter free tier requires privacy settings enabled at openrouter.ai/settings/privacy
- OpenRouter $10 lifetime credit unlocks 1000 free req/day permanently
- Multiple OpenRouter accounts can be pooled — limits multiply per account not per key
- Bob is permanent system orchestrator — not temporary caretaker
- RUNBOOK.md is Bob's procedure reference — consult before any config change
- git-filter-repo via toolbox is the correct history cleanup method on Silverblue

### Issues Encountered
- openrouter/auto charged for usage — routes to paid models
- Kimi K2 has no free tier on OpenRouter
- gpt-oss free models blocked by OpenRouter privacy settings
- Bob hallucinating tool execution — free model reliability issue
- Bob committed API keys to git history — secrets in projects/dev-project/docs/config.yaml
- systemctl commands policy-blocked in ZeroClaw — Bob cannot check service status

### Next Session
1. Investigate systemctl policy block in ZeroClaw config.toml
2. Test Bob's standard diagnostic routine end-to-end
3. Test Bob's session start routine in a fresh session
4. Verify Bob can read RUNBOOK.md
5. Update SOUL.md to reflect Bob as default with others archived
6. Add second OpenRouter account key to LiteLLM config

---

## Session 10 — 2026-02-27

**Focus:** LiteLLM config finalisation — desktop PC as primary, named groups, fallback chain
*(Config since superseded by Session 11 simplification)*

---

## Session 9 — 2026-02-26

**Focus:** LiteLLM multi-key configuration and debugging

### Key learnings
- API key values must be unquoted in ~/.silverblue-ai-config
- os.environ/ is correct format — quotes were the problem
- Duplicate general_settings blocks silently drop first block's values
- model_group_alias alone insufficient — explicit entry needed per group name

---

## Session 8 — 2026-02-25

**Focus:** Phase 15 Calendar MCP research, Node.js planning, Logseq → VS Code switch

---

## Session 7 — 2026-02-25

**Focus:** Logseq setup planning & Google Calendar integration design

---

## Session 6 — 2026-02-24

**Focus:** MANDATORY FIRST STEP protocol, all personas updated

---

## Sessions 1-5 — 2026-02-23 to 2026-02-24

**Focus:** Infrastructure, workspace restructure, persona system, Bob operational
