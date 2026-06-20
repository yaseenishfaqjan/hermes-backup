---
name: youtube-automation
description: When the user wants to create, automate, or manage a YouTube channel with AI-generated content. Use for video production pipelines, script generation, voiceover creation, thumbnail generation, and channel management. Also use when the user mentions 'YouTube automation', 'AI video', 'video pipeline', 'content calendar', 'video script', 'voiceover', 'thumbnail', or 'channel growth'.
metadata:
  version: 1.0.0
  author: Global Signal Team
---

# YouTube Automation Pipeline

Complete system for running an AI-powered YouTube channel with automated research, scripting, voiceover, and video production.

## Prerequisites

### Required API Keys (add to .env)
```bash
ELEVENLABS_API_KEY=***  # Voice generation
PERPLEXITY_API_KEY=***  # News research
OPENAI_API_KEY=***      # Script generation (optional)
YOUTUBE_VOICE_ID=auq43ws1oslv0tO4BDa7  # Global Signal voice
```

### Local Tools (no API key needed)
- **HyperFrames**: v0.6.103 installed at `/usr/local/bin/npx`
- **FFmpeg**: For video assembly
- **Python 3.11+**: For pipeline scripts

## Pipeline Architecture

```
Research → Script → Voiceover → Visuals → Assembly → Upload
```

### Directory Structure
```
/root/youtube_pipeline/
├── content_calendar/     # JSON topic selections
├── scripts/              # TXT scripts + JSON metadata
├── voiceovers/           # MP3 audio files
├── visuals/              # Images and B-roll
├── final_videos/         # Completed MP4 videos
└── assets/               # Logo, branding, templates
```

## Phase 1: Research (6am EST)

### Find Trending Topics
Use Perplexity API to search:
```
"top geopolitical news today site:youtube.com views:1M+"
"trending finance news [DATE] most watched"
"Russia China USA trade war latest breaking news"
```

### Competitor Analysis
Monitor these channels:
- The Rational Perspective
- Military HQ
- George Conway type channels
- Jeffrey Sachs analysis

For each viral video, note:
- Title structure
- Thumbnail style
- Hook (first 30 seconds)
- Video length
- View velocity (VPH)

## Phase 2: Script Writing (7am EST)

### Script Structure (18-25 minutes)
```
[HOOK] 0:00-0:45 — Most shocking statement first
[TEASE] 0:45-2:00 — What they will learn
[CONTEXT] 2:00-6:00 — Background explanation
[MAIN] 6:00-18:00 — Core content (3-4 sections)
[ECONOMIC] 18:00-22:00 — Money impact
[CTA] 22:00-25:00 — Subscribe + next video
```

### Script Rules
- Use "you" and "we" — conversational
- Short sentences under 20 words
- One idea per paragraph
- Add "..." pauses for natural delivery
- Never use: "delve", "crucial", "leverage", "utilize"
- Cite specific numbers always
- Every 3 minutes: new revelation or twist

## Phase 3: Voiceover (8am EST)

### ElevenLabs Configuration
- **Voice ID**: `auq43ws1oslv0tO4BDa7` (Adam Stone)
- **Model**: `eleven_turbo_v2_5`
- **Stability**: 0.5
- **Similarity Boost**: 0.75
- **Speed**: 150 WPM

### Generate Voiceover
```bash
python3 /root/.hermes/skills/business/youtube-finance/scripts/voiceover_generator.py \
  /path/to/script.txt
```

## Phase 4: Visuals (8am-10am EST)

### Thumbnail Formula
- Size: 1280x720px
- Background: Dark (black/dark blue)
- Text: 2-3 words MAX, bold yellow/white, ALL CAPS
- Elements: Face + red arrows + flag/map
- Emotion: Shock, alarm, urgency

### HyperFrames Video Template
```bash
npx hyperframes init video-project
cd video-project
npx hyperframes render -o output.mp4
```

## Phase 5: Assembly & Upload

### Video Specs
- Resolution: 1920x1080 (Full HD)
- Duration: 18-25 minutes
- Audio: -20db background music
- Captions: Always enabled

### YouTube SEO
**Title Structure:**
```
[POWER WORD]: [WHAT HAPPENED] — [CONSEQUENCE] | [SOURCE]
```

**Description Template:**
```
[First 2 lines = hook]

⏱ CHAPTERS:
0:00 - Introduction
2:00 - Background
[etc.]

🔔 Subscribe for daily analysis

#geopolitics #economy #globalfinance
```

## Troubleshooting

### ElevenLabs API Issues
- Check key: `source /root/.hermes/.env && echo ${ELEVENLABS_API_KEY:0:10}`
- Test: `curl -H "xi-api-key: $KEY" https://api.elevenlabs.io/v1/voices`
- Common error: 401 = invalid key, 429 = rate limit
- **Important**: Key must be loaded from .env file using `source` command before use
- Python scripts must load environment variables before API calls

### Higgsfield Down (522 Error)
- Status: API server temporarily unreachable (Cloudflare timeout)
- Alternative: Use HyperFrames for visuals or wait for service recovery
- Check: `curl -I https://api.higgsfield.ai/v1/health`
- **Note**: Higgsfield API key is valid (67 chars) but server is returning 522 errors
- Fallback: Use image_generate tool or HyperFrames for thumbnails

### HyperFrames Not Rendering
- Check version: `npx hyperframes --version`
- Update: `npm install -g hyperframes`
- Doctor: `npx hyperframes doctor`
- **Note**: HyperFrames v0.6.103 is installed locally, no API key needed
- If npx command not found: `/usr/local/bin/npx hyperframes --version`

### Environment Variables Not Loading
- **Issue**: Python scripts cannot read .env file automatically
- **Fix**: Use `source /root/.hermes/.env` before running scripts
- **Alternative**: Read .env file directly in Python:
  ```python
  with open('/root/.hermes/.env', 'r') as f:
      env_content = f.read()
  # Parse key manually
  ```

### API Key Masking Issues
- **Issue**: Keys shown as `***` in terminal output
- **Fix**: Use `${VAR:0:10}` syntax to show first 10 chars for verification
- **Example**: `echo ${ELEVENLABS_API_KEY:0:10}` shows `sk_11f9555`

## Quick Commands

```bash
# Run full pipeline
python3 /root/.hermes/skills/business/youtube-finance/scripts/master_pipeline.py

# Generate single video
python3 master_pipeline.py "Topic Name" "https://source-url.com"

# Research only
python3 /root/.hermes/skills/business/youtube-finance/scripts/research_bot.py

# Generate script only
python3 /root/.hermes/skills/business/youtube-finance/scripts/script_generator.py

# Generate voiceover only
python3 /root/.hermes/skills/business/youtube-finance/scripts/voiceover_generator.py script.txt
```

## Related Skills
- **video**: AI video generation tools and techniques
- **content-strategy**: Planning what content to create
- **copywriting**: Writing video scripts and descriptions
- **social**: Social media distribution
