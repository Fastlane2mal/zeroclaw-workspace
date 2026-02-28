# Getting Started

**Purpose**: First-time deployment walkthrough for new users  
**Audience**: Someone with Linux basics but new to this platform  
**Time**: 6-8 hours across multiple sessions  
**Last Updated**: February 2026 (v2026.02)

---

## Overview

This guide walks you through deploying the Silverblue AI Platform from scratch on physical hardware. You'll end up with a headless server running local and cloud AI models accessible via web interface.

**What you'll deploy**:
- Fedora Silverblue (immutable OS)
- Ollama (local LLM inference)
- LiteLLM (API gateway)
- Groq Cloud integration (free tier)
- AnythingLLM (web UI)
- Caddy (HTTPS proxy)
- Tailscale (VPN access)

**Prerequisites**:
- Physical machine ready to dedicate
- USB drive for OS installation
- Windows PC for SSH access (macOS/Linux similar)
- Basic Linux terminal skills
- Patience - this is a learning deployment!

---

## Before You Start

### What You Need

**Hardware** (minimum):
- [ ] CPU: Intel i5-8250U or equivalent (4C/8T)
- [ ] RAM: 8GB (11GB+ recommended)
- [ ] Storage: 256GB SSD + 500GB HDD
- [ ] Network: Wired ethernet connection
- [ ] USB drive (8GB+) for Fedora Silverblue installer

**Software**:
- [ ] Fedora Silverblue 40 ISO downloaded
- [ ] USB creation tool (Rufus on Windows, dd on Linux)
- [ ] SSH client (built into Windows 10+, macOS, Linux)

