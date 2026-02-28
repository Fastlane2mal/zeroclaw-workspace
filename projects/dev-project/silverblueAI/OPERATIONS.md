# Operations

**Purpose**: Daily management and common operational tasks  
**Audience**: Operators managing the running system  
**Last Updated**: February 2026 (v2026.02)

---

## Table of Contents

- [Starting and Stopping Services](#starting-and-stopping-services)
- [Health Checks](#health-checks)
- [Viewing Logs](#viewing-logs)
- [Model Management](#model-management)
- [Workspace Management](#workspace-management)
- [Backup and Restore](#backup-and-restore)
- [System Updates](#system-updates)
- [Resource Monitoring](#resource-monitoring)
- [Common Tasks](#common-tasks)
- [Routine Maintenance](#routine-maintenance)

---

## Quick Reference

| Task | Command |
|------|---------|
| Check all services | `systemctl --user status ollama litellm && podman ps` |
| View Ollama logs | `journalctl --user -u ollama -f` |
| View LiteLLM logs | `podman logs litellm -f` |
| Restart LiteLLM | `systemctl --user restart litellm` |
| List models | `ollama list` |
| Check disk space | `df -h /mnt/hdd` |
| Check RAM usage | `free -h` |
| Access web UI | `ssh -L 3001:localhost:3001 mal@silverblue-ai` |

---

## Starting and Stopping Services

### Ollama (Local LLM Engine)

**Start**:
```bash
systemctl --user start ollama
```

**Stop**:
```bash
systemctl --user stop ollama
```

**Restart**:
```bash
systemctl --user restart ollama
```

**Status**:
```bash
systemctl --user status ollama
```

**Enable auto-start on boot**:
```bash
systemctl --user enable ollama
```

**Disable auto-start**:
```bash
systemctl --user disable ollama
```

### LiteLLM (API Gateway)

**Start**:
```bash
systemctl --user start litellm
```

**Stop**:
```bash
systemctl --user stop litellm
```

**Restart** (after config changes):
```bash
systemctl --user restart litellm
```

**Status**:
```bash
systemctl --user status litellm
```

**Rebuild container** (after image update):
```bash
systemctl --user stop litellm
podman pull ghcr.io/berriai/litellm:main-stable
systemctl --user start litellm
```

### AnythingLLM (Web UI)

**Start**:
```bash
podman start anythingllm
```

**Stop**:
```bash
podman stop anythingllm
```

**Restart**:
```bash
podman restart anythingllm
```

**Full restart** (recreate container):
```bash
podman stop anythingllm
podman rm anythingllm
podman run -d \
  --name anythingllm \
  --network host \
  -v /mnt/hdd/projects/anythingllm-storage:/app/server/storage:Z \
  --cap-add SYS_ADMIN \
  ghcr.io/mintplex-labs/anythingllm:master
```

### Caddy (HTTPS Proxy)

**Start**:
```bash
podman start caddy-https
```

**Stop**:
```bash
podman stop caddy-https
```

**Restart**:
```bash
podman restart caddy-https
```

### System Services (SSH, Samba, Tailscale)

**Samba**:
```bash
sudo systemctl restart smb nmb
systemctl status smb nmb
```

**SSH**:
```bash
sudo systemctl restart sshd
systemctl status sshd
```

**Tailscale**:
```bash
sudo systemctl restart tailscaled
systemctl status tailscaled
sudo tailscale status
```

---

## Health Checks

### Quick System Health Check

```bash
# Check all critical services
echo "=== User Services ==="
systemctl --user status ollama litellm

echo "=== Containers ==="
podman ps

echo "=== System Services ==="
systemctl status sshd smb nmb tailscaled

echo "=== Disk Space ==="
df -h | grep -E "Filesystem|/mnt/hdd|/dev/sdb"

echo "=== Memory ==="
free -h
```

Save as `~/health-check.sh` and run: `bash ~/health-check.sh`

### Individual Service Health

**Ollama**:
```bash
# Check service
systemctl --user status ollama

# Test API
curl http://localhost:11434/api/tags
```

**LiteLLM**:
```bash
# Check service
systemctl --user status litellm

# Test API (needs auth)
source ~/.silverblue-ai-config
curl http://localhost:4000/health \
  -H "Authorization: Bearer ${LITELLM_MASTER_KEY}"

# List models
curl http://localhost:4000/v1/models \
  -H "Authorization: Bearer ${LITELLM_MASTER_KEY}"
```

**AnythingLLM**:
```bash
# Check container running
podman ps | grep anythingllm

# Check port listening
sudo ss -tlnp | grep 3001

# Access via browser (with SSH tunnel)
ssh -L 3001:localhost:3001 mal@silverblue-ai
# Then: http://localhost:3001
```

**Tailscale**:
```bash
# Check connection
sudo tailscale status

# Check IP
sudo tailscale ip -4

# Test connectivity
sudo tailscale ping silverblue-ai
```

### Storage Health

```bash
# Check HDD mounted
mount | grep /mnt/hdd

# Check disk usage
df -h /mnt/hdd

# Check directory sizes
du -sh /mnt/hdd/*

# Check model storage
du -sh /mnt/hdd/llms/

# Check available space
df -h /mnt/hdd | awk 'NR==2 {print "Used: "$3" / Available: "$4" ("$5")"}'
```

---

## Viewing Logs

### Real-Time Log Monitoring

**Ollama**:
```bash
journalctl --user -u ollama -f
```

**LiteLLM**:
```bash
podman logs litellm -f
```

**AnythingLLM**:
```bash
podman logs anythingllm -f
```

**System logs**:
```bash
journalctl -f
```

### Historical Logs

**Ollama** (last 100 lines):
```bash
journalctl --user -u ollama -n 100
```

**LiteLLM** (last 50 lines):
```bash
podman logs litellm --tail 50
```

**Specific time range**:
```bash
journalctl --user -u ollama --since "1 hour ago"
journalctl --user -u ollama --since "2024-02-15 10:00" --until "2024-02-15 11:00"
```

### Search Logs

**Search for errors**:
```bash
journalctl --user -u ollama | grep -i error
podman logs litellm | grep -i error
```

**Search for specific text**:
```bash
journalctl --user -u ollama | grep "model"
```

### Log Cleanup

**Reduce log size** (keep last 7 days):
```bash
journalctl --vacuum-time=7d
```

**Reduce log size** (keep max 500M):
```bash
journalctl --vacuum-size=500M
```

---

## Model Management

### List Installed Models

```bash
ollama list
```

Example output:
```
NAME              ID            SIZE    MODIFIED
smollm2:latest    abc123...     1.0GB   2 days ago
qwen2.5:1.5b      def456...     900MB   3 days ago
```

### Add a New Model

```bash
# Pull model
ollama pull <model-name>

# Examples
ollama pull smollm2
ollama pull qwen2.5:1.5b
ollama pull gemma3:1b
```

**Check available models**: https://ollama.com/library

### Remove a Model

```bash
ollama rm <model-name>

# Example
ollama rm llama3.2
```

**When to remove**:
- Model too slow (>60s response time)
- Not using it anymore
- Need disk space

### Test a Model

**Interactive test**:
```bash
ollama run smollm2
# Type messages, Ctrl+D to exit
```

**Single query**:
```bash
ollama run smollm2 "What is 2+2?"
```

**API test** (JSON response):
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "smollm2",
  "prompt": "Write a Python hello world",
  "stream": false
}' | jq -r '.response'
```

### Check Model Performance

```bash
# Time a query
time ollama run smollm2 "Count from 1 to 10"

# Expected:
# - smollm2: 10-15 seconds
# - qwen2.5:1.5b: 20-30 seconds
# - Anything >60s: Too slow, consider removing
```

### Update LiteLLM Model Config

After adding/removing models in Ollama:

1. Edit LiteLLM config:
```bash
nano ~/.litellm/config.yaml
```

2. Add model to `model_list`:
```yaml
- model_name: new-model
  litellm_params:
    model: ollama/new-model
    api_base: http://localhost:11434
```

3. Restart LiteLLM:
```bash
systemctl --user restart litellm
```

4. Verify in AnythingLLM (model dropdown)

---

## Workspace Management

### Access AnythingLLM Web UI

**From Windows** (via SSH tunnel):
```powershell
# Create tunnel
ssh -L 3001:localhost:3001 mal@silverblue-ai

# Keep terminal open, browse to:
# http://localhost:3001
```

**From Linux/Mac**:
```bash
ssh -L 3001:localhost:3001 mal@silverblue-ai
# Browse to: http://localhost:3001
```

### Create a New Workspace

1. Click "New Workspace" in AnythingLLM
2. Name it (e.g., "Coding Assistant", "Document Q&A")
3. Configure LLM:
   - Provider: Generic OpenAI
   - Base URL: `http://localhost:4000/v1`
   - API Key: Your LITELLM_MASTER_KEY
   - Model: Choose from dropdown (e.g., smollm2)
4. Save

### Upload Documents to Workspace

1. Open workspace
2. Click "Upload Document"
3. Select PDF, TXT, DOCX, or other supported files
4. Wait for embedding (may take a few minutes)
5. Ask questions about the document

### Switch Models in Workspace

1. Open workspace settings (gear icon)
2. Change "Chat Model"
3. Choose from:
   - **smollm2** (fast, general - 10-15s)
   - **qwen2.5-1.5b** (coding - 20-30s)
   - **llama-3.3-70b** (Groq cloud - 1-2s, free)
   - **claude-haiku-4** (Claude - 1-3s, paid)
4. Save

### Export/Backup Workspace

```bash
# Workspace data stored here
ls -lh /mnt/hdd/projects/anythingllm-storage/

# Backup workspace
tar czf ~/anythingllm-backup-$(date +%Y%m%d).tar.gz \
  /mnt/hdd/projects/anythingllm-storage/

# Copy to Windows (via Samba share)
cp ~/anythingllm-backup-*.tar.gz /mnt/hdd/share/
```

### Restore Workspace

```bash
# Stop AnythingLLM
podman stop anythingllm

# Restore from backup
tar xzf ~/anythingllm-backup-20260215.tar.gz -C /

# Start AnythingLLM
podman start anythingllm
```

---

## Backup and Restore

### Manual Backup

**Backup configuration**:
```bash
mkdir -p ~/backups/$(date +%Y%m%d)
cd ~/backups/$(date +%Y%m%d)

# Core config
cp ~/.silverblue-ai-config config.txt
cp ~/.litellm/config.yaml litellm-config.yaml
cp ~/.config/litellm.env litellm.env

# Service files
cp -r ~/.config/systemd/user/ systemd-user-services/
cp -r ~/.config/containers/systemd/ containers-systemd/

# Document system state
rpm-ostree status > ostree-status.txt
podman images > container-images.txt
ollama list > ollama-models.txt
systemctl --user list-units > user-services.txt
```

**Backup data** (excluding models):
```bash
cd ~/backups/$(date +%Y%m%d)
tar czf anythingllm-data.tar.gz /mnt/hdd/projects/anythingllm-storage/
```

**Backup to Windows** (via Samba):
```bash
cp -r ~/backups/$(date +%Y%m%d) /mnt/hdd/share/backups/
```

### Automated Backup (Future Enhancement)

Create `~/backup.sh`:
```bash
#!/bin/bash
BACKUP_DIR=~/backups/$(date +%Y%m%d)
mkdir -p $BACKUP_DIR

# Backup configs
cp ~/.silverblue-ai-config $BACKUP_DIR/
cp ~/.litellm/config.yaml $BACKUP_DIR/
cp -r ~/.config/systemd/user/ $BACKUP_DIR/systemd/

# Backup data
tar czf $BACKUP_DIR/anythingllm.tar.gz /mnt/hdd/projects/anythingllm-storage/

# Copy to share
cp -r $BACKUP_DIR /mnt/hdd/share/backups/

echo "Backup completed: $BACKUP_DIR"
```

Run daily via systemd timer (to be implemented).

### Restore from Backup

```bash
# Stop services
systemctl --user stop ollama litellm
podman stop anythingllm

# Restore configs
cd ~/backups/20260215/
cp config.txt ~/.silverblue-ai-config
cp litellm-config.yaml ~/.litellm/config.yaml

# Restore service files if needed
cp -r systemd-user-services/* ~/.config/systemd/user/

# Restore data
tar xzf anythingllm-data.tar.gz -C /

# Reload and restart
systemctl --user daemon-reload
systemctl --user start ollama litellm
podman start anythingllm
```

---

## System Updates

### OS Updates

**Check for updates**:
```bash
rpm-ostree upgrade --check
```

**Apply updates**:
```bash
rpm-ostree upgrade
```

**Reboot to apply**:
```bash
sudo systemctl reboot
```

**Verify after reboot**:
```bash
rpm-ostree status
```

**Rollback if issues**:
```bash
rpm-ostree rollback
sudo systemctl reboot
```

### Container Updates

**LiteLLM**:
```bash
# Stop service
systemctl --user stop litellm

# Pull new image
podman pull ghcr.io/berriai/litellm:main-stable

# Start service (uses new image)
systemctl --user start litellm

# Verify
podman images | grep litellm
```

**AnythingLLM**:
```bash
# Stop and remove
podman stop anythingllm
podman rm anythingllm

# Pull new image
podman pull ghcr.io/mintplex-labs/anythingllm:master

# Recreate container (data persists in /mnt/hdd)
podman run -d \
  --name anythingllm \
  --network host \
  -v /mnt/hdd/projects/anythingllm-storage:/app/server/storage:Z \
  --cap-add SYS_ADMIN \
  ghcr.io/mintplex-labs/anythingllm:master
```

### Ollama Updates

```bash
# Download and run installer
curl -fsSL https://ollama.com/install.sh | sh

# Restart service
systemctl --user restart ollama

# Verify version
ollama --version
```

### Package Updates (Layered Packages)

**Update tailscale or samba**:
```bash
# Check current version
rpm-ostree status

# Upgrade (includes layered packages)
rpm-ostree upgrade

# Reboot
sudo systemctl reboot
```

---

## Resource Monitoring

### CPU Usage

```bash
# Real-time
htop

# Or simpler
top

# Current load
uptime
```

### RAM Usage

```bash
# Overview
free -h

# Per-process
ps aux --sort=-%mem | head -20

# Container usage
podman stats
```

### Disk Usage

```bash
# Overview
df -h

# Detailed by directory
du -sh /mnt/hdd/*

# Find large files
du -ah /mnt/hdd | sort -rh | head -20

# Model storage
du -sh /mnt/hdd/llms/
```

### Network Usage

```bash
# Active connections
sudo ss -tunapl

# Port usage
sudo ss -tlnp

# Tailscale status
sudo tailscale status
```

### Service Resource Usage

```bash
# Systemd service resources
systemctl --user show ollama | grep -E "CPU|Memory"

# Container resources
podman stats --no-stream

# Real-time container stats
podman stats
```

---

## Common Tasks

### Change LiteLLM API Key

1. Edit config:
```bash
nano ~/.silverblue-ai-config
# Update LITELLM_MASTER_KEY
```

2. Regenerate env file:
```bash
sed 's/^export //; s/"//g' ~/.silverblue-ai-config > ~/.config/litellm.env
```

3. Restart LiteLLM:
```bash
systemctl --user restart litellm
```

4. Update AnythingLLM workspaces with new key

### Add Groq API Key

1. Get key from: https://console.groq.com

2. Add to config:
```bash
nano ~/.silverblue-ai-config
# Add: export GROQ_API_KEY="gsk_..."
```

3. Update env file:
```bash
sed 's/^export //; s/"//g' ~/.silverblue-ai-config > ~/.config/litellm.env
```

4. Add models to LiteLLM config:
```bash
nano ~/.litellm/config.yaml
```

5. Restart LiteLLM:
```bash
systemctl --user restart litellm
```

### Change Samba Password

```bash
smbpasswd -a $USER
# Enter new password when prompted
```

### Regenerate SSH Keys

**On Windows** (if needed):
```powershell
# Backup old keys
mv $env:USERPROFILE\.ssh\id_ed25519 $env:USERPROFILE\.ssh\id_ed25519.old
mv $env:USERPROFILE\.ssh\id_ed25519.pub $env:USERPROFILE\.ssh\id_ed25519.pub.old

# Generate new
ssh-keygen -t ed25519 -C "new-key"

# Copy new public key
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub
```

**On server**:
```bash
# Edit authorized_keys
nano ~/.ssh/authorized_keys
# Replace old key with new public key
# Save and exit

# Verify permissions
chmod 600 ~/.ssh/authorized_keys
```

### Free Up Disk Space

```bash
# Remove unused models
ollama list
ollama rm <unused-model>

# Remove old containers
podman image prune -a

# Clean logs
journalctl --vacuum-time=7d

# Remove old backups
rm -rf ~/backups/old-date/
```

### Test Model Performance

```bash
# Create test script
cat > ~/test-model.sh << 'EOF'
#!/bin/bash
MODEL=$1
echo "Testing $MODEL..."
time curl -s http://localhost:11434/api/generate -d "{
  \"model\": \"$MODEL\",
  \"prompt\": \"Write a Python function to reverse a string\",
  \"stream\": false
}" | jq -r '.response' | head -20
EOF

chmod +x ~/test-model.sh

# Test models
~/test-model.sh smollm2
~/test-model.sh qwen2.5:1.5b
```

---

## Routine Maintenance

### Daily (Automated via Monitoring)

- [ ] Check service status (all services running)
- [ ] Check disk space (>20% free)
- [ ] Check RAM usage (<90% used)
- [ ] Check logs for errors

### Weekly (Manual)

- [ ] Review logs for errors or warnings
- [ ] Check for OS updates: `rpm-ostree upgrade --check`
- [ ] Check for container updates
- [ ] Verify backups (if automated)
- [ ] Test SSH access via Tailscale
- [ ] Test Samba share access

### Monthly (Manual)

- [ ] Apply OS updates and reboot
- [ ] Update containers (LiteLLM, AnythingLLM)
- [ ] Review and clean old models
- [ ] Review disk usage, clean up if needed
- [ ] Test model performance
- [ ] Review and update documentation
- [ ] Rotate credentials (if needed)

### Quarterly (Manual)

- [ ] Full system backup
- [ ] Test restore procedure
- [ ] Review security advisories
- [ ] Update Ollama
- [ ] Review and optimize configs
- [ ] Plan for hardware upgrades if needed

---

## Emergency Procedures

### System Won't Boot

1. Boot from Silverblue USB
2. Mount SSD: `sudo mount /dev/sdb3 /mnt`
3. Check fstab: `cat /mnt/etc/fstab`
4. Fix or comment out bad entry
5. Unmount and reboot

### Services Won't Start After Reboot

```bash
# Check systemd status
systemctl --user status ollama litellm

# Check for errors
journalctl --user -xe

# Reload if needed
systemctl --user daemon-reload

# Start manually
systemctl --user start ollama
systemctl --user start litellm
```

### Out of Disk Space

```bash
# Check what's using space
df -h
du -sh /* 2>/dev/null | sort -rh | head -10

# Quick cleanup
ollama list  # Remove unused models
podman image prune -a  # Remove old images
journalctl --vacuum-time=3d  # Reduce logs
```

### Can't Access via SSH

```bash
# From console (keyboard/monitor)
systemctl status sshd
sudo systemctl restart sshd

# Check Tailscale
sudo tailscale status
sudo tailscale up

# Check firewall
sudo firewall-cmd --list-services
```

---

**Related Documentation**:
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Problem diagnosis and fixes
- [REFERENCE.md](REFERENCE.md) - Command reference
- [ARCHITECTURE.md](ARCHITECTURE.md) - How components work
- [DEPLOYMENT.md](DEPLOYMENT.md) - Initial setup procedures

**Status**: Current operations guide for v2026.02  
**Last Updated**: February 2026  
**Maintained**: Updated with operational experience
