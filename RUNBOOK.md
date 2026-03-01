# Silverblue AI Platform — Runbook

**Owner:** Bob (primary persona and system orchestrator)  
**Last updated:** 2026-02-28  
**Purpose:** Step-by-step procedures for common platform tasks. Consult this before making any config changes or running platform commands.

---

## 1. Standard Diagnostic

Run this whenever something seems wrong or Malcolm asks for a platform check.

```bash
# Step 1 — ZeroClaw health
systemctl --user status zeroclaw --no-pager
journalctl --user -u zeroclaw -n 10 --no-pager

# Step 2 — LiteLLM health
systemctl --user status litellm --no-pager
journalctl --user -u litellm -n 10 --no-pager

# Step 3 — Timers
systemctl --user list-timers --no-pager

# Step 4 — Git sync
tail -20 /var/home/mal/.zeroclaw/push.log
cd /var/home/mal/.zeroclaw/workspace && git status
git log --oneline -5

# Step 5 — LiteLLM ping
curl -s -X POST http://localhost:4000/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"default","messages":[{"role":"user","content":"ping"}]}' \
  --max-time 10
```

**Report each result clearly. Flag anything abnormal. Do not guess — report what the commands actually return.**

**What to look for:**
- ZeroClaw: `Active: active (running)` — anything else needs investigation
- LiteLLM: `Active: active (running)` — anything else needs investigation
- Timers: both `zeroclaw-autocommit.timer` and `zeroclaw-push.timer` should be active
- Git: no uncommitted changes older than 15 minutes; last push within 1 hour
- LiteLLM ping: response `model` field should show `gpt-oss-20b` or `gpt-oss-120b` — if it shows `llama-3.3-70b-versatile` OpenRouter free tier is failing

---

## 2. Log Interpretation Guide

### LiteLLM logs — what to look for

| Log entry | Meaning | Action |
|-----------|---------|--------|
| `x-litellm-attempted-fallbacks: 1` | Primary model failed, fell back | Check why primary failed |
| `x-litellm-model-group: groq` when default expected | OpenRouter is failing | Check OpenRouter status |
| `429` | Rate limit or quota exhausted | Wait for reset or check quota |
| `400 Bad Request` | Wrong model name or config error | Check model ID in config.yaml |
| `401` | Auth failure | Check LITELLM_MASTER_KEY |
| `RateLimitError` | Quota exhausted | Reduce rpm in config or wait |
| `Key 'x' is not a valid argument` | Invalid config parameter | Remove the parameter |
| `free is not a valid model ID` | Wrong OpenRouter model format | Check model ID format |
| `No endpoints found matching your data policy` | OpenRouter privacy settings blocking free models | Enable free endpoints at openrouter.ai/settings/privacy |

### ZeroClaw logs — what to look for

| Log entry | Meaning | Action |
|-----------|---------|--------|
| `tool call validation failed` | Model incompatible with ZeroClaw tool format | Switch to OpenAI-compatible model |
| `file not found` | Wrong file path | Check path is relative to workspace root |
| `connection refused` on port 4000 | LiteLLM not running | Restart LiteLLM |
| `max_actions_per_hour exceeded` | ZeroClaw rate limit hit | Wait for cooldown |
| Raw tool call syntax in response | Model outputting tool calls as text instead of executing | Model incompatible — switch provider |

---

## 3. LiteLLM Config Change Procedure

**Always follow this procedure. Never edit config.yaml without these steps.**

```bash
# Step 1 — Read current config
cat /var/home/mal/.litellm/config.yaml

# Step 2 — Show proposed change to Malcolm and wait for approval

# Step 3 — Make change using str_replace (never rewrite whole file)

# Step 4 — Restart LiteLLM
systemctl --user restart litellm

# Step 5 — Wait for startup
sleep 10

# Step 6 — Verify models loaded
curl -s http://localhost:4000/v1/models \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" | python3 -m json.tool

# Step 7 — Test ping
curl -s -X POST http://localhost:4000/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"default","messages":[{"role":"user","content":"ping"}]}' \
  --max-time 30

# Step 8 — Confirm model in response is expected provider (not a fallback)
```

---

## 4. ZeroClaw Config Change Procedure

```bash
# Step 1 — Read current config
cat /var/home/mal/.zeroclaw/config.toml

# Step 2 — Show proposed change to Malcolm and wait for approval

# Step 3 — Make change using str_replace

# Step 4 — Validate
zeroclaw doctor

# Step 5 — Restart
systemctl --user restart zeroclaw

# Step 6 — Check logs
journalctl --user -u zeroclaw -n 20 --no-pager

# Step 7 — Confirm responding via Telegram
```

---

## 5. API Key Rotation Procedure

**Run this whenever Malcolm rotates an API key.**

```bash
# Step 1 — Malcolm updates the key value in ~/.silverblue-ai-config
# (Bob should never edit this file directly)

# Step 2 — Regenerate LiteLLM env file
sed 's/^export //; s/"//g' ~/.silverblue-ai-config > ~/.config/litellm.env

# Step 3 — Restart LiteLLM
systemctl --user restart litellm

# Step 4 — Wait for startup
sleep 10

# Step 5 — Test the affected provider
curl -s -X POST http://localhost:4000/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"default","messages":[{"role":"user","content":"ping"}]}' \
  --max-time 30

# Step 6 — Confirm response is from expected provider
```

**Important:** If a key was exposed in git history, Malcolm must also revoke the old key at the provider's dashboard before rotation is complete.

---

## 6. Git Sync Troubleshooting

### Check why GitHub hasn't been updated

