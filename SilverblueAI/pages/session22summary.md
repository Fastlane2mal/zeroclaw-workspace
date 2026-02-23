# Session 22 Summary - ZeroClaw Deployment

**Date**: 2026-02-20 / 2026-02-21  
**Duration**: ~5 hours  
**Status**: ⚠️ Partially complete — core working, tool execution blocked by upstream bug  
**Next Session**: Investigate ZeroClaw tool execution bug, check GitHub issues

---

## Session Objectives

1. Remove AnythingLLM from server
2. Deploy ZeroClaw as replacement AI agent
3. Configure Telegram channel
4. Enable web research capability
5. Enable file read/write to Samba share

---

## What We Accomplished

### ✅ AnythingLLM Removed

- Stopped and removed container with `podman rm --force` (SIGKILL required — normal behaviour)
- Removed image `docker.io/mintplexlabs/anythingllm:latest` (~3.19GB)
- Removed orphaned image layers (~10GB total freed)
- Data preserved at `/mnt/hdd/projects/anythingllm-storage`
- RAM freed: ~300-800MB

### ✅ ZeroClaw Built and Installed

- Build tools layered via rpm-ostree: `gcc`, `openssl-devel`, `rust`, `cargo`
- Cloned from canonical repo: `github.com/zeroclaw-labs/zeroclaw` (not RightNow-AI fork)
- Built with `cargo build --release --locked` (~8 minutes on i5-8250U)
- Installed to `~/.local/bin/zeroclaw` (not `~/.cargo/bin` — avoids PATH issues)
- Binary: ~3.4MB, RAM usage: ~10MB

### ✅ ZeroClaw Configured

- Ran `zeroclaw onboard --interactive` (9-step wizard)
- Config at `~/.zeroclaw/config.toml` (chmod 600)
- Workspace: `~/.zeroclaw/workspace` (default)
- Telegram bot configured and working
- Tailscale private tailnet tunnel active
- Gateway on `127.0.0.1:3000`

### ✅ Systemd Service Running

- Installed via `zeroclaw service install`
- Runs `zeroclaw daemon` (gateway + channels + scheduler + heartbeat)
- Auto-starts on boot
- Service: `~/.config/systemd/user/zeroclaw.service`

### ✅ Telegram Working

- Bot responding via Telegram from Windows PC
- Accessible via Tailscale private tailnet
- Response time: 1-3 seconds via OpenRouter/Gemini

### ✅ Web Research Working

- DuckDuckGo search enabled
- HTTP fetch enabled
- **Critical finding**: Must add `web_search` and `http_fetch` to `auto_approve` list — enabling them in config alone is not sufficient

### ⚠️ File Write — Blocked by Upstream Bug

- Model correctly generates `tool_code` blocks
- ZeroClaw does not execute them — returns ~600ms (no dispatch)
- Affects all providers tested
- Documented in Known Issues section of deployment guide

---

## Technical Discoveries

### Discovery 1: ZeroClaw is Not on crates.io

Must be built from GitHub source. `cargo install zeroclaw --locked` fails with package not found.

### Discovery 2: Groq Native Provider Broken (v0.1.0)

All calls fail with:
```
Unknown request URL: POST /openai/responses
```
ZeroClaw sends requests to a Groq Responses API endpoint that doesn't exist. Do not use `default_provider = "groq"`.

### Discovery 3: LiteLLM custom: Provider — Tool Execution Broken

Conversation works but tool calls are narrated not executed. The model returns `tool_code` blocks as text; ZeroClaw doesn't parse and dispatch them. Not suitable for agentic tasks.

### Discovery 4: OpenRouter is the Working Provider

Native ZeroClaw support, fast, reliable. Gemini models work for conversation. Tool execution still broken (same `tool_code` issue) but this appears to be a ZeroClaw dispatch bug not a provider issue.

### Discovery 5: auto_approve Controls Tool Surfacing

Tools enabled in config (`web_search`, `http_request`) are NOT offered to the model unless they also appear in the `[autonomy]` `auto_approve` list. This is undocumented and non-obvious.

### Discovery 6: zeroclaw daemon vs zeroclaw serve

`zeroclaw serve` is not a valid command. The correct command for running ZeroClaw persistently (gateway + channels + scheduler) is `zeroclaw daemon`. The service file uses this automatically.

### Discovery 7: systemd Service Auto-Restarts

Running `zeroclaw daemon` manually while the service is running causes "Address already in use" errors and Telegram 409 conflicts. Always use `systemctl --user restart zeroclaw` — never run the daemon manually.

### Discovery 8: Samba Permissions Required for New Directories

New directories under `/mnt/hdd/share` require explicit `chmod 755` and `chown mal:mal` before they appear in the Windows Samba share. Creating the directory alone is not sufficient.

### Discovery 9: workspace Key in config.toml Ignored

Setting `workspace = "/path"` in config.toml has no effect — ZeroClaw always uses `~/.zeroclaw/workspace`. This may be a v0.1.0 limitation.

---

## Provider Status Summary (v0.1.0)

