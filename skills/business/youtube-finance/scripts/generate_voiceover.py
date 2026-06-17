from elevenlabs import ElevenLabs
import os
import sys

def generate_voiceover(script_path: str, output_path: str = None):
    """
    Generate voiceover using Global Signal official voice
    Voice ID: auq43ws1oslv0tO4BDa7
    """
    
    # Read script
    with open(script_path, 'r', encoding='utf-8') as f:
        script_text = f.read()
    
    # Truncate to first 5000 chars (ElevenLabs limit for single generation)
    text = script_text[:5000]
    
    # Generate with official Global Signal voice
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    
    audio = client.text_to_speech.convert(
        text=text,
        voice_id="auq43ws1oslv0tO4BDa7",  # OFFICIAL GLOBAL SIGNAL VOICE
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128"
    )
    
    # Save
    if not output_path:
        output_path = script_path.replace('.txt', '_voiceover.mp3')
    
    with open(output_path, 'wb') as f:
        for chunk in audio:
            f.write(chunk)
    
    print(f"✅ Voiceover generated: {output_path}")
    print(f"   Voice: auq43ws1oslv0tO4BDa7 (Global Signal Official)")
    print(f"   Duration: ~{len(text.split()) // 150} minutes")
    return output_path

if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_voiceover(sys.argv[1])
    else:
        print("Usage: python3 generate_voiceover.py <script.txt>")
