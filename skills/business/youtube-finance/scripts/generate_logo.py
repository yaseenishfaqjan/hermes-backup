#!/usr/bin/env python3
"""
Higgsfield Logo Generator for Global Signal
Run this script with your HIGGSFIELD_API_KEY to generate the channel logo
"""

import os
import requests
import json
from pathlib import Path

# Configuration
HIGGSFIELD_API_KEY = os.getenv("HIGGSFIELD_API_KEY", "")
HIGGSFIELD_API_URL = "https://api.higgsfield.ai/v1/generate"

# Logo prompt
LOGO_PROMPT = """Professional YouTube channel logo, dark navy black background, 
glowing blue Earth globe in center with white latitude and longitude grid lines, 
blue wifi/signal waves radiating upward from globe, text GLOBAL SIGNAL in bold white below globe, 
DAILY ANALYSIS in small blue text underneath, cinematic lighting, 4K quality, 
square format 1000x1000px, news channel professional style, no watermark"""

OUTPUT_DIR = "/root/youtube_pipeline/assets"

def generate_logo():
    """Generate channel logo using Higgsfield API"""
    
    if not HIGGSFIELD_API_KEY:
        print("❌ HIGGSFIELD_API_KEY not found in environment")
        print("Please set it: export HIGGSFIELD_API_KEY=your_key_here")
        return False
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f"{OUTPUT_DIR}/global_signal_logo.png"
    
    print("🎨 Generating Global Signal Channel Logo...")
    print(f"Prompt: {LOGO_PROMPT[:100]}...")
    
    headers = {
        "Authorization": f"Bearer {HIGGSFIELD_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": LOGO_PROMPT,
        "width": 1000,
        "height": 1000,
        "num_images": 1,
        "style": "photorealistic",
        "negative_prompt": "watermark, blurry, low quality, cartoon, amateur"
    }
    
    try:
        response = requests.post(
            HIGGSFIELD_API_URL,
            headers=headers,
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Download image
            if "image_url" in data:
                img_url = data["image_url"]
                img_response = requests.get(img_url, timeout=30)
                
                with open(output_path, "wb") as f:
                    f.write(img_response.content)
                
                print(f"✅ Logo saved to: {output_path}")
                print(f"📐 Size: 1000x1000px")
                return True
            else:
                print(f"⚠️ No image URL in response: {data}")
                return False
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    generate_logo()
