# Changelog

**Purpose**: Version history and major changes  
**Format**: Date-based versioning (vYYYY.MM)  
**Last Updated**: February 2026

---

## Version History

### v2026.02 (February 2026) - Current Stable Baseline

**Release Date**: 2026-02-15  
**Session**: 21  
**Status**: 🟢 Production-ready

**Major Changes**:
- ✅ **AnythingLLM Web UI** deployed as Phase 5
  - Modern web interface for AI chat
  - Document upload with RAG capabilities
  - Multi-workspace support
  - Replaces OpenClaw as primary interface
  - Status: In-progress, functional
- ✅ **GDM (GNOME Display Manager) Disabled**
  - Reduces RAM usage by ~250MB
  - True headless operation (no display server)
  - Faster boot times
  - Command: `sudo systemctl disable gdm`
- ✅ **Groq Cloud Integration Stable**
  - Free tier models via LiteLLM
  - llama-3.3-70b (12k TPM)
  - llama-3.1-8b (6k TPM)
  - Fast responses (1-2s) for complex tasks
- ✅ **Documentation Consolidation**
  - Unified deployment guide
  - Clear troubleshooting procedures
  - Operations handbook created
  - Quick reference guide

**System Status**:
- Ollama: Running (smollm2, qwen2.5-1.5b)
- LiteLLM: Running (local + Groq + Claude)
- AnythingLLM: Running (port 3001)
- Caddy: Running (HTTPS proxy)
- Tailscale: Active (VPN access)
- Uptime: 24/7 stable

**Performance**:
- RAM usage: ~3.5GB idle (down from ~4GB)
- Local model response: 10-30s
- Cloud model response: 1-3s
- Boot time: ~45s (improved from 60s)

**Known Issues**:
- None critical
- Groq rate limits prevent direct OpenClaw integration
- See TROUBLESHOOTING.md for details

---

### v2026.01 (January 2026) - Security Hardening

**Release Date**: 2026-01-31  
**Sessions**: 15-20  
**Status**: 🟡 Superseded by v2026.02

**Major Changes**:
- âŒ **OpenClaw Removed** due to security vulnerabilities
  - CVE-2026-25253 (CVSS 8.8): 1-click RCE
  - CVE-2026-25157 (CVSS 7.8): SSH injection
  - CVE-2026-24763 (CVSS 8.8): Container escape
  - 21,639+ public instances compromised globally
  - Decision: Too risky for learning environment
- ✅ **Firewall Hardening**
  - Removed dangerous 1025-65535 port range
  - Verified localhost-only for AI services
  - Added firewall audit to deployment checklist
- ✅ **LiteLLM EnvironmentFile Fix**
  - Moved EnvironmentFile to [Container] section in quadlet
  - API keys now properly reach container
  - Claude routing working
- ✅ **Groq API Integration**
  - Added free tier cloud models
  - Integrated via LiteLLM proxy
  - Discovered rate limit incompatibility with OpenClaw
  - Kept for direct API use

**Session Highlights**:
- **Session 15**: LiteLLM quadlet fix, OpenClaw security removal
- **Session 16-17**: Firewall audit, repository URL corrections
- **Session 18**: Caddy HTTPS, auto-restart configuration
- **Session 19**: Groq integration, rate limit discovery
- **Session 20**: Stable baseline established

**Lessons Learned**:
- Always audit firewall on new deployments
- Check official docs before configuration changes
- Rate limits have multiple dimensions (RPM, TPM, RPD, TPD)
- Free tiers may not suit all usage patterns
- Agent frameworks have high token usage per request

---

### v2025.12 (December 2025) - Database Stack Removal

**Release Date**: 2025-12-XX  
**Sessions**: 12-14  
**Status**: 🔴 Deprecated - Critical bugs

**Major Changes**:
- âŒ **Removed Postgres Database Stack** from LiteLLM
  - Database deadlock causing complete service failure
  - `update_spend` job blocked all requests
  - No timeout, no error - just hung indefinitely
  - Resolution: Remove DB, use stateless config
- ✅ **Credentials Rotation**
  - Removed hardcoded credentials from container files
  - All credentials via EnvironmentFile
  - Added to security checklist
