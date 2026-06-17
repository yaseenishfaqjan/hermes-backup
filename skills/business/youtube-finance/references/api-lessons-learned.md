# API Integration Lessons Learned — Global Signal Pipeline

## ElevenLabs Voice ID (LOCKED)

**Voice ID:** `auq43ws1oslv0tO4BDa7`
**Status:** ✅ Verified working — 22 voices available, target voice confirmed
**Rule:** NEVER use any other voice for Global Signal channel

### API Key Loading Pattern (IMPORTANT)

When loading API keys from `.env` files in Python scripts, `os.environ.get()` does NOT always work because the environment may not be loaded.

**Correct Pattern:**
```python
import os

# Method 1: Read .env file directly (MOST RELIABLE)
def load_api_key(key_name, env_file="/root/.hermes/.env"):
    """Load API key directly from .env file"""
    try:
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith(f"{key_name}="):
                    return line.strip().split('=', 1)[1].strip().strip('"').strip("'")
    except:
        pass
    
    # Fallback to environment
    return os.environ.get(key_name, "")

# Usage
ELEVENLABS_KEY = load_api_key("ELEVENLABS_API_KEY")
OPENAI_KEY = load_api_key("OPENAI_API_KEY")
PERPLEXITY_KEY = load_api_key("PERPLEXITY_API_KEY")
```

**Why this matters:** The `source /root/.hermes/.env` command only works in the shell session that runs it. Python scripts started separately won't inherit those variables unless the environment is explicitly loaded.

## Higgsfield API Issue

**Status:** ❌ API Server Down (522 Cloudflare Error)
**URL:** https://api.higgsfield.ai/v1/images/generations
**Error:** Connection timed out

### Workarounds (in order of preference)

1. **HyperFrames** (Recommended)
   - Already installed locally: `hyperframes v0.6.103`
   - No API key needed
   - Command: `npx hyperframes render --output video.mp4`
   - Can generate thumbnails via HTML composition + screenshot

2. **Image Generation Tools**
   - Use `image_generate` tool if available
   - Or other image generation APIs (DALL-E, Midjourney, etc.)

3. **Cloudinary Transformations**
   - Transform existing images
   - Add text overlays, effects

4. **Wait for Higgsfield Fix**
   - Monitor https://higgsfield.ai/status
   - Retry later

### Testing Higgsfield API

```python
import requests

HIGGSFIELD_KEY = load_api_key("HIGGSFIELD_API_KEY")

url = "https://api.higgsfield.ai/v1/images/generations"
headers = {"Authorization": f"Bearer {HIGGSFIELD_KEY}"}
data = {"prompt": "test image", "size": "1024x1024"}

response = requests.post(url, json=data, headers=headers, timeout=10)
print(f"Status: {response.status_code}")

if response.status_code == 522:
    print("❌ Higgsfield API is down (Cloudflare timeout)")
    print("Use HyperFrames or alternative instead")
```

## API Status Check Script

Save this as a verification script:

```python
#!/usr/bin/env python3
"""Quick API health check for Global Signal pipeline"""

import requests

def load_api_key(key_name):
    with open('/root/.hermes/.env', 'r') as f:
        for line in f:
            if line.startswith(f"{key_name}="):
                return line.strip().split('=', 1)[1].strip().strip('"').strip("'")
    return ""

def check_elevenlabs():
    key = load_api_key("ELEVENLABS_API_KEY")
    headers = {"xi-api-key": key}
    r = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers, timeout=10)
    return r.status_code == 200

def check_openai():
    key = load_api_key("OPENAI_API_KEY")
    headers = {"Authorization": f"Bearer {key}"}
    r = requests.get("https://api.openai.com/v1/models", headers=headers, timeout=10)
    return r.status_code == 200

def check_perplexity():
    key = load_api_key("PERPLEXITY_API_KEY")
    headers = {"Authorization": f"Bearer {key}"}
    r = requests.get("https://api.perplexity.ai/models", headers=headers, timeout=10)
    return r.status_code == 200

def check_higgsfield():
    key = load_api_key("HIGGSFIELD_API_KEY")
    headers = {"Authorization": f"Bearer {key}"}
    r = requests.post("https://api.higgsfield.ai/v1/images/generations", 
                      json={"prompt": "test"}, headers=headers, timeout=10)
    return r.status_code not in [522, 503, 502]  # Accept 401 (auth ok, bad prompt)

print("API Health Check:")
print(f"  ElevenLabs: {'✅' if check_elevenlabs() else '❌'}")
print(f"  OpenAI: {'✅' if check_openai() else '❌'}")
print(f"  Perplexity: {'✅' if check_perplexity() else '❌'}")
print(f"  Higgsfield: {'✅' if check_higgsfield() else '❌'}")
```

## Connected APIs (Confirmed Working)

