#!/usr/bin/env python3
"""
Global Signal Research Bot — Morning research automation
Fetches top stories, scores virality, outputs 3 winning topics
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import openai

# APIs
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

class ResearchBot:
    def __init__(self):
        self.topics = []
        self.virality_scores = {}
        
    def fetch_news(self) -> List[Dict]:
        """Fetch top finance/geopolitics news"""
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": "geopolitics OR economics OR 'market crash' OR 'federal reserve' OR 'inflation' OR 'china economy' OR 'oil prices'",
            "from": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
            "sortBy": "popularity",
            "language": "en",
            "apiKey": NEWS_API_KEY
        }
        try:
            r = requests.get(url, params=params, timeout=30)
            return r.json().get("articles", [])
        except Exception as e:
            print(f"News API error: {e}")
            return []
    
    def fetch_reddit(self) -> List[Dict]:
        """Fetch trending posts from r/geopolitics and r/economics"""
        subreddits = ["geopolitics", "economics", "wallstreetbets", "finance"]
        posts = []
        for sub in subreddits:
            url = f"https://www.reddit.com/r/{sub}/hot.json"
            headers = {"User-Agent": "GlobalSignalBot/1.0"}
            try:
                r = requests.get(url, headers=headers, timeout=15)
                if r.status_code == 200:
                    posts.extend(r.json()["data"]["children"])
            except Exception as e:
                print(f"Reddit error for r/{sub}: {e}")
        return posts
    
    def score_virality(self, title: str, engagement: int) -> float:
        """Score topic by potential YouTube performance"""
        if not OPENAI_KEY:
            return 50.0
            
        prompt = f"""
        Score this YouTube video title 0-100 for virality in the
        geopolitics/economics niche. Consider: controversy, timeliness,
        search volume, and emotional trigger potential.
        
        Title: "{title}"
        
        Return ONLY a number 0-100.
        """
        
        try:
            client = openai.OpenAI(api_key=OPENAI_KEY)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10
            )
            return float(response.choices[0].message.content.strip())
        except:
            return 50.0
    
    def select_top_3(self, all_topics: List[Dict]) -> List[Dict]:
        """Select top 3 topics for the day"""
        scored = []
        for topic in all_topics[:20]:
            score = self.score_virality(topic["title"], topic.get("engagement", 0))
            scored.append({**topic, "virality_score": score})
        
        scored.sort(key=lambda x: x["virality_score"], reverse=True)
        return scored[:3]
    
    def run(self):
        """Execute full research cycle"""
        print("🔍 Global Signal Research Bot Starting...")
        
        news = self.fetch_news()
        reddit = self.fetch_reddit()
        
        all_topics = []
        
        for article in news[:10]:
            all_topics.append({
                "title": article["title"],
                "source": article.get("source", {}).get("name", "Unknown"),
                "url": article["url"],
                "engagement": article.get("popularity", 0)
            })
        
        for post in reddit[:10]:
            data = post["data"]
            all_topics.append({
                "title": data["title"],
                "source": f"reddit.com/r/{data['subreddit']}",
                "url": f"https://reddit.com{data['permalink']}",
                "engagement": data["score"]
            })
        
        top_3 = self.select_top_3(all_topics)
        
        # Save to content calendar
        os.makedirs("/root/youtube_pipeline/content_calendar", exist_ok=True)
        calendar_entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "videos": top_3,
            "generated_at": datetime.now().isoformat()
        }
        
        with open(f"/root/youtube_pipeline/content_calendar/{datetime.now().strftime('%Y-%m-%d')}.json", "w") as f:
            json.dump(calendar_entry, f, indent=2)
        
        print(f"✅ Selected 3 topics for today:")
        for i, topic in enumerate(top_3, 1):
            print(f"  {i}. [{topic['virality_score']:.0f}/100] {topic['title']}")
        
        return top_3

if __name__ == "__main__":
    bot = ResearchBot()
    bot.run()
