# Global Signal Channel Configuration

## Channel Identity
- **Name:** Global Signal
- **Niche:** Geopolitics + Economic Impact
- **Angle:** World events explained + what they mean for your money
- **Avatar:** Fictional intellectual presenter (never impersonate real people)
- **Language:** English (USA audience)
- **Target Audience:** 25-55 year old Americans interested in world affairs, finance, trading
- **Posting Schedule:** 3 videos/day at 8am, 2pm, 7pm EST
- **Video Length:** 18-25 minutes (main), 45-59 seconds (Shorts)
- **Resolution:** 1920x1080 minimum, 4K preferred

## API Keys Status (as of June 16, 2026)

| API | Status | Key Format | Notes |
|-----|--------|-----------|-------|
| **ElevenLabs** | ✅ WORKING | 51 chars, starts with `sk_11f9` | Voice ID: `auq43ws1oslv0tO4BDa7` (Adam Stone) |
| **Perplexity** | ✅ Connected | Key present | Needs testing |
| **OpenAI** | ✅ Connected | Key present | Optional for scripts |
| **HyperFrames** | ✅ WORKING | v0.6.103 local | No API key needed |
| **Higgsfield** | ❌ DOWN | 67 chars, starts with `hf_e6Y` | Server returning 522 error |
| **Zernio** | ✅ Connected | Key present | For social media posting |
| **HeyGen** | ✅ Connected | Key present | For avatar videos |
| **Firecrawl** | ✅ Connected | Key present | For web scraping |
| **Cloudinary** | ✅ Connected | URL configured | For image optimization |

## Pipeline Scripts Location
```
/root/.hermes/skills/business/youtube-finance/scripts/
├── research_bot.py          # Phase 1: Daily research
├── script_generator.py      # Phase 2: Script writing
├── voiceover_generator.py   # Phase 3: ElevenLabs voice
├── visual_pipeline.py       # Phase 4: Visuals (placeholder)
├── video_assembler.py       # Phase 5: Final assembly
└── master_pipeline.py       # Orchestrates all phases
```

## Output Directories
```
/root/youtube_pipeline/
├── content_calendar/        # JSON topic files
├── scripts/                 # Script files (TXT + JSON)
├── voiceovers/              # MP3 audio files
├── visuals/                 # Images and B-roll clips
├── final_videos/            # Completed MP4 videos
└── assets/                  # Logo, branding materials
```

## ElevenLabs Voice Settings
```json
{
  "voice_id": "auq43ws1oslv0tO4BDa7",
  "voice_name": "Adam Stone - Smooth and Relaxed",
  "voice_category": "professional",
  "model_id": "eleven_turbo_v2_5",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.75
  },
  "speed_wpm": 150
}
```

## Thumbnail Formula (Proven Viral Style)
- **Size:** 1280x720px
- **Background:** Dark (black/dark blue/dark red)
- **Text:** 2-3 words MAX in bold yellow or white, ALL CAPS
- **Elements:** Face + red arrows + flag or map
- **Emotion:** Shock, alarm, urgency

### Example Thumbnail Texts
- "RUSSIA WINS"
- "EU DESTROYED"
- "DOLLAR FALLS"
- "CHINA STRIKES"
- "TRUMP EXPLODES"
- "CRISIS NOW"

## Script JSON Format
```json
{
  "title": "VIDEO TITLE HERE",
  "hook": "Opening statement",
  "sections": [
    {
      "title": "Section Name",
      "content": "Script content...",
      "duration_seconds": 240,
      "visual_cue": "Show map of Russia/chart/image description"
    }
  ],
  "thumbnail_prompt": "Higgsfield image generation prompt",
  "tags": ["geopolitics", "russia", "economy"],
  "target_length_minutes": 20
}
```

## Content Rules
### ✅ DO
- Focus on geopolitics + economic impact
- Use shocking statistics in hooks
- Cite specific numbers and dates
- Connect events to money/markets
- Use fictional avatar (never real people)

### ❌ DON'T
- Impersonate real living people
- Give specific investment advice ("buy X stock")
- Use copyrighted footage without transformation
- Post duplicate content
- Buy fake views

## Competitor Channels to Monitor
- The Rational Perspective
- Military HQ
- George Conway type channels
- Jeffrey Sachs analysis channels

## First 10 Video Topics (Proven Viral Categories)
1. Russia + Europe energy crisis angle
2. China + USA trade war latest
3. Dollar collapse / BRICS alternative
4. Trump + Canada/Mexico trade
5. Middle East + oil prices
6. Ukraine war + economic impact
7. Europe recession warning
8. Gold/crypto + geopolitical hedge
9. China military + Taiwan economic impact
10. Global debt crisis explained

## Monetization Timeline
| Milestone | Target | Timeline |
|-----------|--------|----------|
| 100 subscribers | First week | Days 1-7 |
| 1,000 subscribers | Month 1 | Days 1-30 |
| 4,000 watch hours | Month 2 | Days 30-60 |
| YouTube Partner Program | Month 2-3 | Apply when ready |
| First AdSense payment | Month 3 | $100 threshold |
| $1,000/month | Month 4-5 | Scale content |
| $5,000/month | Month 6-8 | Add sponsorships |
