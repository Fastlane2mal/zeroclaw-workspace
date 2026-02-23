# Commands Reference

## Access the Server

**SSH from Windows PowerShell**:
```powershell
ssh silverblue-ai
# or with full address:
ssh mal@100.110.112.76
```

**SSH tunnel for AnythingLLM web UI**:
```powershell
ssh -L 3001:localhost:3001 silverblue-ai
# Then open: http://localhost:3001
```

---

## Health Checks

**Check all core services**:
```bash
systemctl --user status ollama litellm
```

**Full system health check**:
```bash
# Services
systemctl --user status ollama litellm
# API health
curl -s http://localhost:4000/health -H "Authorization: Bearer ${LITELLM_MASTER_KEY}"
# Available models
curl -s http://localhost:4000/v1/models -H "Authorization: Bearer ${LITELLM_MASTER_KEY}" | jq -r '.data[].id'
# RAM usage
free -h | grep Mem
# Disk usage
df -h /mnt/hdd
# AnythingLLM running?
podman ps | grep anythingllm
```

**Test a model response**:
```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer ${LITELLM_MASTER_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"model": "smollm2", "messages": [{"role": "user", "content": "Hello"}]}'
```

---

## Service Management

**Ollama**:
```bash
systemctl --user start ollama
systemctl --user stop ollama
systemctl --user restart ollama
journalctl --user -u ollama -n 50      # last 50 log lines
journalctl --user -u ollama -f         # follow live logs
```

**LiteLLM**:
```bash
systemctl --user start litellm
systemctl --user stop litellm
systemctl --user restart litellm
podman logs litellm --tail 50
podman logs litellm -f
```

**AnythingLLM**:
```bash
podman start anythingllm
podman stop anythingllm
podman restart anythingllm
podman logs anythingllm --tail 50
podman logs anythingllm -f
```

**All services (restart everything)**:
```bash
systemctl --user restart ollama litellm
podman restart anythingllm
```

---

## Model Management (Ollama)

**List installed models**:
```bash
ollama list
```

**Download a model**:
```bash
ollama pull smollm2
ollama pull qwen2.5:1.5b
```

**Remove a model**:
```bash
ollama rm llama3.2
```

**Test a model directly**:
```bash
ollama run smollm2
```

**Check how much RAM models use**:
```bash
ollama ps
```

---

## Resource Monitoring

**RAM usage**:
```bash
free -h
```

**CPU usage (live)**:
```bash
htop
```

**Container resource usage (live)**:
```bash
podman stats
```

**Disk usage**:
```bash
df -h /mnt/hdd
du -sh /mnt/hdd/llms/      # model storage
du -sh /mnt/hdd/projects/   # project storage
```

---

## Troubleshooting

**Check if API keys are reaching LiteLLM container**:
```bash
podman exec litellm printenv | grep ANTHROPIC_API_KEY
podman exec litellm printenv | grep GROQ_API_KEY
```

**Check what's using a port**:
```bash
sudo ss -tlnp | grep 4000
```

**Check Tailscale VPN status**:
```bash
tailscale status
```

**Check for suspend attempts (should be empty)**:
```bash
sudo journalctl --since "1 hour ago" | grep -i suspend
uptime
```

**Verify HDD is mounted**:
```bash
df -h /mnt/hdd
ls /mnt/hdd
```

---

## Configuration Files (Location Reference)
| File | What It's For |
|---|---|
| `~/.silverblue-ai-config` | Master config: API keys, paths |
| `~/.litellm/config.yaml` | LiteLLM model list |
| `~/.config/litellm.env` | LiteLLM API key environment vars |
| `~/.config/systemd/user/ollama.service` | Ollama service definition |
| `~/.config/containers/systemd/litellm.container` | LiteLLM container definition |
| AnythingLLM launch command (see Services page) | AnythingLLM run via podman run (not a quadlet) |
| `/etc/fstab` | HDD auto-mount on boot |

## Related
- [[Services]] — what each service does
- [[Known Issues]] — common problems and fixes
