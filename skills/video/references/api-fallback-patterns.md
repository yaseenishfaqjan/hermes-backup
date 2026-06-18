# API Fallback Patterns for Video Production

When image generation and avatar APIs fail, use these fallback patterns.

## Failure Scenarios & Fallbacks

### 1. OpenAI Image Generation (DALL-E / GPT-Image) — Billing Limit

**Symptom:** `billing_hard_limit_reached` error
**Fix:** Switch to PIL + ffmpeg approach. Do not retry — the account needs billing resolution.

### 2. Higgsfield Auth — Hanging / Timeout

**Symptom:** `higgsfield auth login` hangs indefinitely in headless environments
**Fix:** 
1. Kill the process after 15s timeout
2. Try browser-based auth at https://higgsfield.ai → copy token
3. If still failing, use HeyGen avatar API or PIL static avatar

### 3. Hyperframes — MODULE_NOT_FOUND

**Symptom:** `import { render } from "hyperframes"` fails despite npm install
**Fix:** Use PIL + ffmpeg fallback. The hyperframes CLI may work even when the module import fails:
```bash
npx hyperframes render --frames frames.json --output out.mp4
```

### 4. ElevenLabs Voiceover — 401/422 Errors

**Symptom:** API key invalid or voice ID not found
**Fix:** 
- Check key in `/root/.hermes/.env` (not `/root/.env`)
- Verify voice ID at https://elevenlabs.io/voice-library
- Use a different voice ID from the library

### 5. image_generate Tool — Auth Required

**Symptom:** `No Codex/ChatGPT OAuth credentials available`
**Fix:** Run `hermes auth codex` or use PIL fallback. The built-in image_generate tool requires Codex OAuth.

## PIL + ffmpeg Quick Start

```python
from PIL import Image, ImageDraw, ImageFont
import os

# Setup
WIDTH, HEIGHT = 1920, 1080
FPS = 30

# Colors
DARK = (10, 10, 15)
NAVY = (15, 23, 42)
WHITE = (255, 255, 255)
GRAY = (148, 163, 184)

# Create gradient background
img = Image.new('RGB', (WIDTH, HEIGHT), DARK)
draw = ImageDraw.Draw(img)
for y in range(HEIGHT):
    ratio = y / HEIGHT
    r = int(DARK[0] * (1 - ratio) + NAVY[0] * ratio)
    g = int(DARK[1] * (1 - ratio) + NAVY[1] * ratio)
    b = int(DARK[2] * (1 - ratio) + NAVY[2] * ratio)
    draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

# Add text
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
draw.text((WIDTH//2, HEIGHT//2), "Headline", font=font, fill=WHITE, anchor="mm")

# Save frame
img.save("frame_00001.png")
```

Assemble with ffmpeg:
```bash
ffmpeg -framerate 30 -i frame_%05d.png -i audio.mp3 \
  -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest output.mp4
```

## API Key Locations

| Service | Key Location | Env Var |
|---------|-------------|---------|
| ElevenLabs | `/root/.hermes/.env` | `ELEVENLABS_API_KEY` |
| OpenAI | `/root/.hermes/.env` | `OPENAI_API_KEY` |
| HeyGen | `/root/.hermes/.env` | `HEYGEN_API_KEY` |
| Higgsfield | `/root/.hermes/.env` | `HIGGSFIELD_API_KEY` |
| Zernio | `/root/.hermes/.env` | `ZERNIO_API_KEY` |

**Note:** Keys are NOT in `/root/.env` — always check `/root/.hermes/.env` first.

## Avatar Placement Pattern

When using a user's photo as a static avatar in PIL frames:

```python
# Circular crop + border
avatar = Image.open(avatar_path).convert("RGBA")
avatar = avatar.resize((250, 250))
mask = Image.new('L', (250, 250), 0)
ImageDraw.Draw(mask).ellipse([0, 0, 250, 250], fill=255)
img.paste(avatar, (x, y), mask)
# Add colored border
draw.ellipse([x-5, y-5, x+255, y+255], outline=(124, 58, 237), width=4)
```