- âŒ **OpenClaw Deployment Attempts**
  - Multiple failed attempts (pairing issues)
  - Root cause: LiteLLM unavailable (DB deadlock)
  - Never actually an OpenClaw problem

**Critical Bugs**:
- LiteLLM Postgres deadlock (3 sessions lost)
- Credentials hardcoded in quadlet files
- EnvironmentFile in wrong section

**Decision**: Never use database_url in LiteLLM config (see DECISIONS.md)

---

### v2025.11 (November 2025) - Initial Deployment

**Release Date**: 2025-11-XX  
**Sessions**: 1-11  
**Status**: 🔴 Deprecated - Replaced by v2025.12

**Major Changes**:
- ✅ **Initial Platform Deployment**
  - Fedora Silverblue 40 installed
  - Ollama + local models (llama3.2)
  - LiteLLM proxy configured
  - Samba file sharing
  - SSH key authentication
- ✅ **Storage Architecture**
  - UUID-based fstab mounts
  - SSD for OS, HDD for models/data
  - Directory structure: llms/, projects/, backups/, share/
- ✅ **Service Infrastructure**
  - User-level systemd services
  - Podman containers for LiteLLM
  - Auto-start on boot
  - Power management disabled (24/7)
- ✅ **Network Configuration**
  - SSH remote access
  - Samba LAN file sharing
  - SELinux contexts configured

**Lessons Learned**:
- VM testing critical before hardware deployment
- UUID-based mounts essential for reliability
- User-level services avoid reboot requirements
- Minimal LiteLLM config reduces failure surface
- Documentation-driven development works well

---

## Component Version History

### Ollama
- **v0.5.0+** (Current) - Stable local inference
- Models: smollm2 (1.7B), qwen2.5:1.5b

### LiteLLM
- **main-stable** (Current) - Podman container deployment
- Config: Minimal (2-4 models, drop_params enabled)
- Removed: Database stack, complex routing, caching

### AnythingLLM
- **latest** (v2026.02+) - Primary web UI
- Deployment: Podman container
- Status: In-progress, functional
- Features: Chat, RAG, multi-workspace

### OpenClaw
- **v2026.2.9** - Last tested version
- Status: Removed in v2026.01 (security concerns)
- May be revisited when project matures
- See DECISIONS.md for full rationale

### Caddy
- **latest** (Current) - HTTPS reverse proxy
- Port: 8443
- Auto-restart: Enabled
- Self-signed certificates

### Tailscale
- **latest** (Current) - VPN access
- Status: Active, production use
- IP: 100.110.112.76
- Hostname: silverblue-ai.{tailnet}.ts.net

---

## Migration Guide

### From v2026.01 → v2026.02

**Required Actions**:
1. Disable GDM:
   ```bash
   sudo systemctl disable gdm
   sudo systemctl reboot
   ```

2. Deploy AnythingLLM (Phase 5):
   ```bash
   # Pull image
   podman pull ghcr.io/mintplex-labs/anythingllm:master
   
   # Create storage
   mkdir -p /mnt/hdd/projects/anythingllm-storage
   
   # Start container (see DEPLOYMENT.md Phase 5)
   ```

3. Update LiteLLM config (add Groq if using):
   ```yaml
   # Add to ~/.litellm/config.yaml
   - model_name: llama-3.3-70b
     litellm_params:
       model: groq/llama-3.3-70b-versatile
       api_key: os.environ/GROQ_API_KEY
   ```

4. Update environment file:
   ```bash
   # Add to ~/.silverblue-ai-config
   export GROQ_API_KEY="your-key-here"
   
   # Regenerate litellm.env
   sed 's/^export //; s/"//g' ~/.silverblue-ai-config > ~/.config/litellm.env
   ```

**Optional**:
- Remove OpenClaw containers/images (if present)
- Clean up old session files
- Archive old documentation

**Compatibility**: Backward compatible - existing LiteLLM config works

---

### From v2025.12 → v2026.01

**Required Actions**:
1. Remove OpenClaw (if deployed):
   ```bash
   podman stop openclaw-gateway
   podman rm openclaw-gateway
   podman rmi openclaw:local
   ```

2. Audit firewall:
   ```bash
   sudo firewall-cmd --list-all
   # Should NOT show: ports: 1025-65535/tcp
   
   # Remove if present
   sudo firewall-cmd --permanent --remove-port=1025-65535/tcp
   sudo firewall-cmd --permanent --remove-port=1025-65535/udp
   sudo firewall-cmd --reload
   ```

