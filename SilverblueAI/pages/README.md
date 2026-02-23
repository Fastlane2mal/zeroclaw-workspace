# Silverblue AI Platform — Logseq Pages

## What's in This Folder

These are ready-to-use Logseq pages for the Silverblue AI Platform project. Copy them into your Logseq graph's `pages` folder to import everything at once.

## Files Included

| File | What It Contains |
|---|---|
| `Silverblue AI Platform.md` | Hub page — start here, links to everything |
| `Hardware.md` | Server specs, storage layout, performance expectations |
| `Architecture.md` | How the system is designed, 4-layer stack, data flow |
| `Services.md` | Every running service: what it does, ports, start/stop commands |
| `Commands Reference.md` | All useful commands organised by task |
| `Decisions.md` | Key choices made and why — read before changing anything |
| `Known Issues.md` | Active issues and resolved issues for reference |
| `Session Log.md` | Full history of all 21 sessions + template for future sessions |

## How to Import Into Logseq

1. Open Logseq on your Windows 11 PC
2. Open your Silverblue AI Platform graph (or create one)
3. Find the graph's folder on disk — usually shown in Settings → Graph
4. Copy all these `.md` files into the `pages` subfolder inside that graph folder
5. Switch back to Logseq — the pages will appear automatically
6. Open "Silverblue AI Platform" as your starting page

## How AnythingLLM Reads Your Pages

Your Logseq graph is saved to `F:\Projects\SilverblueAI\` on the Samba share. AnythingLLM does **not** automatically sync from this folder in Docker mode — documents must be uploaded manually via the web UI.

**First-time setup in AnythingLLM:**
1. Open `http://100.110.112.76:3001` in your browser (direct via Tailscale — no SSH tunnel needed)
2. Create a workspace called "Silverblue AI Platform"
3. Click the document icon → Upload files
4. Upload all the `.md` files from your Logseq pages folder
5. Assign them to the workspace
6. Test with a question like "What services are running on the server?"

## Keeping Things in Sync

When you update a Logseq page:
1. Open AnythingLLM at `http://100.110.112.76:3001`
2. Go to your workspace → document icon
3. Re-upload the changed file(s)
4. AnythingLLM re-processes and updates the workspace

This is a manual step, but only needed for files you actually changed — usually one or two per session.

## Adding a New Project

For each new project:
1. Create a new Logseq graph saved to a folder on F:\
2. In AnythingLLM, create a new workspace
3. Upload the project's Logseq pages via the web UI
4. Assign them to the new workspace

## Future Improvement — Automatic Sync

AnythingLLM's **Live Document Sync** feature would automate this entirely, but it is only available in the Desktop app (not Docker). Installing AnythingLLM Desktop on your Windows 11 PC — pointing it at your Logseq pages folder and connecting it to your LiteLLM server — would give you fully automatic sync with no manual uploads needed.

## The Workflow

```
Edit a page in Logseq (Windows PC)
        ↓
Logseq saves to F:\Projects\SilverblueAI\pages\
        ↓
Manually re-upload changed files to AnythingLLM
        ↓
Ask AnythingLLM questions about your project
        ↓
Get answers backed by your own up-to-date documentation
```
