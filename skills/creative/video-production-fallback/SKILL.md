---
name: video-production-fallback
description: Fallback video production using PIL/Pillow + FFmpeg when HyperFrames, AI image generation, or other primary tools fail. Produces professional marketing videos with text overlays, screenshots, and avatars.
trigger:
  - "video production failed"
  - "hyperframes not working"
  - "image generation failed"
  - "create video with screenshots"
  - "pil ffmpeg video"
  - "fallback video production"
  - "marketing video without animation"
metadata:
  hermes:
    tags: [video, fallback, pil, ffmpeg, marketing]
    category: creative
    requires_toolsets: [terminal]
---

# Video Production Fallback (PIL + FFmpeg)

When HyperFrames fails (module not found, timeouts, auth issues) and image generation APIs are unavailable (billing limits, auth failures), this fallback produces professional marketing videos using Python PIL/Pillow + FFmpeg.

## When to Use

- HyperFrames `npm install` or `import` fails with MODULE_NOT_FOUND
- HyperFrames render hangs/times out
- OpenAI/DALL-E image generation returns billing limit or auth errors
- Need quick turnaround without complex animation frameworks
- Building B2B SaaS marketing videos with screenshots and text overlays

## Prerequisites

```bash
# Usually pre-installed on Linux
python3 -c "from PIL import Image; print('Pillow OK')"
ffmpeg -version | head -1
```

If Pillow missing: `pip install Pillow`

## Core Technique

### 1. Generate Static Frames with PIL

```python
from PIL import Image, ImageDraw, ImageFont
import os

WIDTH, HEIGHT = 1920, 1080
DARK = (10, 10, 15)
NAVY = (15, 23, 42)
PURPLE = (124, 58, 237)
WHITE = (255, 255, 255)
GRAY = (148, 163, 184)

def create_bg():
    img = Image.new('RGB', (WIDTH, HEIGHT), DARK)
    draw = ImageDraw.Draw(img)
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(DARK[0] * (1 - ratio) + NAVY[0] * ratio)
        g = int(DARK[1] * (1 - ratio) + NAVY[1] * ratio)
        b = int(DARK[2] * (1 - ratio) + NAVY[2] * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
    return img, draw

def get_font(size):
    for fp in ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
               '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf']:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()

def add_text_centered(draw, text, y_offset, font, color, width, shadow=True):
    lines = text.split('\n')
    total_height = sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines)
    total_height += (len(lines) - 1) * 20
    current_y = y_offset - total_height // 2
    for line in lines:
        bbox = font.getbbox(line)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        if shadow:
            draw.text((x+3, current_y+3), line, font=font, fill=(0, 0, 0))
        draw.text((x, current_y), line, font=font, fill=color)
        current_y += text_height + 20
```

### 2. Add Screenshots with Rounded Corners

```python
def add_screenshot(img, screenshot_path, x, y, w, h):
    if not os.path.exists(screenshot_path):
        return
    ss = Image.open(screenshot_path).convert('RGB')
    ss = ss.resize((w, h), Image.Resampling.LANCZOS)
    
    mask = Image.new('L', (w, h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, w, h], radius=20, fill=255)
    
    shadow = Image.new('RGBA', (w+20, h+20), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle([10, 10, w+10, h+10], radius=20, fill=(0, 0, 0, 100))
    img.paste(shadow, (x-10, y-10), shadow)
    
    img.paste(ss, (x, y), mask)
    
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([x, y, x+w, y+h], radius=20, outline=PURPLE, width=3)
```

### 3. Add Circular Avatar with Glow

```python
def add_avatar(img, avatar_path, x, y, size):
    if not os.path.exists(avatar_path):
        return
    av = Image.open(avatar_path).convert('RGBA')
    av = av.resize((size, size), Image.Resampling.LANCZOS)
    
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse([0, 0, size, size], fill=255)
    
    glow = Image.new('RGBA', (size+40, size+40), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([0, 0, size+40, size+40], fill=(124, 58, 237, 80))
    img.paste(glow, (x-20, y-20), glow)
    
    img.paste(av, (x, y), mask)
    
    draw = ImageDraw.Draw(img)
    draw.ellipse([x, y, x+size, y+size], outline=PURPLE, width=4)
```

### 4. Scene Generation Loop

```python
scenes = [
    ('hook', 8),
    ('problem', 10),
    ('show_software1', 12),
    ('cta', 15),
]

frame_count = 0
for scene_name, duration in scenes:
    num_frames = duration * FPS
    for i in range(num_frames):
        frame_num = frame_count + i
        frame_file = f'{frames_dir}/frame_{frame_num:05d}.png'
        
        img, draw = create_bg()
        
        if scene_name == 'hook':
            font = get_font(80)
            add_text_centered(draw, 'A Hailstorm Just Hit', 300, font, WHITE, WIDTH)
            
        elif scene_name == 'show_software1':
            add_screenshot(img, '/path/to/screenshot.png', 200, 150, 1520, 700)
            font = get_font(36)
            add_text_centered(draw, 'Real-Time Storm Intelligence', 900, font, WHITE, WIDTH)
        
        elif scene_name == 'cta':
            add_avatar(img, '/path/to/avatar.png', 200, 300, 300)
            font = get_font(64)
            draw.text((600, 280), 'Stop Losing', font=font, fill=WHITE)
            draw.text((600, 370), 'Storm Jobs', font=font, fill=WHITE)
            sub = get_font(32)
            draw.text((600, 480), 'Book your free demo at scalaro.io', font=sub, fill=CYAN)
        
        img.save(frame_file, 'PNG')
    
    frame_count += num_frames
```

### 5. Assemble with FFmpeg

```bash
# 16:9 version
ffmpeg -y -framerate 30 -i frames/frame_%05d.png -i voiceover.mp3 \
  -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest final_video.mp4

# 9:16 vertical version
ffmpeg -y -i final_video.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,\
  pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:a copy final_vertical.mp4
```

## Performance Tips

- **Lower FPS for static scenes**: Use 10-15 FPS instead of 30 for text-only scenes
- **Batch generation**: For 1800+ frames, script may timeout. Generate in chunks.
- **Font caching**: Load fonts once, reuse across frames
- **Avoid gradients per-frame**: Create background once, paste text/screenshots on top

## Limitations vs HyperFrames

- No GSAP animations (no easing, no stagger, no timelines)
- No shader transitions
- No audio-reactive visuals
- Static text/screenshots only
- But: 100% reliable, zero dependencies, works everywhere

## When to Switch Back to HyperFrames

Use this fallback for quick marketing videos (60-90s). Switch to HyperFrames when:
- Complex animations needed (kinetic typography, motion graphics)
- Audio-reactive or beat-sync visuals
- Multi-scene transitions with effects
- Website-to-video capture pipeline

## Pitfalls

- **ImageMagick not available**: Use PIL instead. `convert` command often missing on Linux servers.
- **Font not found**: Check `/usr/share/fonts/truetype/` for DejaVu or Liberation fonts.
- **Frame generation timeout**: For 1800+ frames at 30 FPS, use 10-15 FPS or split into batches.
- **Memory issues**: Don't hold all frames in memory. Save each frame to disk immediately.

## References

- [scripts/generate_video.py](scripts/generate_video.py) — Complete working example
