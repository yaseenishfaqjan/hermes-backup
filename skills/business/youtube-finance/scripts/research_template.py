#!/usr/bin/env python3
"""
Manual Research Template for Global Signal
Use this when Perplexity API is not available
"""

def get_trending_topics_manual():
    """
    Template for manual topic research
    Copy this output and fill in with actual research from:
    - YouTube Trending tab
    - Google Trends
    - News websites
    - Twitter/X trending
    """
    
    topics = [
        {
            "rank": 1,
            "topic": "[FILL IN - e.g., Russia cuts gas to Europe]",
            "suggested_title": "[FILL IN - e.g., RUSSIA WINS: Europe's Energy Crisis Explained]",
            "hook": "[FILL IN - e.g., Russia just turned off the gas tap to 3 European countries. Here's what it means for your heating bill this winter...]",
            "search_volume": "[FILL IN - e.g., 500K+ daily searches]",
            "competitor_views": "[FILL IN - e.g., 2.3M views in 48hrs]",
            "source_urls": [
                "https://news-source-1.com/article",
                "https://news-source-2.com/article"
            ]
        },
        {
            "rank": 2,
            "topic": "[FILL IN - e.g., China dumps US Treasury bonds]",
            "suggested_title": "[FILL IN - e.g., CHINA STRIKES: $50B Treasury Dump Shocks Markets]",
            "hook": "[FILL IN - e.g., China just sold $50 billion in US Treasury bonds in a single week. The dollar is shaking, and here's why your savings are at risk...]",
            "search_volume": "[FILL IN]",
            "competitor_views": "[FILL IN]",
            "source_urls": []
        },
        {
            "rank": 3,
            "topic": "[FILL IN - e.g., Trump announces new tariffs]",
            "suggested_title": "[FILL IN - e.g., TRUMP EXPLODES: New Tariffs on 15 Countries]",
            "hook": "[FILL IN - e.g., Trump just announced tariffs on 15 countries effective immediately. Your grocery bill is about to change forever...]",
            "search_volume": "[FILL IN]",
            "competitor_views": "[FILL IN]",
            "source_urls": []
        }
    ]
    
    return topics

def print_research_template():
    """Print formatted research template"""
    print("=" * 70)
    print("🌍 GLOBAL SIGNAL - DAILY TOPIC RESEARCH TEMPLATE")
    print("=" * 70)
    print()
    print("Date: June 16, 2026")
    print("Research Sources: YouTube Trending, Google Trends, News Sites")
    print()
    print("INSTRUCTIONS:")
    print("1. Visit YouTube.com and check Trending tab")
    print("2. Search 'geopolitics news today' on YouTube")
    print("3. Check Google Trends for 'Russia', 'China', 'Trump tariffs'")
    print("4. Visit news sites: Reuters, Bloomberg, Financial Times")
    print("5. Fill in the template below with actual data")
    print()
    print("-" * 70)
    
    topics = get_trending_topics_manual()
    
    for topic in topics:
        print(f"\n🔥 TOPIC #{topic['rank']}")
        print(f"Topic: {topic['topic']}")
        print(f"Suggested Title: {topic['suggested_title']}")
        print(f"Hook: {topic['hook']}")
        print(f"Search Volume: {topic['search_volume']}")
        print(f"Competitor Views: {topic['competitor_views']}")
        print(f"Sources: {', '.join(topic['source_urls']) if topic['source_urls'] else 'To be filled'}")
    
    print("\n" + "=" * 70)
    print("NEXT STEPS:")
    print("1. Fill in all [FILL IN] sections above")
    print("2. Pick the best topic (highest search volume + competitor views)")
    print("3. Run: python3 script_generator.py")
    print("4. Run: python3 generate_voiceover.py script.txt")
    print("=" * 70)

if __name__ == "__main__":
    print_research_template()
