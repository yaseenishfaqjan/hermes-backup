#!/usr/bin/env python3
"""
Higgsfield Image Generator for Global Signal
Generates YouTube channel logo and thumbnails using Higgsfield API
"""

import requests
import os
import sys
from pathlib import Path

# API Configuration
HIGGSFIELD_API_KEY = os.getenv("HIGGSFIELD_API_KEY", "")
HIGGSFIELD_BASE_URL = "https://api.higgsfield.ai/v1"  # Adjust if different

def generate_image(prompt: str, output_path: str, width: int = 1024, height: int = 1024, style: str = "cinematic"):
    """Generate image using Higgsfield API"""
    
    if not HIGGSFIELD_API_KEY:
        print("❌ HIGGSFIELD_API_KEY not set in environment")
        print("Add to .env: HIGGSFIELD_API_KEY=your_key_here")
        return False
    
    headers = {
        "Authorization": f"Bearer {HIGGSFIELD_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "style": style,
        "negative_prompt": "watermark, blurry, low quality, distorted text, amateur",
        "num_images": 1,
        "seed": -1  # Random seed
    }
    
    print(f"🎨 Generating image...")
    print(f"   Prompt: {prompt[:80]}...")
    
    try:
        response = requests.post(
            f"{HIGGSFIELD_BASE_URL}/generate",
            headers=headers,
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Download image
            image_url = data.get("images", [{}])[0].get("url")
            if image_url:
                img_response = requests.get(image_url, timeout=60)
                if img_response.status_code == 200:
                    # Save image
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    with open(output_path, "wb") as f:
                        f.write(img_response.content)
                    
                    size_kb = len(img_response.content) / 1024
                    print(f"✅ Image saved: {output_path}")
                    print(f"   Size: {size_kb:.1f} KB")
                    print(f"   Dimensions: {width}x{height}")
                    return True
            
            print(f"❌ No image URL in response")
            return False
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def generate_channel_logo():
    """Generate Global Signal channel logo"""
    
    prompt = """Professional YouTube channel logo, dark navy black background, 
    glowing blue Earth globe in center with white latitude and longitude grid lines, 
    blue wifi/signal waves radiating upward from globe, 
    text "GLOBAL SIGNAL" in bold white sans-serif font below globe, 
    "DAILY ANALYSIS" in small blue text underneath, 
    cinematic lighting, 4K quality, square format 1000x1000px, 
    news channel professional style, clean modern design, no watermark, 
    high contrast, corporate branding style"""
    
    output_path = "/root/youtube_pipeline/branding/global_signal_logo.png"
    
    return generate_image(prompt, output_path, width=1000, height=1000, style="cinematic")

def generate_thumbnail(topic: str, headline: str, output_name: str = None):
    """Generate viral thumbnail for a video"""
    
    prompt = f"""YouTube thumbnail, dark dramatic background, 
    split image showing {topic} on left with red arrow pointing right, 
    bold text "{headline}" in bright yellow at bottom, 
    cinematic lighting, high contrast, professional news channel style, 
    1280x720 resolution, no watermark, viral style, shocking, alarming"""
    
    if not output_name:
        output_name = f"thumb_{topic.replace(' ', '_').lower()}.png"
    
    output_path = f"/root/youtube_pipeline/thumbnails/{output_name}"
    
    return generate_image(prompt, output_path, width=1280, height=720, style="cinematic")

def generate_banner():
    """Generate YouTube channel banner"""
    
    prompt = """YouTube channel banner, dark navy blue background, 
    world map with glowing connection lines, 
    text "GLOBAL SIGNAL" in large white bold letters center, 
    "Daily Geopolitical & Economic Analysis" in smaller text below, 
    subtle grid pattern, professional news channel style, 
    2560x1440 resolution, cinematic, no watermark"""
    
    output_path = "/root/youtube_pipeline/branding/channel_banner.png"
    
    return generate_image(prompt, output_path, width=2560, height=1440, style="cinematic")

def main():
    """Main function - generate all branding assets"""
    
    print("=" * 60)
    print("🎨 GLOBAL SIGNAL BRANDING GENERATOR")
    print("=" * 60)
    print(f"API Key: {'✅ Set' if HIGGSFIELD_API_KEY else '❌ Missing'}")
    print(f"API URL: {HIGGSFIELD_BASE_URL}")
    print("=" * 60)
    
    # Create directories
    os.makedirs("/root/youtube_pipeline/branding", exist_ok=True)
    os.makedirs("/root/youtube_pipeline/thumbnails", exist_ok=True)
    
    # Generate logo
    print("\n1️⃣ Generating Channel Logo...")
    if generate_channel_logo():
        print("   ✅ Logo complete!")
    else:
        print("   ❌ Logo failed")
    
    # Generate banner
    print("\n2️⃣ Generating Channel Banner...")
    if generate_banner():
        print("   ✅ Banner complete!")
    else:
        print("   ❌ Banner failed")
    
    # Generate sample thumbnail
    print("\n3️⃣ Generating Sample Thumbnail...")
    if generate_thumbnail("Russia flag", "RUSSIA WINS", "sample_thumb.png"):
        print("   ✅ Thumbnail complete!")
    else:
        print("   ❌ Thumbnail failed")
    
    print("\n" + "=" * 60)
    print("✅ BRANDING GENERATION COMPLETE")
    print("=" * 60)
    print("\n📁 Files saved to:")
    print("   /root/youtube_pipeline/branding/")
    print("   /root/youtube_pipeline/thumbnails/")
    print("\n📋 Next Steps:")
    print("   1. Review generated images")
    print("   2. Upload logo to YouTube Studio")
    print("   3. Upload banner to YouTube Studio")
    print("   4. Use thumbnails for videos")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Custom generation
        if sys.argv[1] == "logo":
            generate_channel_logo()
        elif sys.argv[1] == "banner":
            generate_banner()
        elif sys.argv[1] == "thumb" and len(sys.argv) > 3:
            generate_thumbnail(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
        else:
            print("Usage: python3 higgsfield_generator.py [logo|banner|thumb 'topic' 'headline']")
    else:
        main()
