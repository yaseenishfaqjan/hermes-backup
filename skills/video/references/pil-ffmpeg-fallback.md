# PIL + FFmpeg Fallback for Video Production

When Hyperframes, Remotion, or image generation APIs fail, this approach generates video frames programmatically with Python PIL and assembles them with ffmpeg. Zero external API dependencies.

## When to Use This Fallback

- **Hyperframes npm import fails** — module not found, timeout, or browser issues
- **Image generation APIs down** — OpenAI billing limit, Higgsfield 522, DALL-E unavailable
- **Need fast turnaround** — no time to debug npm/node setup
- **Text-heavy videos** — explainers, product demos, marketing videos with minimal visuals
- **VPS/server environment** — no GUI, no browser, no GPU

## Quick Start

```bash
# 1. Ensure dependencies
python3 -c "from PIL import Image; print('Pillow OK')" || pip install Pillow
ffmpeg -version | head -1 || apt-get install ffmpeg

# 2. Use the boilerplate script
python3 /root/.hermes/skills/youtube-content-pipeline/scripts/pil_frame_generator.py \
    /path/to/script.txt /path/to/output.mp4
```

## Frame Generation Pattern

```python
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1920, 1080
DARK = (10, 10, 15)
NAVY = (15, 23, 42)

def create_gradient_background(width, height, color1, color2):
    img = Image.new("RGB", (width, height), color1)
    draw = ImageDraw.Draw(img)
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return img, draw

def add_text_centered(draw, text, y_offset, font, color, width):
    lines = text.split("\n")
    total_height = sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines)
    total_height += (len(lines) - 1) * 20
    current_y = y_offset - total_height // 2
    for line in lines:
        bbox = font.getbbox(line)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x + 3, current_y + 3), line, font=font, fill=(0, 0, 0))  # shadow
        draw.text((x, current_y), line, font=font, fill=color)
        current_y += text_height + 20
```

## Assembly with FFmpeg

```bash
# With audio
ffmpeg -y -framerate 30 -i frames/frame_%05d.png -i voiceover.mp3 \
    -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest output.mp4

# Without audio (silent video)
ffmpeg -y -framerate 30 -i frames/frame_%05d.png \
    -c:v libx264 -pix_fmt yuv420p -t 60 output.mp4

# Vertical 9:16 from 16:9
ffmpeg -y -i input_16x9.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
    -c:a copy output_9x16.mp4
```

## Performance Tips

- **Lower FPS for static content**: Use 10 FPS instead of 30 for text slides — smaller files, faster generation
- **Batch scene generation**: Generate all frames for one scene, then move to next
- **Disk space**: 1800 frames at 1920x1080 ≈ 50-100MB. Ensure `/tmp` or target dir has space
- **Font paths**: Check `/usr/share/fonts/truetype/` for available fonts. DejaVu and Liberation are common on Linux

## Color Palette Example (GlobalShield Brand)

```python
DARK = (10, 10, 15)
NAVY = (15, 23, 42)
PURPLE = (124, 58, 237)
BLUE = (59, 130, 246)
CYAN = (6, 182, 212)
WHITE = (255, 255, 255)
GRAY = (148, 163, 184)
RED = (239, 68, 68)
```

## Adding an Avatar Photo

```python
from PIL import Image

avatar = Image.open("/path/to/photo.jpg").convert("RGBA")
avatar = avatar.resize((250, 250))

# Circular mask
mask = Image.new("L", (250, 250), 0)
mask_draw = ImageDraw.Draw(mask)
mask_draw.ellipse([0, 0, 250, 250], fill=255)

# Paste onto frame
img.paste(avatar, (x, y), mask)
```

## Thumbnail Generation

Same PIL approach, just different dimensions:

```python
img = Image.new("RGB", (1280, 720), DARK)
draw = ImageDraw.Draw(img)
# ... add text, shapes, etc.
img.save("thumbnail.png", "PNG")
```

## Limitations vs. Full Video Tools

| Feature | PIL+FFmpeg | Hyperframes | Remotion |
|---------|:----------:|:-----------:|:--------:|
| Complex animations | ❌ | ✅ | ✅ |
| CSS transitions | ❌ | ✅ | ✅ |
| AI-generated B-roll | ❌ | ❌ | ❌ |
| Text overlays | ✅ | ✅ | ✅ |
| Gradients/shapes | ✅ | ✅ | ✅ |
| Image embeds | ✅ | ✅ | ✅ |
| No npm/node needed | ✅ | ❌ | ❌ |
| Works offline | ✅ | ❌ | ❌ |
| Fastest to run | ✅ | ⚠️ | ⚠️ |

## See Also

- `youtube-content-pipeline/scripts/pil_frame_generator.py` — full boilerplate with scene system
- `youtube-content-pipeline` skill — end-to-end pipeline with voiceover, scripts, assembly
