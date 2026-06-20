#!/usr/bin/env python3
"""
Global Signal Video Production Pipeline Template
Copy and modify this template for each video production run.
"""

import os
import sys
import json
from datetime import datetime

# Configuration
CHANNEL_NAME = "Global Signal"
VOICE_ID = "auq43ws1oslv0tO4BDa7"  # Adam Stone
ELEVENLABS_MODEL = "eleven_turbo_v2_5"

# Video Settings
VIDEO_LENGTH_MINUTES = 20
TARGET_WORD_COUNT = 3000  # 150 WPM * 20 minutes
SPEAKING_WPM = 150

# Directory Paths (adjust as needed)
PIPELINE_DIR = "/root/youtube_pipeline"
CONTENT_CALENDAR_DIR = f"{PIPELINE_DIR}/content_calendar"
SCRIPTS_DIR = f"{PIPELINE_DIR}/scripts"
VOICEOVERS_DIR = f"{PIPELINE_DIR}/voiceovers"
VISUALS_DIR = f"{PIPELINE_DIR}/visuals"
FINAL_VIDEOS_DIR = f"{PIPELINE_DIR}/final_videos"
ASSETS_DIR = f"{PIPELINE_DIR}/assets"

def create_topic_json(topic_name: str, source_url: str = ""):
    """Create a topic entry for content calendar"""
    topic = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "topic": topic_name,
        "source_url": source_url,
        "status": "pending",
        "priority": "high",
        "estimated_views": "100K+"
    }
    
    filename = f"{CONTENT_CALENDAR_DIR}/{datetime.now().strftime('%Y-%m-%d')}_{topic_name.replace(' ', '_')}.json"
    with open(filename, 'w') as f:
        json.dump(topic, f, indent=2)
    
    print(f"✅ Topic saved: {filename}")
    return filename

def generate_script_template(topic: str) -> dict:
    """Generate script structure template"""
    script = {
        "title": f"BREAKING: {topic} — What This Means for YOUR Money",
        "hook": f"What just happened with {topic} could change everything you know about global markets...",
        "tease": "By the end of this analysis, you will understand exactly why this matters and what smart money is doing right now.",
        "sections": [
            {
                "title": "Introduction",
                "content": "",  # Fill with research
                "duration_seconds": 120,
                "visual_cue": "Show world map with highlighted regions"
            },
            {
                "title": "What Just Happened",
                "content": "",  # Fill with facts
                "duration_seconds": 300,
                "visual_cue": "Show news footage style graphics"
            },
            {
                "title": "The Economic Impact",
                "content": "",  # Connect to money
                "duration_seconds": 600,
                "visual_cue": "Show charts, stock market data, oil prices"
            },
            {
                "title": "What Smart Money Is Doing",
                "content": "",  # Investment implications
                "duration_seconds": 300,
                "visual_cue": "Show investment flows, gold prices, crypto"
            },
            {
                "title": "Conclusion",
                "content": "",  # Summary and CTA
                "duration_seconds": 180,
                "visual_cue": "Channel logo, subscribe animation"
            }
        ],
        "thumbnail_prompt": f"Dark dramatic background, {topic} headline, red arrows, world map, cinematic lighting, 1280x720",
        "tags": ["geopolitics", "economy", "globalfinance", "news"],
        "target_length_minutes": VIDEO_LENGTH_MINUTES
    }
    
    return script

def save_script(script: dict, filename: str):
    """Save script to file"""
    filepath = f"{SCRIPTS_DIR}/{filename}.json"
    with open(filepath, 'w') as f:
        json.dump(script, f, indent=2)
    
    # Also save as text for voiceover
    text_filepath = f"{SCRIPTS_DIR}/{filename}.txt"
    with open(text_filepath, 'w') as f:
        f.write(f"{script['title']}\n\n")
        f.write(f"{script['hook']}\n\n")
        f.write(f"{script['tease']}\n\n")
        for section in script['sections']:
            f.write(f"{section['title']}\n")
            f.write(f"{section['content']}\n\n")
    
    print(f"✅ Script saved: {filepath}")
    return filepath

def generate_voiceover(script_path: str) -> str:
    """Generate voiceover using ElevenLabs"""
    import requests
    
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        print("❌ ELEVENLABS_API_KEY not set")
        return None
    
    # Read script text
    with open(script_path, 'r') as f:
        text = f.read()
    
    # API call
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    data = {
        "text": text,
        "model_id": ELEVENLABS_MODEL,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        headers=headers,
        json=data,
        timeout=60
    )
    
    if response.status_code == 200:
        output_path = f"{VOICEOVERS_DIR}/{os.path.basename(script_path).replace('.txt', '.mp3')}"
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"✅ Voiceover saved: {output_path}")
        return output_path
    else:
        print(f"❌ Voiceover failed: {response.status_code}")
        return None

# Example usage
if __name__ == "__main__":
    # Create directories
    for d in [CONTENT_CALENDAR_DIR, SCRIPTS_DIR, VOICEOVERS_DIR, VISUALS_DIR, FINAL_VIDEOS_DIR, ASSETS_DIR]:
        os.makedirs(d, exist_ok=True)
    
    # Example: Create topic
    topic = "Trump Iran Deal Oil Shock"
    create_topic_json(topic, "https://news-source.com/article")
    
    # Generate script template
    script = generate_script_template(topic)
    save_script(script, f"{datetime.now().strftime('%Y-%m-%d')}_{topic.replace(' ', '_')}")
    
    print("\n✅ Pipeline template initialized!")
    print("Next steps:")
    print("1. Fill in script content with research")
    print("2. Generate voiceover with generate_voiceover()")
    print("3. Create visuals with HyperFrames")
    print("4. Assemble final video")
