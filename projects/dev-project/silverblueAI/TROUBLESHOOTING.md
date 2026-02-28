# Troubleshooting

**Purpose**: Known issues and solutions for common problems  
**Audience**: Operators diagnosing and fixing issues  
**Last Updated**: February 2026 (v2026.02)

---

## Table of Contents

- [Active Issues](#active-issues)
- [Common Deployment Problems](#common-deployment-problems)
- [Service-Specific Issues](#service-specific-issues)
- [Network and Firewall Issues](#network-and-firewall-issues)
- [Performance Issues](#performance-issues)
- [Recently Resolved Issues](#recently-resolved-issues)

---

## How to Use This Guide

**Format**: Symptom → Diagnosis → Resolution

**Quick diagnostic steps**:
1. Check service status: `systemctl --user status <service>`
2. Check logs: `journalctl --user -u <service> -f`
3. Check this guide for matching symptoms
4. Apply resolution steps
5. Verify fix worked

**If not found here**:
- Check [REFERENCE.md](REFERENCE.md) for commands
- Review [OPERATIONS.md](OPERATIONS.md) for procedures
- Consult [DECISIONS.md](DECISIONS.md) for design rationale

---

## Active Issues

### âš ï¸ Groq Free Tier Incompatible with Agent Frameworks

**Status**: Active - No free workaround  
**Impact**: Cannot use Groq direct API with OpenClaw or similar agent frameworks  
**Discovered**: Session 19 (2026-02-14)

**Symptoms**:
- OpenClaw shows 429 rate limit errors immediately
- Error message mentions "Request too large" for TPM limits
- Agent restarts automatically after each message
- Works fine with LiteLLM but not direct Groq

**Root Cause**:
Agent frameworks send large context per request (13k+ tokens):
- System prompts and configuration
- Workspace state and file context
- Tool definitions (browser, code execution)
- Conversation history (5+ messages)
- User message

Groq free tier limits:
- llama-3.1-8b: 6,000 TPM (too low)
- llama-3.3-70b: 12,000 TPM (barely too low)
- mixtral-8x7b: 5,000 TPM (too low)

**Why `maxTokens` doesn't help**: Only controls response size, not input size.

**Resolution**:
Use LiteLLM proxy instead of direct Groq API:
```yaml
# In OpenClaw or agent config
"providers": {
  "litellm": {
    "baseUrl": "http://localhost:4000/v1",
    "apiKey": "${LITELLM_MASTER_KEY}",
    "models": [
      {"id": "smollm2", ...},         # Local, FREE, no limits
      {"id": "llama-3.3-70b", ...}    # Groq via LiteLLM
    ]
  }
}
```

**Alternatives**:
1. Pay for Groq developer tier (higher limits)
2. Use different provider (OpenAI, Claude, Together.ai)
3. Use local models only (completely free)

**Prevention**: Check API rate limits against expected usage before integration.

**Related**: See [DECISIONS.md](DECISIONS.md) - "Direct Groq Provider for OpenClaw - REJECTED"

---

## Common Deployment Problems

### SSH Connection Refused

**Symptoms**:
- `ssh: connect to host 192.168.0.33 port 22: Connection refused`
- Cannot access server remotely

**Diagnosis**:
```bash
# On server (at console)
systemctl status sshd
```

**Resolution**:
```bash
# Start and enable SSH
sudo systemctl enable --now sshd

# Verify listening
sudo ss -tlnp | grep :22

# Check firewall allows SSH
sudo firewall-cmd --list-services | grep ssh
```

**Prevention**: SSH should auto-start on Silverblue by default.

---

### SSH "Permission denied (publickey)"

**Symptoms**:
- SSH asks for password but rejects it
- "Permission denied (publickey)" error
- Key authentication not working

**Diagnosis**:
```bash
# Check key permissions on server
ls -la ~/.ssh/
# Should show: drwx------ (700) for .ssh/
#              -rw------- (600) for authorized_keys
```

**Resolution**:
```bash
# Fix permissions
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys

# Verify key is in authorized_keys
cat ~/.ssh/authorized_keys

# Check SSH daemon accepts keys
sudo sshd -t  # Test config
```

**Common mistakes**:
- Wrong permissions (755 or 644 won't work)
- Multiple keys on one line (should be one per line)
- Extra spaces or newlines in key file
- Key added for wrong user

---

### HDD Not Mounting on Boot

**Symptoms**:
- `/mnt/hdd` is empty after reboot
- Services can't find models or data
- `df -h` doesn't show HDD

**Diagnosis**:
```bash
# Check if mount failed
mount | grep /mnt/hdd

# Check fstab entry
cat /etc/fstab | grep /mnt/hdd

# Check UUID matches device
sudo blkid | grep <uuid-from-fstab>
```

**Resolution**:
```bash
# Get correct UUID
sudo blkid /dev/sda1  # Replace with your HDD partition

# Edit fstab with correct UUID
sudo nano /etc/fstab
# Should be: UUID=actual-uuid /mnt/hdd ext4 defaults,nofail 0 2

# Test mount
sudo mount -a

# Verify
df -h /mnt/hdd
```

**Critical**: Never use device letters (sda, sdb) - they change with boot order!

**Prevention**: Always use UUIDs and test with `sudo mount -a` before rebooting.

---

### Wrong UUID = System Won't Boot

**Symptoms**:
- System hangs during boot
- "Dependency failed" messages
- Emergency mode / rescue shell

**Cause**: Incorrect UUID in /etc/fstab without `nofail` flag.

**Resolution** (from rescue shell):
```bash
# Remove or comment out bad line in /etc/fstab
nano /etc/fstab

# Or add nofail option
UUID=wrong-uuid /mnt/hdd ext4 defaults,nofail 0 2
#                                      ^^^^^^^ prevents boot hang

# Reboot
reboot
```

**Prevention**: 
1. Always verify UUID before editing fstab
2. Always use `nofail` flag for non-essential mounts
3. Test with `sudo mount -a` before rebooting

---

### SELinux Blocking Samba Access

**Symptoms**:
- Windows shows "System error 67" or "Network name not found"
- Can ping server but can't access share
- `testparm` shows config is correct

**Diagnosis**:
```bash
# Check SELinux is enforcing
getenforce  # Should show: Enforcing

# Check Samba booleans
getsebool -a | grep samba

# Check file contexts
ls -Z /mnt/hdd/share
```

**Resolution**:
```bash
# Enable Samba SELinux booleans
sudo setsebool -P samba_export_all_rw on
sudo setsebool -P samba_export_all_ro on

# Set correct context on share directory
sudo semanage fcontext -a -t samba_share_t "/mnt/hdd/share(/.*)?"
sudo restorecon -Rv /mnt/hdd/share

# Verify context
ls -Z /mnt/hdd/share
# Should show: samba_share_t

# Restart Samba
sudo systemctl restart smb nmb
```

**Common mistake**: Forgetting to set SELinux contexts on new directories.

---

## Service-Specific Issues

### Ollama: Response Takes 10+ Minutes

**Symptoms**:
- Model responds but extremely slowly
- `ollama run` takes forever
- API requests timeout
- CPU at 100% for extended periods

**Cause**: Model too large for CPU-only system.

**Diagnosis**:
```bash
# Check which models installed
ollama list

# Check model size
ollama show <model-name>
```

**Resolution**:
```bash
# Remove slow models (>3B parameters)
ollama rm llama3.2      # If you have it
ollama rm phi3:mini     # If too slow

# Use fast models only
ollama pull smollm2     # 1.7B - fast
ollama pull qwen2.5:1.5b  # 1.5B - fast
```

**Performance expectations**:
- 1-2B models: 10-30 seconds (acceptable)
- 3-7B models: 60-180 seconds (too slow)
- 7B+ models: 10+ minutes (unusable on CPU)

**Prevention**: Always test model performance before relying on it.

---

### Ollama: Port 11434 Already in Use

**Symptoms**:
- Ollama service fails to start
- "address already in use" error
- Two Ollama instances running

**Cause**: Manual `ollama serve` still running when systemd tries to start.

**Diagnosis**:
```bash
# Check what's using port
sudo ss -tlnp | grep 11434

# Check for multiple Ollama processes
ps aux | grep ollama
```

**Resolution**:
```bash
# Kill all Ollama processes
sudo pkill -9 ollama

# Start via systemd only
systemctl --user start ollama

# Verify single process
ps aux | grep ollama
```

**Prevention**: Always use `systemctl --user start ollama`, never `ollama serve` manually.

---

### LiteLLM: Environment Variables Not Loading

**Symptoms**:
- Claude API requests fail with authentication errors
- LiteLLM logs show "Invalid API key"
- Container shows ANTHROPIC_API_KEY not set

**Cause**: EnvironmentFile in wrong systemd section (see Session 15 fix).

**Diagnosis**:
```bash
# Check if variables reached container
podman exec litellm printenv | grep ANTHROPIC_API_KEY

# Should output: ANTHROPIC_API_KEY=sk-ant-...
# If empty, EnvironmentFile not working
```

**Resolution**:
```bash
# Edit quadlet file
nano ~/.config/containers/systemd/litellm.container

# Ensure EnvironmentFile is in [Container] section
[Container]
Image=ghcr.io/berriai/litellm:main-stable
EnvironmentFile=%h/.config/litellm.env  # HERE, not in [Service]!
...

[Service]
Restart=on-failure
# NOT here - won't reach container

# Reload and restart
systemctl --user daemon-reload
systemctl --user restart litellm

# Verify
podman exec litellm printenv | grep ANTHROPIC_API_KEY
```

**Critical**: This is a Podman quadlet-specific requirement. EnvironmentFile in [Service] section sets env for systemd process, NOT container.

---

### LiteLLM: Requests Hang Indefinitely

**Symptoms**:
- `/health` endpoint never responds
- Chat completions timeout
- No error message, just hangs
- Container logs show "waiting for database"

**Cause**: Database stack deadlock (Session 12-14 issue).

**Diagnosis**:
```bash
# Check for database-related files
ls ~/.config/containers/systemd/ | grep -E "db|postgres"

# Check config for database_url
cat ~/.litellm/config.yaml | grep database
```

**Resolution**:
```bash
# Remove database stack completely
rm ~/.config/containers/systemd/litellm-db.container
rm ~/.config/containers/systemd/litellm-db.volume
rm ~/.config/containers/systemd/litellm.network

# Edit config, remove database lines
nano ~/.litellm/config.yaml
# Remove: database_url, store_model_in_db, litellm_salt_key

# Reload and restart
systemctl --user daemon-reload
systemctl --user restart litellm
```

**Prevention**: NEVER use `database_url` in LiteLLM config. Keep stateless.

**Related**: See [DECISIONS.md](DECISIONS.md) - "LiteLLM Database Stack Removal"

---

### LiteLLM: Ollama Models Not Found

**Symptoms**:
- Requests to local models fail
- "Model not found" errors
- Ollama works directly but not via LiteLLM

**Diagnosis**:
```bash
# Test Ollama directly
curl http://localhost:11434/api/tags

# Check LiteLLM can reach Ollama
podman exec litellm curl http://localhost:11434/api/tags
```

**Resolution**:
```bash
# Verify Ollama bound to 0.0.0.0
systemctl --user cat ollama | grep OLLAMA_HOST
# Should show: Environment="OLLAMA_HOST=0.0.0.0:11434"

# If wrong, edit service
nano ~/.config/systemd/user/ollama.service

# Add to [Service] section
Environment="OLLAMA_HOST=0.0.0.0:11434"

# Reload and restart
systemctl --user daemon-reload
systemctl --user restart ollama

# Verify
curl http://localhost:11434/api/tags
```

**Common mistake**: Ollama defaults to 127.0.0.1 which containers can't reach.

---

### AnythingLLM: Can't Connect to LiteLLM

**Symptoms**:
- AnythingLLM shows "Connection failed"
- Models don't appear in dropdown
- Test connection fails in UI

**Diagnosis**:
```bash
# Check LiteLLM is running
systemctl --user status litellm

# Test LiteLLM from server
source ~/.silverblue-ai-config
curl http://localhost:4000/health \
  -H "Authorization: Bearer ${LITELLM_MASTER_KEY}"
```

**Resolution**:
1. Verify LiteLLM running and healthy
2. In AnythingLLM UI, configure LLM provider:
   - Type: Generic OpenAI
   - Base URL: `http://localhost:4000/v1`
   - API Key: Your LITELLM_MASTER_KEY from `~/.silverblue-ai-config`
3. Click "Test Connection"
4. Select model from dropdown

**Common mistakes**:
- Using wrong API key
- Forgetting `/v1` at end of base URL
- LiteLLM not actually running

---

### AnythingLLM: Port 3001 Inaccessible

**Symptoms**:
- Browser shows "Connection refused" at http://localhost:3001
- SSH tunnel established but no response

**Diagnosis**:
```bash
# Check container running
podman ps | grep anythingllm

# Check port listening on server
sudo ss -tlnp | grep 3001
```

**Resolution**:
```bash
# Start AnythingLLM if not running
podman start anythingllm

# Or run if not exists
podman run -d \
  --name anythingllm \
  --network host \
  -v /mnt/hdd/projects/anythingllm-storage:/app/server/storage:Z \
  --cap-add SYS_ADMIN \
  ghcr.io/mintplex-labs/anythingllm:master

# Verify SSH tunnel from Windows
ssh -L 3001:localhost:3001 mal@silverblue-ai

# Browse to: http://localhost:3001
```

---

## Network and Firewall Issues

### Firewall Exposes High Ports (1025-65535)

**Symptoms**:
- Can access LiteLLM from LAN without SSH tunnel
- Port 4000, 11434, or 18789 accessible externally
- Security audit shows open ports

**Cause**: FedoraWorkstation zone has blanket high-port rule (Session 17 discovery).

**Diagnosis**:
```bash
# Check firewall rules
sudo firewall-cmd --list-all

# Look for: ports: 1025-65535/tcp 1025-65535/udp
```

**Resolution**:
```bash
# Remove dangerous port range
sudo firewall-cmd --permanent --remove-port=1025-65535/tcp
sudo firewall-cmd --permanent --remove-port=1025-65535/udp
sudo firewall-cmd --reload

# Verify removed
sudo firewall-cmd --list-all
# ports: should be empty or only specific ports

# Test from Windows
Test-NetConnection -ComputerName 192.168.0.33 -Port 4000
# Should fail (TcpTestSucceeded: False)
```

**Critical**: This is a security vulnerability. All AI services should be localhost-only.

**Prevention**: Audit firewall on every new deployment.

---

### Tailscale Not Connecting

**Symptoms**:
- Can't SSH via Tailscale hostname
- `tailscale status` shows disconnected
- IP doesn't appear in Tailscale admin

**Diagnosis**:
```bash
# Check service
systemctl status tailscaled

# Check auth status
sudo tailscale status
```

**Resolution**:
```bash
# Bring up Tailscale
source ~/.silverblue-ai-config
sudo tailscale up --authkey ${TAILSCALE_AUTHKEY} --hostname silverblue-ai

# Verify connected
sudo tailscale status

# Get IP
sudo tailscale ip -4
```

**Common issues**:
- Auth key expired (generate new one)
- Service not enabled: `sudo systemctl enable --now tailscaled`
- Firewall blocking: Tailscale handles this automatically

---

### Samba Share Not Accessible from Windows

**Symptoms**:
- Can ping server but \\server\share fails
- "Network path not found" error
- testparm shows correct config

**Diagnosis**:
```bash
# Check services running
systemctl status smb nmb

# Check firewall
sudo firewall-cmd --list-services | grep samba

# Check SELinux contexts
ls -Z /mnt/hdd/share
```

**Resolution** (complete checklist):
```bash
# 1. Verify services running
sudo systemctl restart smb nmb

# 2. Set Samba password
smbpasswd -a $USER

# 3. Configure firewall
sudo firewall-cmd --permanent --zone=FedoraWorkstation --add-service=samba
sudo firewall-cmd --reload

# 4. Fix SELinux (see earlier section)
sudo setsebool -P samba_export_all_rw on
sudo semanage fcontext -a -t samba_share_t "/mnt/hdd/share(/.*)?"
sudo restorecon -Rv /mnt/hdd/share

# 5. Test from Windows
net use Z: \\192.168.0.33\share /user:mal
```

**Most common cause**: SELinux contexts not set (step 4).

---

## Performance Issues

### System Runs Out of RAM

**Symptoms**:
- OOM (Out of Memory) killer activates
- Services crash randomly
- `free -h` shows no available memory
- System becomes unresponsive

**Diagnosis**:
```bash
# Check memory usage
free -h

# Check what's using memory
ps aux --sort=-%mem | head -20

# Check container usage
podman stats
```

**Immediate resolution**:
```bash
# Stop non-essential services temporarily
systemctl --user stop ollama

# Or restart heavy containers
podman restart anythingllm
```

**Long-term solutions**:
1. Use smaller models (1-2B parameters)
2. Don't run multiple models simultaneously
3. Limit AnythingLLM embeddings cache
4. Consider adding more RAM (16GB recommended)
5. Disable GDM if still enabled: `sudo systemctl disable gdm`

---

### Disk Space Running Low

**Symptoms**:
- "No space left on device" errors
- Services fail to write logs
- Models won't download

**Diagnosis**:
```bash
# Check overall usage
df -h

# Check HDD directories
du -sh /mnt/hdd/*

# Find large model files
du -ah /mnt/hdd/llms | sort -rh | head -20
```

**Resolution**:
```bash
# Remove unused models
ollama list
ollama rm <unused-model>

# Clean up old logs (if accumulating)
journalctl --vacuum-time=7d

# Remove old container images
podman image prune -a

# Check what else is using space
du -ah /home/$USER | sort -rh | head -20
```

---

## Recently Resolved Issues (Reference)

### âœ… Critical Firewall Misconfiguration (Session 17)

**Status**: Resolved  
**Solution**: Remove ports 1025-65535 from firewall  
**See**: [Network and Firewall Issues](#firewall-exposes-high-ports-1025-65535) above

---

### âœ… LiteLLM EnvironmentFile Not Loading (Session 15)

**Status**: Resolved  
**Solution**: Move EnvironmentFile to [Container] section in quadlet  
**See**: [LiteLLM: Environment Variables Not Loading](#litellm-environment-variables-not-loading) above

---

### âœ… Database Stack Deadlock (Sessions 12-14)

**Status**: Resolved  
**Solution**: Remove database stack entirely from LiteLLM  
**Decision**: Never use database_url in LiteLLM config  
**See**: [LiteLLM: Requests Hang Indefinitely](#litellm-requests-hang-indefinitely) above

---

### âœ… OpenClaw Security Vulnerabilities (Session 15)

**Status**: OpenClaw removed from deployment  
**Reason**: Critical CVEs, 21,639+ compromised instances  
**Alternative**: AnythingLLM deployed in v2026.02  
**See**: [CHANGELOG.md](CHANGELOG.md) - v2026.01

---

### âœ… Git Protocol Blocked (Session 17)

**Status**: Resolved  
**Solution**: Use HTTPS tarball download instead of git clone  
**Command**: `curl -L https://github.com/openclaw/openclaw/archive/refs/tags/v2026.2.9.tar.gz -o openclaw.tar.gz`

---

### âœ… Wrong OpenClaw Repository URL (Session 17)

**Status**: Resolved  
**Correct**: `github.com/openclaw/openclaw` (not `lastmile-ai/openclaw`)  
**Fixed**: In deployment guide v2.3

---

## Getting More Help

**If issue not listed here**:

1. **Check logs first**:
   ```bash
   journalctl --user -u <service> -n 100
   podman logs <container> --tail 100
   ```

2. **Search DECISIONS.md** for context on design choices

3. **Review ARCHITECTURE.md** for how components interact

4. **Check REFERENCE.md** for correct commands and configs

5. **Verify from DEPLOYMENT.md** that setup was correct

6. **Test components individually**:
   - Ollama: `curl http://localhost:11434/api/tags`
   - LiteLLM: `curl http://localhost:4000/health`
   - AnythingLLM: Browse http://localhost:3001

---

**Related Documentation**:
- [OPERATIONS.md](OPERATIONS.md) - Daily management procedures
- [REFERENCE.md](REFERENCE.md) - Command reference
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [DECISIONS.md](DECISIONS.md) - Why things work this way

**Status**: Current troubleshooting guide for v2026.02  
**Last Updated**: February 2026  
**Note**: Add new issues as discovered, mark resolved issues with date
