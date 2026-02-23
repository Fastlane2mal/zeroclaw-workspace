# Decisions

A record of the key choices made in this project, and why. Read this before changing anything significant.

---

## Active Decisions

### Use Fedora Silverblue as the OS
**Why**: Immutable OS means the base system is read-only and automatically rolls back if an update breaks something. Predictable and stable.
**Trade-off**: Requires containers for everything — can't just `pip install` things on the host.
**Status**: ✅ Working well

---

### Run all AI services in Podman containers
**Why**: Isolates services from each other and from the OS. Easy to update or remove. No dependency conflicts.
**Status**: ✅ Working well

---

### Use user-level systemd for service management
**Why**: Services managed by the user account (not root). No reboots needed to restart services. Easier to debug.
**Status**: ✅ Working well

---

### Mount HDD using UUID in fstab (not device name)
**Why**: Device names like `/dev/sda` can change on reboot if hardware changes. UUIDs are permanent. A wrong fstab entry can prevent the system from booting.
**Status**: ✅ Critical rule — never change this

---

### EnvironmentFile must be in [Container] section of quadlet files
**Why**: If placed in [Service] section, environment variables only reach the systemd process — they never get passed to the container. This caused 3 sessions of debugging before the root cause was found.
**Status**: ✅ Critical rule — never change this

---

### Ollama must bind to 0.0.0.0 (not 127.0.0.1)
**Why**: If Ollama only listens on localhost, containers running in Podman can't reach it. Binding to 0.0.0.0 allows all local network interfaces.
**Status**: ✅ Required for container access

---

### No database for LiteLLM (stateless only)
**Why**: A Postgres database was added in early sessions for cost tracking. It caused a deadlock in the `update_spend` job that blocked ALL requests indefinitely. Three sessions were lost diagnosing this. Removing the database fixed it immediately.
**Trade-off**: No cost tracking or request logging.
**Rule**: Never add `database_url` to LiteLLM config.
**Status**: ✅ Non-negotiable — learned the hard way

---

### Groq cloud via LiteLLM (not direct)
**Why**: Groq offers fast, free cloud AI (llama-3.3-70b in 1-2 seconds). Route it through LiteLLM so the same API endpoint works for everything.
**Limitation**: Groq free tier is rate limited (12k tokens per minute for llama-3.3-70b). Fine for normal chat, not suitable for agent frameworks.
**Status**: ✅ Working well

---

### Do not use Groq directly with agent frameworks
**Why**: Agent frameworks (like OpenClaw) send 13,000+ tokens per request (system prompts + workspace context + tool definitions + conversation history). Groq free tier allows only 6,000-12,000 tokens per minute. Every single request fails with a 429 rate limit error.
**Status**: ✅ Documented limit — don't attempt this

---

### OpenClaw removed permanently
**Why**: Multiple reasons compounded:
1. Three CVEs discovered (CVSS scores 7.8-8.8): remote code execution, SSH command injection, container sandbox escape
2. 21,000+ publicly exposed instances compromised in January 2026
3. Groq free tier incompatible with its token usage
4. Added complexity without clear enough benefit
**Replaced by**: AnythingLLM for web UI (simpler, no CVEs, proven)
**Status**: ✅ Removed in Session 20

---

### Tailscale VPN for remote access (no public port exposure)
**Why**: Never expose services directly to the internet. Tailscale creates an encrypted VPN tunnel with per-device authentication. No port forwarding required.
**Status**: ✅ Working well

---

### GDM (display manager) disabled
**Why**: The server runs headless (no monitor). GDM was triggering suspend during SSH sessions. Since no graphical login is needed, disabling GDM eliminated the problem and freed ~200-300MB RAM.
**How to re-enable if needed**: `sudo systemctl enable gdm && sudo reboot`
**Status**: ✅ Disabled in Session 21

---

### AnythingLLM as primary web UI
**Why**: Browser-based chat interface with document upload and RAG (question-answering over your own documents). Simpler than OpenClaw, actively developed, no known CVEs.
**Access**: Direct via Tailscale at `http://100.110.112.76:3001` — no SSH tunnel needed.
**Status**: ✅ Running and verified working (Session 22)

---

### Logseq as project knowledge base (source of truth)
**Why**: Logseq stores everything as plain Markdown files on the Samba share, making it easy to version, edit, and feed into AnythingLLM. It provides a structured, linked knowledge base that survives across sessions and users.
**Rule**: Always write in Logseq first. AnythingLLM is a query tool, not a note-taking tool.
**Status**: ✅ Set up in Session 22

---

### Manual document upload to AnythingLLM (not automatic)
**Why**: The hotdir folder watching and Live Document Sync features do not work in the Docker version of AnythingLLM. Live Document Sync is Desktop-only.
**Trade-off**: Requires manual re-upload of changed files via the web UI — acceptable since pages change infrequently (once per session at most).
**Future option**: Install AnythingLLM Desktop on Windows PC to get automatic sync watching the Logseq pages folder directly.
**Status**: ✅ Accepted workflow

---

### STORAGE_DIR environment variable required for AnythingLLM
**Why**: Without it, AnythingLLM cannot find its persistent storage and warns of data loss on restart. Must be set explicitly in the `podman run` command.
**Rule**: Always include `-e STORAGE_DIR=/app/server/storage` when launching the container.
**Status**: ✅ Documented — learned in Session 22

---

## Key Lessons Learned
- Always check official documentation before attempting configuration — don't guess
- Rate limits have multiple dimensions (requests per minute, tokens per minute, per day) — all must be satisfied
- Agent frameworks use far more tokens per request than simple chat — free tiers may not be compatible
- Simple is better than complex — every removed component is one fewer thing that can break
- Minimal configuration reduces the surface area for failures

## Related
- [[Architecture]] — how these decisions shape the system design
- [[Known Issues]] — problems encountered and how they were resolved
- [[Session Log]] — which session each decision was made
