# qwen2API Enterprise Gateway (Coolify Edition)

A high-performance gateway converting chat.qwen.ai web access into OpenAI, Anthropic, and Gemini compatible APIs. 

**This fork has been optimized for Coolify Source Builds. The React WebUI is fully translated to English, and heavy/unused OS dependencies have been stripped.**

---

## Deployment (Coolify Source Build)
1. Add a **New Resource -> Public Repository** in Coolify.
2. Point it to this repository.
3. **In Coolify, set the Docker Compose File to `docker-compose.build.yml`.** This file contains the `build: context: .` directive that builds your fork from source.
4. Set the Required Environment Variables (see below).
5. Deploy.

---

## Environment Variables (.env)
**PORT, WORKERS, and volume mounts are pre-configured in `docker-compose.build.yml` by the maintenance agent.**

### Core Configuration
| Variable | Default | Notes |
|---|---|---|
| `ADMIN_KEY` | `admin` | **Must change!** Master password for the WebUI. |
| `PORT` | `7860` | Pre-configured by agent. |
| `WORKERS` | `1` | Pre-configured by agent. |

### Concurrency & Rate Limiting
| Variable | Default | Notes |
|---|---|---|
| `BROWSER_POOL_SIZE` | `1` | Number of Camoufox pages. Higher = more RAM used. |
| `MAX_INFLIGHT` | `2` | Max concurrent requests per upstream account. |
| `ACCOUNT_MIN_INTERVAL_MS`| `0` | Minimum ms between requests for the same account. |
| `RATE_LIMIT_BASE_COOLDOWN`| `600` | Base cooldown in seconds if an account hits a 429 WAF block. |