3. Verify LiteLLM environment:
   ```bash
   podman exec litellm printenv | grep ANTHROPIC_API_KEY
   # Should show actual key
   ```

**Breaking Changes**: None - additive only

---

### From v2025.11 → v2025.12

**Critical Actions**:
1. Remove database stack:
   ```bash
   rm ~/.config/containers/systemd/litellm-db.container
   rm ~/.config/containers/systemd/litellm-db.volume
   rm ~/.config/containers/systemd/litellm.network
   systemctl --user daemon-reload
   ```

2. Update LiteLLM config (remove database_url):
   ```yaml
   # Remove these lines from ~/.litellm/config.yaml
   database_url: ...
   store_model_in_db: true
   litellm_salt_key: ...
   ```

3. Rotate credentials:
   ```bash
   # Generate new
   openssl rand -hex 32  # New LITELLM_MASTER_KEY
   
   # Update ~/.silverblue-ai-config
   nano ~/.silverblue-ai-config
   
   # Regenerate env file
   sed 's/^export //; s/"//g' ~/.silverblue-ai-config > ~/.config/litellm.env
   ```

4. Restart LiteLLM:
   ```bash
   systemctl --user restart litellm
   ```

**Breaking Changes**:
- Database stack removed (cost tracking lost)
- Credentials rotated (update all clients)
- Stateless config only

---

## Future Roadmap

### Planned for v2026.03 (March 2026)

**Features**:
- [ ] Open WebUI as alternative to AnythingLLM
- [ ] Automated backup system via systemd timer
- [ ] Monitoring dashboard (Grafana + Prometheus)
- [ ] GPU acceleration support (when hardware available)
- [ ] Multi-model comparison in AnythingLLM

**Improvements**:
- [ ] Faster model loading (model caching)
- [ ] Better error messages in LiteLLM
- [ ] Cost tracking without database
- [ ] Automated model updates

**Documentation**:
- [ ] Video walkthrough
- [ ] Troubleshooting decision tree
- [ ] Performance tuning guide
- [ ] Multi-node deployment guide

### Long-term Vision (2026)

**Infrastructure**:
- Self-hosted model fine-tuning pipeline
- Integration with more AI frameworks
- Multi-node clustering for scalability
- Automated testing and CI/CD

**User Experience**:
- Web UI for system management
- Mobile app support
- Voice interface integration
- Automated model recommendations

**Community**:
- Public documentation site
- Contribution guidelines
- Example configurations
- Community model library

---

## Deprecation Policy

**Active Support**:
- Current version (v2026.02): Full support
- Previous version (v2026.01): Security fixes only
- Older versions: No support, archived

**Breaking Changes**:
- Announced 1 month in advance
- Migration guide provided
- Backward compatibility when possible

**Security Updates**:
- Critical: Immediate patch
- High: Within 1 week
- Medium: Next minor version
- Low: Next major version

---

## Version Numbering

**Format**: `vYYYY.MM[.PATCH]`

**Examples**:
- `v2026.02` - February 2026 release
- `v2026.02.1` - Patch 1 for February 2026
- `v2026.03` - March 2026 release

**Semantic**:
- **Major** (YYYY.MM): Monthly releases with features
- **Patch** (.N): Bug fixes, no new features
- No breaking changes between patches
- Breaking changes only in major versions

---

## Release Process

**Monthly Release Cycle**:
1. Feature development (weeks 1-3)
2. Testing and documentation (week 4)
3. Release on last day of month
4. Support previous version for 1 month

**Hotfix Process**:
1. Critical bug identified
2. Fix developed and tested
3. Patch release within 24-48 hours
4. Documentation updated

**Communication**:
- Changelog updated with each release
- Breaking changes highlighted
- Migration guides provided
- Known issues documented

---

**Related Documentation**:
- [README.md](README.md) - Current status
- [DEPLOYMENT.md](DEPLOYMENT.md) - Version-specific deployment
- [DECISIONS.md](DECISIONS.md) - Why changes were made
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Version-specific issues

**Status**: v2026.02 current release  
**Last Updated**: February 2026  
**Next Release**: v2026.03 (planned March 2026)
