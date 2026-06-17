#!/usr/bin/env python3
import os, json, requests
from datetime import datetime

PERPLEXITY_KEY = os.getenv("PERPLEXITY_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

def search_perplexity(query):
    headers = {"Authorization": f"Bearer {PERPLEXITY_KEY}", "Content-Type": "application/json"}
    payload = {"model": "sonar", "messages": [{"role": "user", "content": query}], "max_tokens": 1000}
    try:
        r = requests.post("https://api.perplexity.ai/chat/completions", headers=headers, json=payload, timeout=30)
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"

def run():
    print("Global Signal Research Bot")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}\n")
    print("Searching Perplexity for trending topics...\n")
    
    result = search_perplexity("What are the top 3 trending geopolitical news stories today June 16 2026 that would make viral YouTube videos for US audience? For each give: topic, suggested YouTube title with power words, hook sentence, thumbnail text 2-3 words. Focus on Russia, China, Trump, energy, dollar topics.")
    
    print(result)
    
    os.makedirs("/root/youtube_pipeline/content_calendar", exist_ok=True)
    with open(f"/root/youtube_pipeline/content_calendar/{datetime.now().strftime('%Y-%m-%d')}.json", "w") as f:
        json.dump({"date": datetime.now().strftime("%Y-%m-%d"), "research": result}, f, indent=2)
    
    print("\nSaved to content calendar!")

if __name__ == "__main__":
    run()
