import requests
import json
import time
import csv
import os

API_KEY = "YOUR_API_KEY_HERE"

# Load existing place_ids from previous batches to avoid duplicates
seen_place_ids = set()
for batch_file in ['batch1.csv', 'batch2.csv']:
    try:
        with open(batch_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                seen_place_ids.add(row['place_id'])
        print(f"Loaded place IDs from {batch_file}")
    except:
        pass

print(f"Total existing place IDs: {len(seen_place_ids)}")

# Add your cities here
cities = [
    {"name": "City, ST", "lat": 0.0, "lng": 0.0},
]

keywords = ["roofing", "roof repair", "roof contractor", "roofing company"]

leads = []

def search_places(lat, lng, keyword, pagetoken=None):
    if pagetoken:
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={pagetoken}&key={API_KEY}"
    else:
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=50000&keyword={keyword}&key={API_KEY}"
    try:
        r = requests.get(url, timeout=15)
        return r.json() if r.status_code == 200 else {}
    except:
        return {}

for i, city in enumerate(cities):
    print(f"[{i+1}/{len(cities)}] {city['name']}...")
    
    for keyword in keywords:
        results = search_places(city['lat'], city['lng'], keyword)
        
        if results.get('status') != 'OK':
            continue
        
        for place in results.get('results', []):
            pid = place.get('place_id')
            if pid in seen_place_ids:
                continue
            seen_place_ids.add(pid)
            
            leads.append({
                'place_id': pid,
                'name': place.get('name', ''),
                'address': place.get('vicinity', ''),
                'location': city['name'],
                'rating': place.get('rating', ''),
                'user_ratings_total': place.get('user_ratings_total', ''),
                'business_status': place.get('business_status', ''),
                'types': ','.join(place.get('types', [])),
                'keyword': keyword,
                'lat': place.get('geometry', {}).get('location', {}).get('lat', ''),
                'lng': place.get('geometry', {}).get('location', {}).get('lng', ''),
            })
        
        # Page 2
        next_token = results.get('next_page_token')
        if next_token:
            time.sleep(2)
            results = search_places(city['lat'], city['lng'], keyword, next_token)
            if results.get('status') == 'OK':
                for place in results.get('results', []):
                    pid = place.get('place_id')
                    if pid in seen_place_ids:
                        continue
                    seen_place_ids.add(pid)
                    leads.append({
                        'place_id': pid,
                        'name': place.get('name', ''),
                        'address': place.get('vicinity', ''),
                        'location': city['name'],
                        'rating': place.get('rating', ''),
                        'user_ratings_total': place.get('user_ratings_total', ''),
                        'business_status': place.get('business_status', ''),
                        'types': ','.join(place.get('types', [])),
                        'keyword': keyword,
                        'lat': place.get('geometry', {}).get('location', {}).get('lat', ''),
                        'lng': place.get('geometry', {}).get('location', {}).get('lng', ''),
                    })
        
        time.sleep(0.2)
    time.sleep(0.3)

print(f"\nBatch complete: {len(leads)} new leads")

if leads:
    with open('batch_new.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=leads[0].keys())
        writer.writeheader()
        writer.writerows(leads)
    print("Saved to batch_new.csv")
