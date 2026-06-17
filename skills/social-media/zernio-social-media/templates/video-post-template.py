#!/usr/bin/env python3
"""
Zernio Video Post Template
Standard template for posting marketing videos to all social platforms
"""

import os
import requests
import argparse
from pathlib import Path

ZERNIO_API_KEY = os.environ.get("ZERNIO_API_KEY")
ZERNIO_BASE_URL = "https://zernio.com/api/v1"

def post_video_with_caption(video_path: str, caption: str, platforms: list = None):
    """
    Post a video with caption to multiple social platforms
    
    Args:
        video_path: Path to MP4 video file
        caption: Post text content
        platforms: List of platforms (default: all)
    """
    if not platforms:
        platforms = ["instagram", "tiktok", "facebook", "linkedin", "twitter"]
    
    headers = {
        "Authorization": f"Bearer {ZERNIO_API_KEY}",
        "Content-Type": "multipart/form-data"
    }
    
    # Upload media
    with open(video_path, 'rb') as f:
        files = {'media': f}
        data = {
            'caption': caption,
            'platforms': ','.join(platforms)
        }
        
        response = requests.post(
            f"{ZERNIO_BASE_URL}/posts",
            headers=headers,
            files=files,
            data=data
        )
    
    return response.json()

# Example usage for marketing videos
def post_scalaro_video():
    """Post Scalaro marketing video"""
    video = "/root/marketing_videos/Scalaro_Marketing_Video.mp4"
    caption = """🚀 Transform Your Roofing Business with AI!

Tired of losing leads? Our AI automation helps you:
✅ Capture 10X more leads
✅ Auto-follow up with prospects  
✅ Schedule appointments 24/7
✅ Save 20+ hours per week

💰 ROI: $10K+ guaranteed
👉 Visit scalaro.io

#Roofing #AI #Automation #Contractor #BusinessGrowth"""
    
    return post_video_with_caption(video, caption)

def post_amaan_video():
    """Post Amaan Academy marketing video"""
    video = "/root/marketing_videos/Amaan_Academy_Marketing_Video.mp4"
    caption = """📚 Learn Quran from Anywhere!

✅ 1-on-1 Live Online Classes
✅ Certified Quran Teachers
✅ Flexible Scheduling
✅ Tajweed & Hifz Programs

🌟 First Lesson FREE!
👉 Visit amaanacademy.com

#Quran #IslamicEducation #OnlineLearning #Muslim"""
    
    return post_video_with_caption(video, caption)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, help="Path to video file")
    parser.add_argument("--caption", required=True, help="Post caption")
    parser.add_argument("--platforms", nargs="+", default=["instagram", "facebook", "twitter"])
    args = parser.parse_args()
    
    result = post_video_with_caption(args.video, args.caption, args.platforms)
    print(result)
