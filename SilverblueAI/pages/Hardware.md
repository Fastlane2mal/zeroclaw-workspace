# Hardware

## Server Summary
- **Form factor**: Laptop, running headless (no monitor, no keyboard)
- **Access**: SSH only, via Tailscale VPN
- **Location**: Home network

## Specifications
| Component | Detail |
|---|---|
| CPU | Intel Core i5-8250U @ 1.60GHz |
| Cores | 4 physical cores, 8 threads |
| RAM | 11GB total |
| SSD | 224GB WDC WDS240G2G0B-00EPW0 (OS drive) |
| HDD | 932GB WDC WD10JPVX-60JC3T1 (data drive) |
| Network (wired) | eno1 (currently unused) |
| Network (wifi) | wlo1 (active connection) |
| Tailscale IP | 100.110.112.76 |
| Hostname | silverblue-ai |

## Storage Layout
- **SSD (sdb)**: Fedora Silverblue OS, container images, system files (~30GB used)
- **HDD (sda)**: AI models, project files, AnythingLLM data (~3GB used, 913GB free)
  - Mounted at: `/mnt/hdd`
  - Models stored at: `/mnt/hdd/llms/`
  - Projects stored at: `/mnt/hdd/projects/`

## Typical Resource Usage
| Resource | Idle | During AI Inference |
|---|---|---|
| RAM | ~3.5GB used | ~6GB used |
| CPU | 5-10% | 80-90% |
| HDD Space | ~3GB used | Same |

## Performance Expectations
- Local models (smollm2): 10-15 second responses
- Local models (qwen2.5-1.5b): 20-30 second responses
- Groq cloud (llama-3.3-70b): 1-2 second responses
- Claude cloud: Under 3 seconds

## Important Notes
- No GPU — all local AI inference runs on CPU only
- Models larger than ~3B parameters are too slow for practical use on this hardware
- The machine was originally a laptop; GDM (display manager) has been disabled since it's headless
- WiFi is active (eno1 wired not connected) — still stable for SSH and VPN

## Related
- [[Services]] — what software runs on this hardware
- [[Architecture]] — how the software layers are designed
