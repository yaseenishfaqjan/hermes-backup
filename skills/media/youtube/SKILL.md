---
name: youtube
aliases: [youtube-content-pipeline, youtube-content, youtube-automation]
description: "Complete YouTube content workflow: research, scripting, voiceover, thumbnails, video assembly, and upload automation."
trigger:
  - "create youtube video"
  - "produce youtube content"
  - "youtube automation"
  - "generate video script"
  - "voiceover for video"
  - "youtube thumbnail"
  - "video production pipeline"
  - "batch video production"
  - "youtube transcript"
  - "youtube summary"
  - "youtube content strategy"
---

# YouTube Content Workflow

Complete YouTube content creation from research through upload. Covers end-to-end video production, transcript analysis, and content strategy.

## Pipeline Overview

```
Research → Script → Voiceover → Visuals → Assembly → Upload
     ↑________________________________________________↓
              (Analytics feedback loop)
```

## Part 1: Video Production Pipeline

End-to-end video production for YouTube channels focused on news, geopolitics, finance, and education.

## Pipeline Stages

```
Research → Script → Voiceover → Visuals → Assembly → Upload
```

## Quick Start

### 1. Research Trending Topics
```bash
python3 /root/.hermes/skills/youtube-content-pipeline/scripts/research_bot.py
```

### 2. Generate Script
```bash
python3 /root/.hermes/skills/youtube-content-pipeline/scripts/script_generator.py
```

### 3. Generate Voiceover
```bash
python3 /root/.hermes/skills/youtube-content-pipeline/scripts/voiceover_generator.py /path/to/script.json
```

### 4. Run Full Pipeline
```bash
python3 /root/.hermes/skills/youtube-content-pipeline/scripts/master_pipeline.py
```

## Directory Structure

```
/root/youtube_pipeline/
├── content_calendar/     # Daily topic selections (JSON)
├── scripts/              # Generated scripts (JSON)
├── voiceovers/           # Audio files (MP3)
├── visuals/              # B-roll clips and images
├── final_videos/         # Completed videos (MP4)
└── assets/               # Channel logos, templates
```

## Script Format

Scripts are JSON files with this structure:
```json
{
  "title": "Video Title",
  "hook": "Opening hook sentence",
  "target_length_minutes": 20,
  "sections": [
    {
      "title": "Section Name",
      "start_time": "0:00",
      "end_time": "2:00",
      "content": "Script text...",
      "duration_seconds": 120,
      "visual_cue": "Description of visuals"
    }
  ],
  "thumbnail_prompt": "Image generation prompt",
  "tags": ["tag1", "tag2"],
  "target_audience": "Description"
}
```

## Voiceover Generation

- **Voice ID**: See `references/voice-registry.md` for channel assignments
- **Pacing**: 150 words per minute
- **Chunking**: Scripts >5000 chars are split for API limits
- **Format**: MP3, 44100Hz, mono

## Thumbnail Formula

- **Size**: 1280x720px
- **Background**: Dark (black/navy/dark red)
- **Text**: 2-3 words MAX, bold, uppercase
- **Elements**: Face + red arrows + flag/map
- **Emotion**: Shock, alarm, urgency

## Video Specifications

| Parameter | Value |
|-----------|-------|
| Resolution | 1920x1080 (Full HD) |
| Duration | 18-25 minutes |
| Word Count | 2,700-3,750 |
| Speaking Pace | 150 WPM |
| Background Music | -20db, dramatic |
| Chapters | Every 2-3 minutes |

## Content Rules

✅ **DO**:
- Focus on geopolitics + economic impact
- Use shocking statistics in hooks
- Cite specific numbers and dates
- Connect events to money/markets
- Use fictional avatar (never real people)

❌ **DON'T**:
- Impersonate real living people
- Give specific investment advice
- Use copyrighted footage without transformation
- Post duplicate content
- Buy fake views

## Monetization Timeline

| Milestone | Target | Timeline |
|-----------|--------|----------|
| 100 subscribers | First week | Days 1-7 |
| 1,000 subscribers | Month 1 | Days 1-30 |
| 4,000 watch hours | Month 2 | Days 30-60 |
| YouTube Partner | Month 2-3 | Apply when ready |
| First AdSense | Month 3 | $100 threshold |
| $1,000/month | Month 4-5 | Scale content |
| $5,000/month | Month 6-8 | Add sponsorships |

## User Preferences

- **Direct execution**: Run commands immediately, minimal explanation
- **Progress updates**: Show simple counters [5/20]
- **File paths**: Always show absolute paths
- **Concise output**: Status + file locations, not lengthy descriptions

## Troubleshooting

### Script generation fails
- Check OpenAI API key: `echo $OPENAI_API_KEY`
- Verify disk space: `df -h`
- Check Python packages: `pip list | grep openai`