```bash
# Check timer status
systemctl --user status zeroclaw-push.timer
systemctl --user status zeroclaw-autocommit.timer

# Check push log for errors
cat /var/home/mal/.zeroclaw/push.log

# Check git status
cd /var/home/mal/.zeroclaw/workspace
git status
git log --oneline -5

# Manual push if needed (ask Malcolm for approval first)
~/.local/bin/zeroclaw-push.sh
```

### Common git push failures

| Error | Cause | Action |
|-------|-------|--------|
| `push declined due to repository rule violations` | Secrets detected in commit history | Do NOT attempt git history rewrite without Malcolm's approval — report the specific files and commits flagged |
| `Permission denied (publickey)` | SSH key issue | Check `~/.ssh/config` and GitHub SSH key |
| `rejected: non-fast-forward` | Remote has changes local doesn't | Run `git pull --rebase` then push again |
| `Repository not found` | Wrong remote URL | Check `git remote -v` |

### Before ANY commit

```bash
# Always check what is staged first
git status
git diff --staged

# Check for accidentally staged sensitive files
git diff --staged | grep -i "api_key\|password\|secret\|token"
```

**If sensitive data is found in staged files — stop immediately. Do not commit. Report to Malcolm.**

---

## 7. Secret Hygiene Procedure

### Before writing any file to workspace

1. Does the file contain or could it contain API keys, passwords, tokens, or credentials?
2. If yes — stop. Ask Malcolm how to handle it.
3. Config files referencing API keys must use `os.environ/KEY_NAME` format only
4. Never write actual key values to any workspace file

### Files that must never be committed

Add to `.gitignore` if not already present:

```bash
# Check current gitignore
cat /var/home/mal/.zeroclaw/workspace/.gitignore

# Add sensitive files if missing
echo "shared/health-profile.md" >> /var/home/mal/.zeroclaw/workspace/.gitignore
echo "projects/*/docs/config.yaml" >> /var/home/mal/.zeroclaw/workspace/.gitignore
echo "*.env" >> /var/home/mal/.zeroclaw/workspace/.gitignore
echo "*secrets*" >> /var/home/mal/.zeroclaw/workspace/.gitignore
echo "*credentials*" >> /var/home/mal/.zeroclaw/workspace/.gitignore
```

### If secrets are accidentally committed

1. Stop all push timers immediately: `systemctl --user stop zeroclaw-push.timer`
2. Report to Malcolm — do not attempt to fix without approval
3. Malcolm must rotate the exposed keys immediately
4. History cleanup requires Malcolm's explicit approval and involvement
5. Restart push timer after cleanup: `systemctl --user start zeroclaw-push.timer`

---

## 8. Service Restart Procedures

### Full platform restart (all services)

```bash
# Stop everything
systemctl --user stop zeroclaw
systemctl --user stop litellm

# Start in order
systemctl --user start litellm
sleep 15
systemctl --user start zeroclaw

# Verify
systemctl --user status litellm --no-pager
systemctl --user status zeroclaw --no-pager
```

### Restart a single service

```bash
# ZeroClaw only
systemctl --user restart zeroclaw
journalctl --user -u zeroclaw -n 20 --no-pager

# LiteLLM only
systemctl --user restart litellm
sleep 10
journalctl --user -u litellm -n 20 --no-pager
```

---

## 9. Persona Management

### Activating a persona

```bash
# Step 1 — Check archive
ls /var/home/mal/.zeroclaw/workspace/personas/archive/

# Step 2 — Copy persona file to active location
cp /var/home/mal/.zeroclaw/workspace/personas/archive/FRANK.md \
   /var/home/mal/.zeroclaw/workspace/personas/FRANK.md

# Step 3 — Update SOUL.md trigger if needed
# Step 4 — Restart ZeroClaw
systemctl --user restart zeroclaw

# Step 5 — Test persona activation via Telegram
```

### Archiving a persona

```bash
# Step 1 — Move persona file to archive
mv /var/home/mal/.zeroclaw/workspace/personas/FRANK.md \
   /var/home/mal/.zeroclaw/workspace/personas/archive/FRANK.md

# Step 2 — Restart ZeroClaw
systemctl --user restart zeroclaw
```

---

## 10. Weekly Platform Health Report

Run this once a week and save output to `projects/reports/YYYY-MM-DD-weekly.md`:

```bash
# Service status
systemctl --user status zeroclaw litellm --no-pager

# Git activity this week
cd /var/home/mal/.zeroclaw/workspace
git log --oneline --since="7 days ago"

# Push log summary
tail -50 /var/home/mal/.zeroclaw/push.log

# Timer health
systemctl --user list-timers --no-pager

# LiteLLM ping
curl -s -X POST http://localhost:4000/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"default","messages":[{"role":"user","content":"ping"}]}' \
  --max-time 10
```

**Report should include:**
- Services status (healthy/degraded/down)
- Git sync status (last commit, last push, any failures)
- TODO items completed this week
- Any errors encountered and how resolved
- What's next (top 3 priorities from TODO.md)

---

## Key Paths Reference

| Item | Path |
|------|------|
| Workspace | /var/home/mal/.zeroclaw/workspace/ |
| ZeroClaw config | /var/home/mal/.zeroclaw/config.toml |
| LiteLLM config | /var/home/mal/.litellm/config.yaml |
| API keys | /var/home/mal/.silverblue-ai-config |
| LiteLLM env file | /var/home/mal/.config/litellm.env |
| Push script | /var/home/mal/.local/bin/zeroclaw-push.sh |
| Push log | /var/home/mal/.zeroclaw/push.log |
| Secrets | /var/home/mal/.zeroclaw/secrets/ |
| Active personas | /var/home/mal/.zeroclaw/workspace/personas/ |
| Archived personas | /var/home/mal/.zeroclaw/workspace/personas/archive/ |
