# Higgsfield CLI Integration Guide

## Overview
Higgsfield provides both a web UI and CLI for image/video generation. The API (`api.higgsfield.ai`) may return 522 errors, but the CLI works reliably.

## Installation

```bash
curl -fsSL https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh | sh
```

Verify:
```bash
higgsfield --version  # Should show v0.2.1 or higher
```

## Authentication

### Method 1: Browser Login (Recommended)
```bash
higgsfield auth login
```
- Opens browser for OAuth
- If headless, visit the URL shown (e.g., `https://higgsfield.ai/device?code=XXXX`)
- Approve in browser
- Returns to CLI automatically

### Method 2: Using API Key
The CLI does NOT support `--api-key` flag directly. Use device login instead.

## Image Generation

### Generate Thumbnail
```bash
higgsfield generate create nano_banana_2 \
  --prompt "Dark dramatic YouTube thumbnail, oil tanker in Strait of Hormuz, bold red text OIL SHOCK, cinematic lighting, professional news channel style, dark navy background, high contrast" \
  --aspect_ratio 16:9 \
  --resolution 2k \
  --wait
```

### Available Models
- `nano_banana_2` - Fast, good for thumbnails
- `nano_banana_pro` - Higher quality
- `flux` - Alternative style
- `kling_o1` - Video generation

### Parameters
- `--prompt`: Image description (required)
- `--aspect_ratio`: 16:9, 9:16, 1:1, 4:3
- `--resolution`: 1k, 2k, 4k
- `--wait`: Block until generation completes
- `--output`: Save path (optional)

## Common Issues

### 522 Connection Timeout
- **Cause**: API server overload
- **Fix**: Use CLI instead of direct API calls
- **Retry**: Wait 5 minutes and retry

### Authentication Expired
- **Symptom**: "Unauthorized" errors
- **Fix**: `higgsfield auth login` to refresh token

### CLI vs API Confusion
- **HyperFrames** (`hyperframes` command): Video composition tool, NOT image generation
- **Higgsfield** (`higgsfield` command): Image/video generation
- **Never** use HyperFrames for thumbnails

## Browser Automation Fallback

If CLI fails, use browser automation:
1. Navigate to https://higgsfield.ai/image
2. Enter prompt in text box
3. Click Generate
4. Download result

## Integration with Pipeline

Update `scripts/thumbnail_generator.py` to use CLI:
```python
import subprocess

def generate_thumbnail(prompt, output_path):
    cmd = [
        'higgsfield', 'generate', 'create', 'nano_banana_2',
        '--prompt', prompt,
        '--aspect_ratio', '16:9',
        '--resolution', '2k',
        '--wait'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    # Parse output for image URL or path
    return result.stdout
```

## Account Info
- **Username**: vibingswan1270
- **Plan**: Ultra Plan
- **Credits**: 2,658 remaining
- **Website**: https://higgsfield.ai
