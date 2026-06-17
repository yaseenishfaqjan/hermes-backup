#!/usr/bin/env python3
import os, json, requests, sys
from datetime import datetime

PERPLEXITY_KEY = os.getenv("PERPLEXITY_API_KEY")

def generate_script(topic, keywords=""):
    print(f"Generating script for: {topic}")
    
    prompt = f"""You are a professional YouTube scriptwriter for Global Signal, a geopolitical news channel.

Write a complete 20-minute YouTube video script (2700 words) on this topic:
Title: {topic}
Keywords: {keywords}

STRICT RULES:
- Start with the most shocking fact — NEVER say "In this video"
- Use "you" and "we" — conversational, never academic
- Short sentences under 20 words
- Add [PAUSE] for natural breathing
- Add [B-ROLL: description] for visual cues
- Add "Here's what most people don't realize..." every 3-4 minutes
- Include specific numbers, dates, percentages
- Economic impact section: connect to oil prices, inflation, YOUR money
- End with subscribe CTA

SCRIPT STRUCTURE:
[HOOK 0:00-0:45] Most shocking fact first
[TEASE 0:45-2:00] What viewers will learn
[CONTEXT 2:00-6:00] Background explained simply
[ANALYSIS 6:00-18:00] 4 sections with Fact+Explanation+Impact
[ECONOMIC IMPACT 18:00-22:00] How this affects YOUR money
[CTA 22:00-25:00] Subscribe + next video tease

Write the complete script now. Target exactly 2700 words."""

    headers = {
        "Authorization": f"Bearer {PERPLEXITY_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": "You are an expert YouTube scriptwriter for viral geopolitical news content."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 4000
    }
    
    try:
        r = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        script = r.json()["choices"][0]["message"]["content"]
        
        # Save script
        os.makedirs("/root/youtube_pipeline/scripts", exist_ok=True)
        slug = topic[:50].replace(" ", "_").replace("'", "").replace(":", "")
        filename = f"/root/youtube_pipeline/scripts/{datetime.now().strftime('%Y-%m-%d')}_{slug}.txt"
        
        with open(filename, "w") as f:
            f.write(f"TITLE: {topic}\n")
            f.write(f"DATE: {datetime.now().strftime('%Y-%m-%d')}\n")
            f.write(f"KEYWORDS: {keywords}\n\n")
            f.write(script)
        
        word_count = len(script.split())
        print(f"Script saved: {filename}")
        print(f"Word count: {word_count}")
        return filename
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "Russia Ukraine War Latest Update"
    keywords = sys.argv[2] if len(sys.argv) > 2 else ""
    generate_script(topic, keywords)
