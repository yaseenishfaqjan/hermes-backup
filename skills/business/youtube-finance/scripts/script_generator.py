#!/usr/bin/env python3
"""
Global Signal Script Generator
Creates 20-minute YouTube scripts from research topics
"""

import os
import json
import openai
from datetime import datetime

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

SCRIPT_PROMPT = """You are the head writer for "Global Signal," a top-tier YouTube channel covering
geopolitics and economics with a fast-growing, highly engaged audience.

TODAY'S TOPIC: {topic_title}
SOURCE MATERIAL: {source_url}

Create a YouTube script that is EXACTLY 20 minutes when read aloud at 150 WPM.
That means 3,000 words minimum, 3,750 maximum.

STRUCTURE (follow exactly):
1. HOOK (0:00-0:45) — Start with a shocking statistic, bold prediction, or
   contrarian take. Make the viewer NEED to know more.

2. CONTEXT SETUP (0:45-3:00) — What led to this moment? Brief historical
   background. Establish stakes.

3. DEEP DIVE PART 1 (3:00-8:00) — The core story. Facts, figures, quotes.
   Break down complex mechanisms. Use analogies.

4. DEEP DIVE PART 2 (8:00-13:00) — Second angle or opposing view. What are
   the experts saying? What are they MISSING?

5. ANALYSIS & IMPLICATIONS (13:00-17:00) — So what? What happens next?
   30-day outlook, 6-month outlook, 5-year outlook. Be specific with predictions.

6. CONCLUSION & CTA (17:00-20:00) — Summarize key takeaways. Tell viewers
   EXACTLY what to do with this information. Subscribe + notification bell.
   Mention related video.

WRITING RULES:
- Write for SPEAKING, not reading. Short sentences. Conversational but authoritative.
- Use [PAUSE] for dramatic effect.
- Use [EMPHASIS] for key points.
- Use [B-ROLL: description] to note visual needs.
- Include 3 "pattern interrupts" — moments that break the flow to re-engage attention.
- Include 2 rhetorical questions that make viewers nod.
- NEVER say "In conclusion" or "To sum up." Use stronger transitions.
- End every section with a micro-cliffhanger that leads into the next.
- Never use words: "delve", "crucial", "leverage", "utilize"
- Always cite specific numbers: dates, percentages, dollar amounts

OUTPUT FORMAT:
Return ONLY the script text with [TIMESTAMP] markers every 2 minutes.
No markdown, no headers, just the script.
"""

def generate_script(topic: dict, output_dir: str = "/root/youtube_pipeline/scripts"):
    """Generate 20-minute script for a topic"""
    
    if not OPENAI_KEY:
        print("❌ OPENAI_API_KEY not set")
        return None
    
    client = openai.OpenAI(api_key=OPENAI_KEY)
    
    prompt = SCRIPT_PROMPT.format(
        topic_title=topic['title'],
        source_url=topic.get('url', 'No source')
    )
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000,
        temperature=0.7
    )
    
    script = response.choices[0].message.content
    
    # Save script
    os.makedirs(output_dir, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_title = "".join(c if c.isalnum() else "_" for c in topic['title'][:50])
    filename = f"{output_dir}/{date_str}_{safe_title}.txt"
    
    with open(filename, "w") as f:
        f.write(script)
    
    print(f"✅ Script generated: {filename}")
    print(f"   Length: {len(script.split())} words")
    
    return filename

def generate_all_scripts_for_today():
    """Generate scripts for all today's topics"""
    calendar_file = f"/root/youtube_pipeline/content_calendar/{datetime.now().strftime('%Y-%m-%d')}.json"
    
    if not os.path.exists(calendar_file):
        print("❌ No calendar file found. Run research_bot.py first.")
        return []
    
    with open(calendar_file) as f:
        calendar = json.load(f)
    
    generated = []
    for topic in calendar["videos"]:
        filename = generate_script(topic)
        if filename:
            generated.append(filename)
    
    return generated

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Generate for specific topic
        topic = {"title": sys.argv[1], "url": sys.argv[2] if len(sys.argv) > 2 else ""}
        generate_script(topic)
    else:
        # Generate all for today
        generate_all_scripts_for_today()