### Voiceover fails
- Check ElevenLabs API key: `echo $ELEVENLABS_API_KEY`
- Verify voice ID in `references/voice-registry.md`
- Check script length (max 5000 chars per chunk)
- **HTTP 401 Error**: API key is invalid or expired. Generate new key at https://elevenlabs.io/settings/api-keys
- **HTTP 422 Error / Voice ID not found**: The voice ID doesn't exist in the current ElevenLabs account. Common causes:
  - Voice ID is from a different ElevenLabs account (e.g., user's personal account vs the one configured in `.env`)
  - Voice was deleted or expired
  - Voice ID is from HeyGen (different platform) — HeyGen voice IDs are NOT compatible with ElevenLabs API
  - **Fix**: List available voices with `curl https://api.elevenlabs.io/v1/voices -H "xi-api-key: $KEY"` and use one of those IDs
  - **Fallback**: Use a premade voice like `XB0fDUnXU5powFXDhCwa` (male) or `pNInz6obpgDQGcFmaJgB` (Adam - dominant, firm)

### Video assembly fails
- Check ffmpeg: `ffmpeg -version`
- Verify visual assets exist: `ls /root/youtube_pipeline/visuals/`
- Check disk space: `df -h`

### Image generation APIs fail (OpenAI, Higgsfield, etc.)
- **Billing limit reached**: Switch to PIL/Pillow + ffmpeg programmatic approach
- **Auth hanging**: Use `skill_view(name='video')` for Hyperframes/Remotion fallback, or build frames with PIL
- **No image gen available**: Generate frames with Python PIL → ffmpeg assembly. See `scripts/pil_frame_generator.py` for boilerplate
- **Hyperframes module issues**: If `hyperframes` npm import fails, use direct ffmpeg with image sequences instead

### Image generation APIs fail (OpenAI, Higgsfield, etc.)
- **Billing limit reached**: Switch to PIL/Pillow + ffmpeg programmatic approach
- **Auth hanging**: Use `skill_view(name='video')` for Hyperframes/Remotion fallback, or build frames with PIL
- **No image gen available**: Generate frames with Python PIL → ffmpeg assembly. See `scripts/pil_frame_generator.py` for boilerplate
- **Hyperframes module issues**: If `hyperframes` npm import fails, use direct ffmpeg with image sequences instead

### Higgsfield / Thumbnail Generation
- **API 522 Error**: Higgsfield API server is down. Use CLI instead: `higgsfield auth login` then `higgsfield generate create`
- **CLI not authenticated**: Visit `https://higgsfield.ai/device?code=<CODE>` to approve device
- **HyperFrames confusion**: HyperFrames is for VIDEO compositions, not images. Use `higgsfield` CLI for image generation
- **Alternative**: Use browser automation to access https://higgsfield.ai/image directly if CLI fails

## API Keys Required

Add to `.env`:
```bash
OPENAI_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here
ELEVENLABS_VOICE_ID=auq43ws1oslv0tO4BDa7  # Global Signal
HYPERFRAMES_API_KEY=your_key_here
HIGGSFIELD_API_KEY=your_key_here
```

## Part 2: YouTube Content Analysis

Extract transcripts, summarize videos, and repurpose existing YouTube content into threads, blogs, and newsletters.

### Transcript Extraction

```python
from youtube_transcript_api import YouTubeTranscriptApi

# Extract transcript by video ID
video_id = "dQw4w9WgXcQ"  # From URL: youtube.com/watch?v=VIDEO_ID
transcript = YouTubeTranscriptApi.get_transcript(video_id)

# Convert to plain text
full_text = " ".join([entry["text"] for entry in transcript])
```

### Summarization & Repurposing

| Output | Method |
|--------|--------|
| Twitter/X thread | Extract 5-7 key points, each as a tweet |
| Blog post | Expand summary with context and transitions |
| Newsletter | Add personal commentary + links |
| LinkedIn post | Professional tone, 1 key insight |
| Short-form clips | Identify viral moments (30-60s) |

### Content Strategy Tips

- **Batch process**: Extract 10-20 transcripts at once for research
- **Cross-reference**: Compare multiple sources on the same topic
- **Trend detection**: Track recurring themes across channels
- **Gap analysis**: Find topics covered by competitors but not you

## See Also

- `references/voice-registry.md` - Channel voice assignments + ElevenLabs troubleshooting
- `references/higgsfield-cli-guide.md` - Higgsfield CLI setup for thumbnails
- `templates/script-template.json` - Script JSON template
- `scripts/pil_frame_generator.py` - PIL + ffmpeg fallback when image generation APIs fail
- `scripts/research_bot.py` - Topic research automation
- `scripts/script_generator.py` - Script writing
- `scripts/voiceover_generator.py` - Voiceover generation
- `scripts/master_pipeline.py` - Full pipeline orchestration
