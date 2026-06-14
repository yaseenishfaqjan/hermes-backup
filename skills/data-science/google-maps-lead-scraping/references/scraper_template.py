#!/usr/bin/env python3
"""
Google Maps Lead Scraper Template
Usage: python3 scraper.py
"""

import requests
import csv
import time
import json
import re
from datetime import datetime

# ============ CONFIGURATION ============
API_KEY = "YOUR_GOOGLE_MAPS_API_KEY_HERE"

# Keywords to search for
KEYWORDS = [
    "roofing contractor",
    "roofing company", 
    "roof repair",
    "roof replacement",
    "commercial roofing",
    "residential roofing"
]

# Cities to search (add more as needed)
CITIES = [
    "New York, NY", "Los Angeles, CA", "Chicago, IL", 
    "Houston, TX", "Phoenix, AZ", "Philadelphia, PA"
]

# Output files
OUTPUT_CSV = "leads.csv"
OUTPUT_JSON = "leads.json"
PROGRESS_FILE = "progress.json"

# ============ FUNCTIONS ============

def geocode_city(city):
    """Get lat/lng for a city"""
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": city, "key": API_KEY}
    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        if data.get("results"):
            loc = data["results"][0]["geometry"]["location"]
            return loc["lat"], loc["lng"]
    except Exception as e:
        print(f"  Geocode error for {city}: {e}")
    return None, None

def search_places(lat, lng, keyword, radius=50000):
    """Search Google Places API"""
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "keyword": keyword,
        "key": API_KEY
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        return r.json()
    except Exception as e:
        print(f"  API error: {e}")
        return {}

def get_place_details(place_id):
    """Get detailed info including phone and website"""
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,formatted_address,formatted_phone_number,website,url,types,rating,user_ratings_total",
        "key": API_KEY
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        if data.get("result"):
            return data["result"]
    except Exception as e:
        print(f"  Details error: {e}")
    return {}

def clean_phone(phone):
    """Format phone number to +1-XXX-XXX-XXXX"""
    if not phone:
        return ""
    digits = re.sub(r'\D', '', phone)
    if len(digits) == 10:
        return f"+1-{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits.startswith('1'):
        return f"+1-{digits[1:4]}-{digits[4:7]}-{digits[7:]}"
    return phone

def extract_email_from_website(website):
    """Construct email from website domain"""
    if not website:
        return ""
    try:
        domain = website.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0]
        return f"info@{domain}"
    except:
        return ""

# ============ MAIN SCRAPER ============

def main():
    all_leads = []
    seen_ids = set()
    
    print("=" * 60)
    print("GOOGLE MAPS LEAD SCRAPER")
    print("=" * 60)
    print(f"Cities: {len(CITIES)} | Keywords: {len(KEYWORDS)}")
    print("=" * 60)
    
    city_count = 0
    for city in CITIES:
        city_count += 1
        lat, lng = geocode_city(city)
        if not lat:
            print(f"[{city_count}/{len(CITIES)}] {city} - SKIP (geocode failed)")
            continue
        
        city_leads = 0
        for keyword in KEYWORDS:
            try:
                data = search_places(lat, lng, keyword)
                results = data.get("results", [])
                
                for place in results:
                    pid = place.get("place_id")
                    if not pid or pid in seen_ids:
                        continue
                    seen_ids.add(pid)
                    
                    # Get details
                    details = get_place_details(pid)
                    
                    name = details.get("name", place.get("name", ""))
                    address = details.get("formatted_address", place.get("vicinity", ""))
                    phone = clean_phone(details.get("formatted_phone_number", ""))
                    website = details.get("website", "")
                    maps_url = details.get("url", "")
                    rating = details.get("rating", "")
                    reviews = details.get("user_ratings_total", "")
                    types = ", ".join(details.get("types", place.get("types", [])))
                    email = extract_email_from_website(website)
                    
                    lead = {
                        "Name": name,
                        "Address": address,
                        "Phone": phone,
                        "Email": email,
                        "Website": website,
                        "Google Maps URL": maps_url,
                        "Rating": rating,
                        "Reviews": reviews,
                        "Business Type": types,
                        "Search Keyword": keyword,
                        "City": city,
                        "Scraped Date": datetime.now().strftime("%Y-%m-%d")
                    }
                    all_leads.append(lead)
                    city_leads += 1
                
                time.sleep(0.2)  # Rate limiting
            except Exception as e:
                print(f"  Error with keyword '{keyword}': {e}")
                continue
        
        print(f"[{city_count}/{len(CITIES)}] {city} - {city_leads} leads (Total: {len(all_leads)})")
        
        # Save progress every 10 cities
        if city_count % 10 == 0:
            with open(PROGRESS_FILE, "w") as f:
                json.dump({"total": len(all_leads), "cities_done": city_count}, f)
    
    # Save final results
    print("\n" + "=" * 60)
    print(f"SCRAPING COMPLETE!")
    print(f"TOTAL LEADS FOUND: {len(all_leads)}")
    print("=" * 60)
    
    if all_leads:
        # Save as CSV
        fieldnames = ["Name", "Address", "Phone", "Email", "Website", "Google Maps URL", 
                      "Rating", "Reviews", "Business Type", "Search Keyword", "City", "Scraped Date"]
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_leads)
        
        # Save as JSON
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(all_leads, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved to {OUTPUT_CSV}")
        print(f"✓ Saved to {OUTPUT_JSON}")
    else:
        print("No leads found. Check API key or search parameters.")

if __name__ == "__main__":
    main()
