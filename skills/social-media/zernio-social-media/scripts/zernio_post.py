#!/usr/bin/env python3
"""
Zernio Social Media Auto-Posting Script
Post to Instagram, TikTok, Facebook, LinkedIn, and Twitter simultaneously
"""

import os
import sys
import requests
import json
from pathlib import Path
from datetime import datetime, timedelta

# Configuration
API_KEY = os.getenv("ZERNIO_API_KEY", "")
BASE_URL = "https://zernio.com/api/v1"

if not API_KEY:
    print("❌ Error: ZERNIO_API_KEY not set in environment")
    print("Set it with: export ZERNIO_API_KEY='your_key_here'")
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}

ALL_PLATFORMS = ["instagram", "tiktok", "facebook", "linkedin", "twitter"]


def post_text(content, platforms=None, schedule_time=None):
    """Post text to social media platforms"""
    if platforms is None:
        platforms = ALL_PLATFORMS
    
    payload = {
        "platforms": platforms,
        "content": content,
        "schedule": False
    }
    
    if schedule_time:
        payload["schedule"] = True
        payload["schedule_time"] = schedule_time
    
    headers = {**HEADERS, "Content-Type": "application/json"}
    
    try:
        response = requests.post(
            f"{BASE_URL}/posts",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error posting text: {e}")
        return {"error": str(e)}


def post_with_media(content, media_path, platforms=None, schedule_time=None):
    """Post with image or video to social media platforms"""
    if platforms is None:
        platforms = ALL_PLATFORMS
    
    media_file = Path(media_path)
    if not media_file.exists():
        print(f"❌ Error: Media file not found: {media_path}")
        return {"error": "File not found"}
    
    headers = HEADERS.copy()  # No Content-Type for multipart
    
    data = {
        'platforms': json.dumps(platforms),
        'content': content,
        'schedule': 'false'
    }
    
    if schedule_time:
        data['schedule'] = 'true'
        data['schedule_time'] = schedule_time
    
    try:
        with open(media_path, 'rb') as f:
            files = {'media': (media_file.name, f, 'application/octet-stream')}
            response = requests.post(
                f"{BASE_URL}/posts",
                headers=headers,
                files=files,
                data=data,
                timeout=60
            )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error posting media: {e}")
        return {"error": str(e)}


def get_analytics(post_id=None, days=7):
    """Get analytics for posts"""
    params = {"days": days}
    if post_id:
        params["post_id"] = post_id
    
    headers = {**HEADERS, "Content-Type": "application/json"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/analytics",
            headers=headers,
            params=params,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting analytics: {e}")
        return {"error": str(e)}


def schedule_posts(posts):
    """Schedule multiple posts
    
    posts: list of dicts with keys:
        - content: str
        - media_path: str (optional)
        - platforms: list (optional)
        - schedule_time: str (ISO format)
    """
    results = []
    
    for post in posts:
        content = post.get("content", "")
        media_path = post.get("media_path")
        platforms = post.get("platforms", ALL_PLATFORMS)
        schedule_time = post.get("schedule_time")
        
        if media_path:
            result = post_with_media(content, media_path, platforms, schedule_time)
        else:
            result = post_text(content, platforms, schedule_time)
        
        results.append(result)
        
        # Rate limiting - wait between posts
        if len(posts) > 1:
            print("⏳ Waiting 30 seconds between posts...")
            import time
            time.sleep(30)
    
    return results


def main():
    """CLI interface for posting"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Zernio Social Media Poster")
    parser.add_argument("--content", "-c", required=True, help="Post content/text")
    parser.add_argument("--media", "-m", help="Path to image or video file")
    parser.add_argument("--platforms", "-p", nargs="+", default=ALL_PLATFORMS,
                       help="Platforms to post to (default: all)")
    parser.add_argument("--schedule", "-s", help="Schedule time (ISO format: 2026-06-20T14:00:00Z)")
    parser.add_argument("--analytics", "-a", help="Get analytics for post ID")
    
    args = parser.parse_args()
    
    if args.analytics:
        result = get_analytics(args.analytics)
        print(json.dumps(result, indent=2))
        return
    
    print(f"🚀 Posting to: {', '.join(args.platforms)}")
    print(f"📝 Content: {args.content[:50]}...")
    
    if args.media:
        print(f"📎 Media: {args.media}")
        result = post_with_media(args.content, args.media, args.platforms, args.schedule)
    else:
        result = post_text(args.content, args.platforms, args.schedule)
    
    if "error" in result:
        print(f"❌ Failed: {result['error']}")
        sys.exit(1)
    else:
        print(f"✅ Success! Post ID: {result.get('post_id', 'N/A')}")
        print(f"📊 Response: {json.dumps(result, indent=2)}")


if __name__ == "__main__":
    main()
