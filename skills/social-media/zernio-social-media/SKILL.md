---
name: zernio-social-media
description: Auto-post to Instagram, TikTok, Facebook, LinkedIn, and Twitter using the Zernio API with a single call. Supports text posts, image posts, and video posts with scheduling.
trigger: 
  - "post to social media"
  - "zernio"
  - "auto post"
  - "social media marketing"
  - "schedule post"
  - "instagram post"
  - "tiktok post"
  - "facebook post"
  - "linkedin post"
  - "twitter post"
---

# Zernio Social Media Auto-Posting Skill

Post to Instagram, TikTok, Facebook, LinkedIn, and Twitter simultaneously using the Zernio API.

## Prerequisites

- `ZERNIO_API_KEY` environment variable set in `.env` file or shell
- Media files (images/videos) available at absolute paths

## Quick Start

### 1. Post Text Only
```bash
curl -X POST https://zernio.com/api/v1/posts \
  -H "Authorization: Bearer $ZERNIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["instagram", "tiktok", "facebook", "linkedin", "twitter"],
    "content": "Your post text here",
    "schedule": false
  }'
```

### 2. Post with Image
```bash
curl -X POST https://zernio.com/api/v1/posts \
  -H "Authorization: Bearer $ZERNIO_API_KEY" \
  -H "Content-Type: multipart/form-data" \
  -F "media=@/path/to/image.jpg" \
  -F "platforms=[\"instagram\",\"facebook\",\"linkedin\"]" \
  -F "content=Check out our new product!" \
  -F "schedule=false"
```

### 3. Post with Video
```bash
curl -X POST https://zernio.com/api/v1/posts \
  -H "Authorization: Bearer $ZERNIO_API_KEY" \
  -H "Content-Type: multipart/form-data" \
  -F "media=@/path/to/video.mp4" \
  -F "platforms=[\"instagram\",\"tiktok\",\"facebook\"]" \
  -F "content=Watch our latest video!" \
  -F "schedule=false"
```

### 4. Schedule a Post
```bash
curl -X POST https://zernio.com/api/v1/posts \
  -H "Authorization: Bearer $ZERNIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["instagram", "facebook"],
    "content": "Scheduled post content",
    "schedule": true,
    "schedule_time": "2026-06-20T14:00:00Z"
  }'
```

## Python Script Template

```python
import os
import requests
from pathlib import Path

API_KEY = os.getenv("ZERNIO_API_KEY")
BASE_URL = "https://zernio.com/api/v1"

def post_to_all_platforms(content, media_path=None, schedule_time=None):
    """Post to all supported platforms"""
    
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    platforms = ["instagram", "tiktok", "facebook", "linkedin", "twitter"]
    
    if media_path and Path(media_path).exists():
        # Post with media
        with open(media_path, 'rb') as f:
            files = {'media': f}
            data = {
                'platforms': str(platforms),
                'content': content,
                'schedule': 'false'
            }
            if schedule_time:
                data['schedule'] = 'true'
                data['schedule_time'] = schedule_time
            
            response = requests.post(
                f"{BASE_URL}/posts",
                headers=headers,
                files=files,
                data=data
            )
    else:
        # Text only post
        payload = {
            "platforms": platforms,
            "content": content,
            "schedule": False
        }
        if schedule_time:
            payload["schedule"] = True
            payload["schedule_time"] = schedule_time
        
        headers["Content-Type"] = "application/json"
        response = requests.post(
            f"{BASE_URL}/posts",
            headers=headers,
            json=payload
        )
    
    return response.json()

# Example usage
result = post_to_all_platforms(
    content="🚀 Transform your roofing business with AI automation!",
    media_path="/root/marketing_videos/Scalaro_Marketing_Video.mp4"
)
print(result)
```

## Platform-Specific Tips

### Instagram
- Images: 1080x1080 (square) or 1080x1350 (portrait)
- Videos: MP4, 60 seconds max for feed, 90 seconds for reels
- Captions: Up to 2,200 characters
- Hashtags: 5-10 relevant hashtags

### TikTok
- Videos: MP4, 9:16 aspect ratio, 15-60 seconds
- Captions: Up to 2,200 characters
- Hashtags: 3-5 trending hashtags

### Facebook
- Images: 1200x630 (landscape)
- Videos: MP4, up to 240 minutes
- Captions: Up to 63,206 characters

### LinkedIn
- Images: 1200x627 (landscape)
- Videos: MP4, 3 seconds to 30 minutes
- Captions: Professional tone, up to 3,000 characters

### Twitter/X
- Images: 1200x675 (landscape)
- Videos: MP4, 2 minutes 20 seconds max
- Text: Up to 280 characters

## Error Handling

Common errors and solutions:

```bash
# 401 Unauthorized - Check API key
echo $ZERNIO_API_KEY

# 400 Bad Request - Check media format
file /path/to/media.mp4

# 429 Rate Limit - Wait before retrying
sleep 60
```

## Batch Posting

Post multiple items at once:

```bash
#!/bin/bash
# batch_post.sh

POSTS=(
  "Post 1 content|/path/to/image1.jpg"
  "Post 2 content|/path/to/image2.jpg"
  "Post 3 content|/path/to/video1.mp4"
)

for post in "${POSTS[@]}"; do
  IFS='|' read -r content media <<< "$post"
  
  curl -X POST https://zernio.com/api/v1/posts \
    -H "Authorization: Bearer $ZERNIO_API_KEY" \
    -F "media=@$media" \
    -F "content=$content" \
    -F "platforms=[\"instagram\",\"facebook\"]"
  
  sleep 30  # Rate limiting
done
```

## Analytics

Check post performance:

```bash
curl -X GET https://zernio.com/api/v1/analytics \
  -H "Authorization: Bearer $ZERNIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "post_id": "your_post_id",
    "metrics": ["impressions", "engagement", "clicks", "shares"]
  }'
```

## Cron Job for Daily Posting

Set up automatic daily posts:

```bash
# Add to crontab
crontab -e

# Post every day at 9 AM
0 9 * * * cd /root && python3 /root/scripts/daily_social_post.py >> /root/logs/social_posts.log 2>&1
```

## User Preferences (Learned from Session)

- **Direct execution preferred**: User wants commands run immediately, not explained first
- **Minimal verbosity**: Provide status updates, not lengthy explanations
- **Show file paths**: Always include absolute paths for generated files
- **Progress indicators**: Use simple progress counters (e.g., "[5/20] City Name")

## Best Practices

1. **Content Calendar**: Plan posts 1-2 weeks ahead
2. **Peak Times**: Post at 9-11 AM and 7-9 PM EST
3. **Hashtags**: Research trending hashtags weekly
4. **Engagement**: Respond to comments within 2 hours
5. **Mix Content**: 80% value, 20% promotion
6. **A/B Testing**: Test different headlines and images
7. **Track ROI**: Monitor clicks and conversions
8. **Voice Consistency**: See `references/voice-id-registry.md` for channel voice assignments
