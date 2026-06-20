---
title: Google Maps Lead Scraping
name: google-maps-lead-scraping
description: Scrape business leads from Google Maps using Places API for sales and marketing outreach
category: data-science
tags: [google-maps, api, scraping, leads, csv, business-intelligence]
version: 1.0
author: hermes
---

# Google Maps Lead Scraping

Scrape business leads from Google Maps using the Places API. Target specific business types, cities, and extract contact information for sales/marketing outreach.

## When to Use

- Need to generate B2B or B2C leads for a specific industry
- Building a prospect database for sales outreach
- Want to find businesses in specific geographic areas
- Need phone numbers, addresses, and websites for cold calling/email campaigns

## Prerequisites

- Google Maps API key with Places API enabled
- Python 3 with `requests` library
- VPS/cloud server for long-running scraping jobs

## API Key Setup

1. Go to https://console.cloud.google.com/
2. Create a project or select existing
3. Enable the **Places API**
4. Create credentials → API Key
5. Restrict the key to Places API only (security best practice)

## Core Workflow

### 1. Search Places (Nearby Search)

```python
import requests
import time

API_KEY="YOUR...ndef search_places(lat, lng, keyword, radius=50000):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "keyword": keyword,
        "key": API_KEY
    }
    r = requests.get(url, params=params, timeout=15)
    return r.json()
```

### 2. Get Place Details

```python
def get_place_details(place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,formatted_address,formatted_phone_number,website,url,types,rating,user_ratings_total",
        "key": API_KEY
    }
    r = requests.get(url, params=params, timeout=10)
    return r.json().get("result", {})
```

### 3. Geocode Cities

```python
def geocode_city(city):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": city, "key": API_KEY}
    r = requests.get(url, params=params, timeout=10)
    data = r.json()
    if data.get("results"):
        loc = data["results"][0]["geometry"]["location"]
        return loc["lat"], loc["lng"]
    return None, None
```

### 4. Phone Number Cleaning

```python
import re

def clean_phone(phone):
    if not phone:
        return ""
    digits = re.sub(r'\D', '', phone)
    if len(digits) == 10:
        return f"+1-{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits.startswith('1'):
        return f"+1-{digits[1:4]}-{digits[4:7]}-{digits[7:]}"
    return phone
```

## Rate Limiting & Performance

- **Google Places API**: ~100 requests per second (with billing enabled)
- **Nearby Search**: Max 60 results per query (3 pages of 20)
- **Sleep between requests**: 0.2-0.3 seconds to avoid rate limits
- **Pagination sleep**: 2 seconds between page tokens

## Lead Estimation Formula

```
Estimated Leads = Cities × Keywords × Average Results per Query
Example: 200 cities × 20 keywords × 5 results = ~20,000 leads
```

## Output Format (CSV)

| Column | Description |
|--------|-------------|
| Name | Business name |
| Address | Full address |
| Phone | Formatted phone number |
| Email | Derived from website domain (info@domain.com) |
| Website | Business website URL |
| Google Maps URL | Direct Google Maps link |
| Rating | Star rating (1-5) |
| Reviews | Number of reviews |
| Business Type | Google Places types |
| Search Keyword | Which keyword found this lead |
| City | City searched |
| Scraped Date | Date of scraping |

## Pitfalls & Lessons Learned

### ❌ Cannot Scrape Individual People
Google Maps API only returns **business listings**, not personal contact info. Cannot get:
- Individual phone numbers
- Personal emails
- Home addresses
- "People who want X" (these are private individuals)

### ✅ What You CAN Get
- Business names and addresses
- Business phone numbers
- Business websites
- Ratings and reviews
- Business categories

### ⚠️ API Costs
- Nearby Search: $17 per 1000 requests (as of 2024)
- Place Details: $17 per 1000 requests
- 10,000 leads ≈ $340 in API costs (20,000 requests)

### ⚠️ Timeout Issues
Scraping thousands of cities takes hours. Always run in **background mode** or use `nohup`:

```bash
nohup python3 scraper.py > output.log 2>&1 &
```

### ⚠️ Duplicate Prevention
Use `place_id` as unique identifier. Maintain a `seen_ids` set to avoid duplicates across keyword searches.

### ⚠️ Geocoding Failures
Some cities may fail to geocode. Skip gracefully and continue.

## Background Execution Strategy

For large scraping jobs (10,000+ leads):

1. **Split into batches** by city groups
2. **Run each batch in background** with `nohup` or `screen`
3. **Save progress** every 10 cities to a JSON file
4. **Merge results** at the end

```bash
# Run in background with logging
nohup python3 scraper.py > scraper_output.log 2>&1 &

# Check progress
tail -f scraper_output.log

# Check progress file
cat progress.json
```

## Keywords Strategy

For **Islamic Education / Quran Learning**:
- "Quran tutoring"
- "Islamic school"
- "Quran classes"
- "Islamic academy"
- "Quran memorization"
- "Hifz program"
- "Islamic education center"
- "Muslim school"
- "Quran learning center"
- "Tajweed classes"

For **Roofing Business**:
- "roofing contractor"
- "roofing company"
- "roof repair"
- "roof replacement"
- "commercial roofing"
- "residential roofing"
- "roofing services"
- "roof inspection"

## City Selection Strategy

Target cities with high concentrations of your target demographic:
- **Islamic education**: Dearborn MI, Paterson NJ, Houston TX, Chicago IL, New York NY
- **Roofing**: Storm-prone areas (Florida, Texas, Midwest), high-growth cities

## Verification Steps

1. Test API key with single city + keyword
2. Verify output CSV has expected columns
3. Check for duplicates in output
4. Validate phone numbers are formatted correctly
5. Confirm website URLs are accessible

## Related Skills
- `github-repo-management` - For backing up lead databases
- `cronjob` - For scheduling daily/weekly scraping updates