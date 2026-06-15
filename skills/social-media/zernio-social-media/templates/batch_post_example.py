#!/usr/bin/env python3
"""
Example: Batch post your marketing content to all social media platforms
"""

import sys
import os
sys.path.insert(0, '/root/.hermes/skills/social-media/zernio-social-media/scripts')
from zernio_post import post_with_media, post_text, schedule_posts

# Your marketing content
POSTS = [
    {
        "content": """🚀 Transform Your Roofing Business with AI!

Tired of losing leads? Our AI automation helps you:
✅ Capture 10X more leads
✅ Auto-follow up with prospects
✅ Schedule appointments 24/7
✅ Save 20+ hours per week

💰 ROI: $10K+ guaranteed

👉 Visit scalaro.io to learn more!

#Roofing #AI #Automation #Contractor #BusinessGrowth""",
        "media_path": "/root/marketing_videos/Scalaro_Marketing_Video.mp4",
        "platforms": ["instagram", "tiktok", "facebook", "linkedin"]
    },
    {
        "content": """📚 Learn Quran from Anywhere with Amaan Academy!

Struggling to find quality Quran teachers? We offer:
✅ 1-on-1 Live Online Classes
✅ Certified Quran Teachers
✅ Flexible Scheduling
✅ Tajweed & Hifz Programs

🌟 First Lesson FREE!
No credit card required. Cancel anytime.

👉 Visit amaanacademy.com

#Quran #IslamicEducation #OnlineLearning #Muslim #Tajweed""",
        "media_path": "/root/marketing_videos/Amaan_Academy_Marketing_Video.mp4",
        "platforms": ["instagram", "tiktok", "facebook", "linkedin"]
    },
    {
        "content": """💡 Did you know? 80% of roofing leads are lost due to slow follow-up.

Our AI assistant:
• Responds in under 1 minute
• Qualifies leads automatically
• Books appointments instantly
• Sends reminders

Stop losing money. Start scaling. 🚀

#RoofingContractor #LeadGeneration #BusinessAutomation #AI""",
        "platforms": ["twitter", "linkedin", "facebook"]
    },
    {
        "content": """🌙 Ramadan is coming! 

Prepare your Quran recitation with Amaan Academy:
• Intensive Tajweed courses
• Flexible evening classes
• Family packages available

Enroll now and get 20% off! 🎉

#Ramadan #Quran #IslamicLearning #MuslimFamily""",
        "platforms": ["instagram", "facebook", "twitter"]
    }
]

def main():
    print("🚀 Starting batch social media posting...")
    print(f"📦 Total posts: {len(POSTS)}")
    print("-" * 50)
    
    results = schedule_posts(POSTS)
    
    print("-" * 50)
    print("✅ Batch posting complete!")
    
    # Summary
    success = sum(1 for r in results if "error" not in r)
    failed = len(results) - success
    
    print(f"\n📊 Results:")
    print(f"   ✅ Successful: {success}")
    print(f"   ❌ Failed: {failed}")
    
    if failed > 0:
        print("\n❌ Failed posts:")
        for i, result in enumerate(results):
            if "error" in result:
                print(f"   Post {i+1}: {result['error']}")

if __name__ == "__main__":
    main()