| Provider | Conversation | Tool Execution | Notes |
|----------|-------------|----------------|-------|
| `openrouter` + Gemini Flash | ✅ Working | ❌ tool_code not executed | Best option currently |
| `openrouter` + Mistral free | ✅ Working | ❌ tool_code not executed | Rate limits on free tier |
| `custom:` (LiteLLM) | ✅ Working | ❌ tool_code not executed | All models tested |
| `ollama` + mistral | ✅ Working | ❌ not tested fully | Too slow (~25s) |
| `groq` (native) | ❌ Broken | ❌ Broken | Wrong API endpoint |

---

## Configuration Changes Made

### ~/.zeroclaw/config.toml (key changes from wizard defaults)

```toml
# Provider (changed from ollama to openrouter)
default_provider = "openrouter"
default_model = "google/gemini-2.0-flash-001"
api_key = "<openrouter-key>"

# Autonomy (added web tools to auto_approve)
[autonomy]
auto_approve = ["file_read", "file_write", "memory_recall", "web_search", "http_fetch"]

# Web research (enabled)
[web_search]
enabled = true

[http_request]
enabled = true
```

### ~/.config/systemd/user/zeroclaw.service

Generated by `zeroclaw service install`. Runs `zeroclaw daemon`.

---

## Config TOML Pitfalls Encountered

1. **`[[providers]]` double brackets required** for array of provider definitions (single `[providers]` causes duplicate key error)
2. **`api_key` must be top-level** — not in a providers block, not from env var
3. **`max_actions_per_hour` must be inside `[autonomy]`** before array fields
4. **`workspace_only` is a required field** in `[autonomy]` — deleting it breaks startup
5. **Two keys on one line** — nano line editing can merge lines; always verify after saving

---

## System State After Session

```
Services running:
- Ollama: ✅ active (auto-start)
- LiteLLM: ✅ active (auto-start)  
- ZeroClaw: ✅ active (auto-start, new)
- SSH, Samba, Tailscale: ✅ active

ZeroClaw status:
- Provider: OpenRouter / google/gemini-2.0-flash-001
- Channel: Telegram ✅
- Web search: ✅ enabled
- File write: ❌ blocked (upstream bug)
- Gateway: 127.0.0.1:3000
- Tunnel: Tailscale private tailnet

RAM usage: ~5.3GB / 11GB (ZeroClaw adds ~10MB)
HDD: AnythingLLM images removed (~10GB freed)
```

---

## Documents Updated

- **ZEROCLAW_DEPLOYMENT.md** → v1.8
  - Correct onboarding wizard answers
  - OpenRouter as working provider (not Groq)
  - auto_approve fix for web tools
  - Known Issues section (tool execution, Groq bug, rate limits)
  - Comprehensive troubleshooting from real deployment experience
  - Provider status table

---

## Outstanding Issues

### Issue 1: Tool Execution Not Working ⚠️ OPEN
**Problem**: ZeroClaw v0.1.0 does not execute tool calls — model generates `tool_code` blocks that are returned as text  
**Impact**: File read/write via AI agent not working  
**Next step**: Check `github.com/zeroclaw-labs/zeroclaw/issues` for `tool_dispatcher`, `tool_code`, `file_write`  
**Workaround**: None

### Issue 2: Groq Native Provider Broken ⚠️ OPEN
**Problem**: Wrong API endpoint in v0.1.0  
**Impact**: Cannot use Groq directly — must use OpenRouter  
**Next step**: Check GitHub issues or wait for v0.1.1  
**Workaround**: Use `openrouter` provider instead

---

## Next Session Plan

1. Check ZeroClaw GitHub issues for tool execution bug
2. If fix available: update binary, retest file write
3. If no fix: investigate `tool_dispatcher` config options or alternative approaches
4. Consider: does ZeroClaw need a specific model format for tool calls? Test with `anthropic-custom:` pointing at LiteLLM → Claude
5. Update SESSION_HISTORY_ARCHIVE.md and STATE files

### Prompt for Next Session

```
I have ZeroClaw v0.1.0 deployed on Fedora Silverblue as a systemd 
user service. It is working for conversation and web research via 
Telegram, but tool execution (file_write, file_read) is broken.

The model generates tool_code blocks correctly but ZeroClaw does 
not execute them — it returns the tool_code as text output with 
~600ms response time indicating no dispatch occurs.

config: tool_dispatcher = "auto"
Provider tested: openrouter/google/gemini-2.0-flash-001
Also tested: custom:http://localhost:4000/v1 (LiteLLM), ollama/mistral

Please load the project documentation and help me:
1. Check if this is a known bug with a fix
2. Find the correct tool call format ZeroClaw expects
3. Identify which provider/model combination would make tool 
   execution work
```

---

## Key Files

| File | Location | Purpose |
|------|----------|---------|
| Deployment guide | `ZEROCLAW_DEPLOYMENT.md` | Full deployment reference (v1.8) |
| Config | `~/.zeroclaw/config.toml` | ZeroClaw runtime config |
| Service | `~/.config/systemd/user/zeroclaw.service` | systemd service |
| Binary | `~/.local/bin/zeroclaw` | Built from source |
| Source | `~/zeroclaw/` | Keep for rebuilds |
| AnythingLLM data | `/mnt/hdd/projects/anythingllm-storage` | Preserved, not deleted |

---

**Session End**: 2026-02-21 ~01:30 GMT  
**Status**: ⚠️ Core working, tool execution blocked by upstream bug  
**Next Session**: Tool execution investigation
