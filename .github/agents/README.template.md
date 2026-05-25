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

## Supported API Endpoints
| API Type | Endpoint | Description |
|---|---|---|
| **OpenAI** | `/v1/chat/completions` | Standard Chat Completions (Supports Tool Calling & Vision) |
| **OpenAI Models**| `/v1/models` | Returns available model aliases |
| **OpenAI Images**| `/v1/images/generations` | DALL-E 3 compatible image generation |
| **Anthropic** | `/anthropic/v1/messages` | Claude SDK / Claude Code compatible |
| **Gemini** | `/v1beta/models/*` | Google GenAI SDK compatible |
| **Gemini Stream**| `/v1beta/models/{model}:streamGenerateContent`| Gemini Streaming |
| **Health Probes**| `/healthz` & `/readyz` | Liveness & Readiness endpoints for Coolify |

*Note: Default upstream routing sends all modern model names (gpt-4o, claude-3-5-sonnet, gemini-2.5-pro) to `qwen3.6-plus` automatically.*

---

## Environment Variables (.env)

**PORT and WORKERS are pre-configured in `docker-compose.build.yml` by the automated maintenance agent. You only need to set `ADMIN_KEY` in the Coolify environment UI.**

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

---

## Data Persistence
This application uses a file-based database for account storage and caching. The persistence is managed via bind mounts mapped to the relative project directory.

Ensure Coolify creates and mounts the following:
* `./data:/workspace/data`
* `./logs:/workspace/logs`

*Note: The environment variables such as `ACCOUNTS_FILE` do not need to be set manually, as the application's default paths correctly point to `/workspace/data/` inside the container.*

---

## Troubleshooting & System Requirements

* **OOM (Out of Memory) Crashes:** The headless Firefox engine (Camoufox) requires shared memory. Ensure your Coolify deployment allows `shm_size: '256m'` (or `512m` if unstable).
* **WebUI requires password instantly:** This is standard SPA behavior. Click "System Settings" (bottom left gear icon) and paste your `ADMIN_KEY` into the Session Key box.
* **403 Forbidden / Empty Responses:** Indicates the upstream Aliyun WAF is blocking your server IP. Ensure you have injected an active web session token in the "Accounts" tab.
