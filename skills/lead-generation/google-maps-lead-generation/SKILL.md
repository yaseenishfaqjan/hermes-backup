---
title: Google Maps Lead Generation via Places API
name: google-maps-lead-generation
description: Generate targeted business leads by scraping Google Maps using the Google Places API with batch processing, deduplication, and CSV export.
trigger: |
  When the user asks to find business leads, scrape leads from Google Maps, 
  collect business contacts from Google Maps, or build a lead database using 
  Google Maps API for any industry or location.
---

# Google Maps Lead Generation via Places API

Generate targeted business leads by scraping Google Maps using the Google Places API.

## Prerequisites

- Valid Google Maps API key with Places API enabled
- Python 3 with `requests` and `csv` modules

## Workflow

### 1. API Key Handling (CRITICAL)

**Pitfall:** The API key gets corrupted when written into code blocks via `execute_code` or `write_file` because the platform masks it with `***`.

**Solution:** Store the key in a file or environment variable, then read it in the script:

```bash
# Setup: Store key securely
mkdir -p /root/.api_keys
echo "AIza..." > /root/.api_keys/google_maps
chmod 600 /root/.api_keys/google_maps
```

```python
# Read from file (recommended)
with open('/root/.api_keys/google_maps', 'r') as f:
    API_KEY=f.read...n
# Or read from env var
import os
API_KEY=os.env...etup: Test the API Key

```python
import requests
API_KEY=*** = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=40.7128,-74.0060&radius=50000&keyword=roofing&key={API_KEY}"
r = requests.get(url)
print(r.json().get('status'))  # Should print 'OK'
```

### 2. Build City List

Create a list of target cities with lat/lng coordinates. Use major metro areas first, then expand to secondary markets.

```python
cities = [
    {"name": "New York, NY", "lat": 40.7128, "lng": -74.0060},
    {"name": "Los Angeles, CA", "lat": 34.0522, "lng": -118.2437},
    # ... add 50-100 cities
]
```

### 3. Search with Multiple Keywords

Use 4-5 related keywords per city to maximize coverage:

```python
keywords = ["roofing", "roof repair", "roof contractor", "roofing company", "roof replacement"]
```

### 4. Handle Pagination

Each search returns up to 20 results. Use `next_page_token` to get pages 2 and 3 (max 60 results per keyword per city). **Wait 2 seconds between page requests** — Google requires this.

### 5. Deduplicate with Place IDs

Store all `place_id` values in a `set()` to avoid duplicates across keywords and cities.

### 6. Batch Processing Strategy

**Critical for large jobs:** Google Places API calls take time. Process in batches of 20 cities per script to avoid timeouts.

1. Save each batch as a separate CSV file: `batch1.csv`, `batch2.csv`, etc.
2. Load existing `place_id`s from all previous batches before starting the next batch
3. Use `terminal(background=True, notify_on_complete=True)` for long-running scrapes

### 7. Enrich with Details (Optional)

After collecting leads, fetch phone numbers and websites:

```python
def get_details(place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=formatted_phone_number,website,url&key={API_KEY}"
    return requests.get(url).json().get('result', {})
```

## Output Format

Save as CSV with columns:
- `place_id` — unique Google identifier
- `name` — business name
- `address` — street address
- `location` — city searched
- `rating` — Google rating (1-5)
- `user_ratings_total` — number of reviews
- `business_status` — OPERATIONAL or CLOSED_TEMPORARILY
- `types` — business categories
- `keyword` — which search found this lead
- `lat`, `lng` — coordinates

## Expected Yield

- 20-60 leads per city per keyword (with pagination)
- 100-200 unique leads per city across all keywords
- 100 cities × 100 leads = ~10,000 leads

## Pitfalls

- **Timeout on large batches:** Never try to process 100 cities in one script. Use 20-city batches.
- **API key in scripts:** The key gets mangled by the system when writing files. Use `sed` to fix: `sed -i '7s/.*/API_KEY=*** script.py`
- **API key masking in execute_code:** Never write API keys directly in `execute_code` or `write_file` — use file/env var indirection. The platform replaces the key with `***` which corrupts the script syntax.`
- **Missing next_page_token delay:** If you don't wait 2 seconds, Google returns INVALID_REQUEST
- **Duplicate place_ids:** Always deduplicate across batches, not just within a batch
- **OVER_QUERY_LIMIT:** Add a 5-second delay and retry if this status appears

## Scripts

See `scripts/batch_scraper.py` for a complete working template.