| API | Key Present | Status | Notes |
|-----|-------------|--------|-------|
| ElevenLabs | ✅ | ✅ Working | Voice ID auq43ws1oslv0tO4BDa7 confirmed |
| OpenAI | ✅ | ✅ Working | Key starts with sk-proj-... |
| Perplexity | ✅ | ✅ Working | Key configured |
| Zernio | ✅ | ✅ Working | Social media posting ready |
| HeyGen | ✅ | ✅ Working | Avatar generation ready |
| Firecrawl | ✅ | ✅ Working | Web scraping ready |
| Cloudinary | ✅ | ✅ Working | Image optimization ready |
| HyperFrames | N/A | ✅ Working | v0.6.103 local install |
| Higgsfield | ✅ | ❌ Down | 522 Cloudflare error |

## Marketing Skills Repo

**Cloned from:** https://github.com/coreyhaines31/marketingskills
**Location:** `/root/.hermes/skills/marketing-strategy/`
**Skills Available:** 46 marketing skills (ab-testing, ad-creative, content-strategy, copywriting, cro, email, seo, social, video, etc.)

## Key Commands

```bash
# Load environment (must do before running scripts)
source /root/.hermes/.env

# Test ElevenLabs voice
curl -X GET "https://api.elevenlabs.io/v1/voices" \
  -H "xi-api-key: $(grep ELEVENLABS_API_KEY /root/.hermes/.env | cut -d= -f2 | tr -d '"')"

# Check HyperFrames
hyperframes --version

# Run full pipeline
python3 /root/.hermes/skills/business/youtube-finance/scripts/master_pipeline.py
```

## Higgsfield MCP Integration (NEW)

**MCP URL:** `https://mcp.higgsfield.ai/mcp`
**Status:** ✅ Working via browser
**CLI Install:** `curl -fsSL https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh | sh`
**CLI Version:** v0.2.1 (installed)
**Authentication:** Device login via browser
**Device Code URL:** `https://higgsfield.ai/device?code=CODE`

### Higgsfield CLI Commands

```bash
# Check version
higgsfield --version

# Authenticate (opens browser)
higgsfield auth login

# Check status
higgsfield auth status

# Generate image
higgsfield generate create nano_banana_2 \
  --prompt "Your prompt here" \
  --aspect_ratio 16:9 \
  --resolution 2k \
  --wait

# Generate video
higgsfield generate create nano_banana_2 \
  --prompt "Your video prompt" \
  --duration 5 \
  --wait
```

### Browser Automation Alternative

When API is down, use browser automation:
1. Navigate to https://higgsfield.ai/image or /video
2. Enter prompt manually
3. Download generated media
4. Upload to VPS via scp or download tools

### MCP Integration for Hermes

```python
# Use Hermes browser tools to interact with Higgsfield MCP
# 1. Navigate to https://mcp.higgsfield.ai/mcp
# 2. Authenticate with device code
# 3. Use browser tools to generate images/videos
# 4. Download results
```

## Marketing Skills Integration (NEW)

**Repo:** https://github.com/coreyhaines31/marketingskills
**Location:** `/root/.hermes/skills/marketing-skills-bundle/`
**Skills Count:** 46 marketing skills
**Categories:** ab-testing, ad-creative, content-strategy, copywriting, cro, email, seo, social, video, etc.

**Usage:**
```bash
# View all marketing skills
ls /root/.hermes/skills/marketing-skills-bundle/

# Use specific skill
skill_view("marketing-skills-bundle/<skill-name>")
```

## Global Signal Logo (NEW)

**File:** `/root/youtube_pipeline/assets/global_signal_logo.png`
**Size:** 1000x1000px
**Features:** Dark navy background, glowing blue globe, signal waves, "GLOBAL SIGNAL" + "DAILY ANALYSIS" text
**Generated via:** Higgsfield API (before outage)

## Video 1 Status (Trump Iran Deal)

**Script:** ✅ Complete (3,000 words, 20 minutes)
**Voiceover:** ❌ Blocked (API key loading issue)
**Thumbnail:** ❌ Blocked (Higgsfield API down)
**Visuals:** ❌ Not started
**Assembly:** ❌ Not started
**Upload:** ❌ Not started

## Video 2 Plan (Russia Energy Crisis)

**Topic:** Russia's Secret Plan to Freeze Europe
**Title:** "EXPOSED: Russia's Secret Plan to Freeze Europe This Winter"
**Hook:** "Europe is sleepwalking into another energy crisis, gas prices have nearly doubled"
**Script:** 🔄 Pending
**Status:** Waiting for Video 1 completion

## Last Updated

**Date:** 2026-06-16
**Session:** Higgsfield CLI setup + MCP integration + Video 2 planning
**Key Lessons:**
1. Always read .env files directly, don't rely on os.environ
2. Higgsfield API has 522 outages — use CLI or browser fallback
3. HyperFrames is local and reliable for video generation
4. Marketing skills repo adds 46 skills to the pipeline
5. Device login is required for Higgsfield CLI authentication
