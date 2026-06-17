#!/usr/bin/env python3
"""
Global Signal Voiceover Generator
Uses ElevenLabs auq43ws1oslv0tO4BDa7 voice to create professional narration
"""

import os
import requests
import time
from pathlib import Path

ELEVENLABS_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = "auq43ws1oslv0tO4BDa7"  # Global Signal official channel voice - NEVER CHANGE

def generate_voiceover(script_path: str, output_dir: str = "/root/youtube_pipeline/voiceovers"):
    """Generate voiceover from script, chunked for ElevenLabs"""
    
    if not ELEVENLABS_KEY:
        print("❌ ELEVENLABS_API_KEY not set")
        return None
    
    with open(script_path) as f:
        script = f.read()
    
    # Clean script — remove stage directions
    import re
    clean_script = re.sub(r'\[.*?\]', '', script)
    clean_script = re.sub(r'\n+', ' ', clean_script)
    
    # Split into ~4,000 char chunks (sentences intact)
    chunks = []
    current_chunk = ""
    sentences = clean_script.split('. ')
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < 4000:
            current_chunk += sentence + '. '
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + '. '
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    print(f"🎙️ Split script into {len(chunks)} chunks")
    
    # Generate audio for each chunk
    os.makedirs(output_dir, exist_ok=True)
    base_name = Path(script_path).stem
    audio_files = []
    
    for i, chunk in enumerate(chunks):
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_KEY
        }
        
        data = {
            "text": chunk,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.35,
                "similarity_boost": 0.75,
                "style": 0.25,
                "use_speaker_boost": True
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=60)
            
            if response.status_code == 200:
                chunk_file = f"{output_dir}/{base_name}_chunk_{i+1:02d}.mp3"
                with open(chunk_file, "wb") as f:
                    f.write(response.content)
                audio_files.append(chunk_file)
                print(f"  ✅ Chunk {i+1}/{len(chunks)} generated")
            else:
                print(f"  ❌ Chunk {i+1} failed: {response.status_code} - {response.text[:100]}")
        except Exception as e:
            print(f"  ❌ Chunk {i+1} error: {e}")
        
        time.sleep(1)  # Rate limit
    
    if not audio_files:
        print("❌ No audio chunks generated")
        return None
    
    # Concatenate all chunks
    final_audio = f"{output_dir}/{base_name}_full.mp3"
    concat_list = f"{output_dir}/{base_name}_concat.txt"
    
    with open(concat_list, "w") as f:
        for af in audio_files:
            f.write(f"file '{af}'\n")
    
    os.system(f"ffmpeg -y -f concat -safe 0 -i {concat_list} -c copy {final_audio}")
    
    print(f"✅ Full voiceover: {final_audio}")
    return final_audio

def generate_all_voiceovers_for_today():
    """Generate voiceovers for all today's scripts"""
    import glob
    from datetime import datetime
    
    today = datetime.now().strftime("%Y-%m-%d")
    scripts = glob.glob(f"/root/youtube_pipeline/scripts/{today}_*.txt")
    
    if not scripts:
        print("❌ No scripts found for today. Run script_generator.py first.")
        return []
    
    generated = []
    for script in scripts:
        audio = generate_voiceover(script)
        if audio:
            generated.append(audio)
    
    return generated

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        generate_voiceover(sys.argv[1])
    else:
        generate_all_voiceovers_for_today()