**Accounts** (free):
- [ ] Anthropic API key (https://console.anthropic.com) - Optional, for Claude
- [ ] Tailscale account (https://tailscale.com) - For remote access

**Knowledge**:
- [ ] Can use terminal/command line
- [ ] Comfortable with SSH
- [ ] Understand basic Linux file permissions
- [ ] Can edit text files (nano/vi)

### Time Commitment

**Initial Deployment**: 6-8 hours (can pause between phases)
- Phase 0: Hardware detection (30 min)
- Phase 1: Base OS install (1 hour)
- Phase 2: Storage setup (30 min)
- Phase 3: Ollama + models (1-2 hours)
- Phase 4: LiteLLM (30 min)
- Phase 5: AnythingLLM (1 hour)
- Phase 6-7: HTTPS + VPN (1 hour)
- Phase 8: Verification (30 min)

**Checkpoints**: Each phase has a checkpoint - safe to pause and resume.

### Important Safety Rules

⚠️ **Read these carefully**:

1. **Never paste actual credentials in Claude conversations**
2. **Always verify UUIDs before editing fstab** (wrong UUID = system won't boot)
3. **Complete each phase's checkpoint before starting next phase**
4. **This is a LEARNING/LAB deployment** - don't use with sensitive data
5. **Never expose services directly to internet** - use Tailscale VPN

### What This Guide Covers

✅ **Included**:
- Complete step-by-step deployment
- Common issues and solutions (inline)
- Verification at each step
- How to access your AI platform

❌ **Not Covered**:
- Windows/macOS deployment (Linux only)
- GPU acceleration (CPU-only deployment)
- Advanced networking (WiFi, static IPs)
- Multi-user setups
- Production hardening

For full deployment details, see [DEPLOYMENT.md](DEPLOYMENT.md).

---

## Quick Start Checklist

Use this checklist to track your progress:

### Phase 0: Hardware Pre-flight
- [ ] Boot from Silverblue USB
- [ ] Document CPU, RAM, storage in terminal
- [ ] Identify which drive is SSD vs HDD
- [ ] Note network interface name

### Phase 1: Base Silverblue
- [ ] Install Silverblue to SSD
- [ ] Create user account
- [ ] Set up SSH key access from Windows
- [ ] Test SSH connection works
- [ ] Update OS and reboot
- [ ] Layer required packages (tailscale, samba)

### Phase 2: Storage + Samba
- [ ] Format HDD (if needed)
- [ ] Add HDD to /etc/fstab with UUID
- [ ] Create directory structure on HDD
- [ ] Configure Samba share
- [ ] Fix SELinux contexts for Samba
- [ ] Test Windows can access share

### Phase 3: Ollama + Models
- [ ] Create config file with credentials
- [ ] Install Ollama
- [ ] Create systemd service for Ollama
- [ ] Download CPU-optimized models (smollm2, qwen2.5)
- [ ] Test model inference
- [ ] Remove slow models

### Phase 4: LiteLLM
- [ ] Create LiteLLM config (local + cloud models)
- [ ] Create Podman quadlet service
- [ ] Start LiteLLM container
- [ ] Test routing to local models
- [ ] Test routing to Groq (optional)
- [ ] Test routing to Claude (optional, costs money)

### Phase 5: AnythingLLM
- [ ] Pull AnythingLLM container image
- [ ] Create persistent storage directory
- [ ] Start AnythingLLM container
- [ ] Access web UI via SSH tunnel
- [ ] Create workspace and connect to LiteLLM
- [ ] Send test message

### Phase 6: Caddy HTTPS
- [ ] Start Caddy reverse proxy container
- [ ] Test HTTPS access to AnythingLLM
- [ ] Enable auto-restart on boot

### Phase 7: Tailscale VPN
- [ ] Create Tailscale auth key
- [ ] Add to server config file
- [ ] Start Tailscale on server
- [ ] Install Tailscale on Windows
- [ ] Test SSH via Tailscale hostname
- [ ] Test Samba via Tailscale

### Phase 8: Final Verification
- [ ] Reboot server
- [ ] Verify all services auto-start
- [ ] Access AnythingLLM web UI
- [ ] Send test messages with different models
- [ ] Document your deployment

---

## The Deployment Process

### Step 1: Create Bootable USB

**On Windows**:
1. Download Fedora Silverblue 40 ISO from https://fedoraproject.org/silverblue/
2. Download Rufus from https://rufus.ie/
3. Insert USB drive (will be erased!)
4. Run Rufus:
   - Device: Your USB drive
   - Boot selection: Downloaded Silverblue ISO
   - Partition scheme: GPT
   - Target system: UEFI
5. Click START and wait for completion

### Step 2: Boot From USB

1. Insert USB into target machine
2. Power on and enter BIOS/UEFI (usually F2, F12, or DEL key)
3. Change boot order to boot from USB first
4. Save and exit
5. Machine should boot into Fedora Silverblue live environment

### Step 3: Run Phase 0 (Hardware Pre-flight)

**From live environment terminal**:

```bash
# Check CPU
echo "=== CPU ===" && lscpu | grep -E "Model name|CPU\(s\)"

# Check RAM
echo "=== RAM ===" && free -h

# Check storage (CRITICAL - identify SSD vs HDD)
echo "=== STORAGE ===" && lsblk -o NAME,SIZE,TYPE,ROTA,MODEL

# Check network
echo "=== NETWORK ===" && ip link show | grep -E "^[0-9]"
```

**Document this output** - you'll need it to identify:
- Which device is SSD (ROTA=0) - for OS installation
- Which device is HDD (ROTA=1) - for data storage
- Network interface name (usually `eno1` or `wlo1`)

**STOP HERE** - Do not proceed until you've confirmed which drive is which!

### Step 4: Install Silverblue

1. In live environment, click "Install to Hard Drive"
2. **Language/Keyboard**: Select your preferences
3. **Installation Destination**: 
   - Select ONLY the SSD (from Phase 0)
   - Storage Configuration: Automatic
   - Click Done
4. **Network & Hostname**:
   - Enable your ethernet interface
   - Set hostname (e.g., `silverblue-ai`)
   - Click Done
5. **User Creation**:
   - Create user (e.g., `mal`)
   - Set password (you'll disable password SSH later)
   - Make user administrator
6. Click "Begin Installation"
7. Wait for completion (15-20 minutes)
8. Click "Reboot System"
9. Remove USB drive

### Step 5: First Boot & SSH Setup

**On the server** (at console):
1. Boot into installed Silverblue
2. Login with your user account
3. Open terminal
4. Check SSH is running: `systemctl status sshd`
5. If not running: `sudo systemctl enable --now sshd`
6. Get IP address: `ip addr show | grep "inet " | grep -v 127.0.0.1`
7. Note the IP (e.g., `192.168.0.33`)

**On Windows** (PowerShell):
```powershell
# Test SSH with password (first time only)
ssh mal@192.168.0.33

# If successful, exit
exit

# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "silverblue-ai-key"
# Press Enter for default location
# Press Enter twice for no passphrase

# View your public key
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub

# Copy this entire output (starts with ssh-ed25519)
```

**Back on server** (at console):
```bash
# Create .ssh directory
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Add your public key
nano ~/.ssh/authorized_keys
# Paste the key you copied from Windows
# Save: Ctrl+X, Y, Enter

# Set permissions
chmod 600 ~/.ssh/authorized_keys

# Exit server
exit
```

**Test from Windows** (should work without password now):
```powershell
ssh mal@192.168.0.33
```

**Success!** You now have SSH access. All remaining steps done via SSH.

### Step 6: Continue with Full Deployment

At this point, you have:
- ✅ Silverblue installed on SSD
- ✅ SSH access from Windows
- ✅ User account created
- ✅ Hardware profile documented

**Next steps**: Follow [DEPLOYMENT.md](DEPLOYMENT.md) starting from Phase 1 (Section 3.4):
- Phase 1: System updates and package layering
- Phase 2: Storage + Samba
- Phase 3: Ollama + Models
- Phase 4: LiteLLM
- Phase 5: AnythingLLM
- Phase 6: Caddy HTTPS
- Phase 7: Tailscale VPN
- Phase 8: Final verification

---

## First Access to Your AI Platform

After completing all deployment phases, here's how to access your AI:

### Via SSH Tunnel (Before Tailscale)

**From Windows PowerShell**:
```powershell
# Create SSH tunnel to AnythingLLM
ssh -L 3001:localhost:3001 mal@192.168.0.33

# Keep this terminal open
```

**In your browser**:
1. Navigate to: `http://localhost:3001`
2. Complete AnythingLLM first-time setup
3. Create workspace
4. Configure LiteLLM connection:
   - Base URL: `http://localhost:4000/v1`
   - API Key: Your `LITELLM_MASTER_KEY` from `~/.silverblue-ai-config`
5. Select model (try `smollm2` first - it's fast and free)
6. Start chatting!

### Via Tailscale (After Phase 7)

**From anywhere**:
```powershell
# SSH via Tailscale
ssh -L 3001:localhost:3001 mal@silverblue-ai.your-tailnet.ts.net

# Then browse to http://localhost:3001
```

---

## Common First-Time Issues

### "SSH connection refused"
**Problem**: Can't connect via SSH  
**Solution**:
```bash
# On server (at console)
sudo systemctl status sshd
sudo systemctl enable --now sshd
```

### "Permission denied (publickey)"
**Problem**: SSH key not working  
**Solution**:
```bash
# On server, check permissions
ls -la ~/.ssh/
# Should show:
# drwx------ (700) for .ssh/
# -rw------- (600) for authorized_keys

# Fix if wrong
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

### "Wrong UUID = system won't boot"
**Problem**: Edited /etc/fstab with wrong UUID  
**Solution**: Always verify UUID before adding to fstab:
```bash
# Get correct UUID
sudo blkid /dev/sdX1

# Compare with your fstab entry
cat /etc/fstab
```

### "Ollama taking 10+ minutes to respond"
**Problem**: Model too large for CPU  
**Solution**: Use smaller models:
```bash
# Remove slow models
ollama rm llama3.2  # If you have it

# Use fast models only
ollama pull smollm2
ollama pull qwen2.5:1.5b
```

### "LiteLLM can't reach Claude API"
**Problem**: Environment variables not loading in container  
**Solution**: Verify EnvironmentFile in [Container] section:
```bash
# Check quadlet file
cat ~/.config/containers/systemd/litellm.container
# Should show EnvironmentFile=%h/.config/litellm.env in [Container] section

# Verify env vars reached container
podman exec litellm printenv | grep ANTHROPIC_API_KEY
# Should show your actual key
```

For more issues, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

---

## Next Steps

After successful deployment:

1. **Learn the system** - Read [ARCHITECTURE.md](ARCHITECTURE.md)
2. **Daily operations** - See [OPERATIONS.md](OPERATIONS.md)
3. **Quick reference** - Bookmark [REFERENCE.md](REFERENCE.md)
4. **Try different models** - Experiment with local and cloud options
5. **Upload documents** - Test AnythingLLM's RAG capabilities
6. **Monitor resources** - Check `podman stats`, `htop`

---

## Getting Help

**If you're stuck**:
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) first
2. Review [DEPLOYMENT.md](DEPLOYMENT.md) for detailed steps
3. Verify you completed all checkpoints
4. Check service status: `systemctl --user status ollama litellm`
5. Check container logs: `podman logs anythingllm --tail 50`

**Remember**: This is a learning deployment. Mistakes are expected and fixable!

---

**Related Documentation**:
- [README.md](README.md) - Project overview
- [DEPLOYMENT.md](DEPLOYMENT.md) - Complete deployment guide
- [OPERATIONS.md](OPERATIONS.md) - Daily management
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Known issues

**Status**: v2026.02 - Stable deployment path  
**Last Updated**: February 2026
