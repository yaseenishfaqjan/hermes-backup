---
title: Long-Running API Scraping with Background Processes
name: long-running-api-scraping
description: Handle API scraping jobs that exceed foreground timeouts by using background processes, batch files, and polling strategies.
trigger: |
  When an API scraping job, data collection task, or bulk API operation 
  exceeds 60-300 second timeouts and needs to run in the background with 
  progress monitoring and completion notification.
---

# Long-Running API Scraping with Background Processes

Handle API scraping jobs that take longer than foreground timeouts allow.

## Problem

- `execute_code` times out after 300 seconds (5 minutes)
- `terminal` foreground times out after 60 seconds
- API scraping 100+ cities with rate limits takes 5-30 minutes
- Naive approach: retrying the same timed-out command (loops forever)

## Solution: Background Process Pattern

### Step 1: Write Script to File

```python
# scraper.py
import requests
import time
# ... your scraping logic
```

Use `write_file` to create the script, then run it with `terminal(background=True)`.

### Step 2: Run in Background with Notification

```bash
python3 scraper.py
```

```json
{
  "command": "python3 scraper.py",
  "background": true,
  "notify_on_complete": true
}
```

This returns a `session_id` immediately and notifies when done.

**Alternative for very long jobs (1+ hours):** Use `nohup` with output redirection:

```bash
nohup python3 scraper.py > scraper_output.log 2>&1 &
echo "PID: $!"
```

Then check progress by reading the log file:
```bash
tail -50 scraper_output.log
cat progress.json  # if script saves progress
```

### Step 3: Poll for Progress

```json
{
  "action": "poll",
  "session_id": "proc_xxxxx"
}
```

Poll every 30-60 seconds to check status. The process runs independently.

### Step 4: Wait for Completion (Optional)

```json
{
  "action": "wait",
  "session_id": "proc_xxxxx",
  "timeout": 60
}
```

Note: `wait` is clamped to 60 seconds max. Use `poll` repeatedly for longer waits.

### Step 5: Get Final Output

When `notify_on_complete` fires, the process output is delivered. Or use:

```json
{
  "action": "log",
  "session_id": "proc_xxxxx"
}
```

## Anti-Patterns to Avoid

- **DON'T** retry the same timed-out command unchanged — this creates infinite loops
- **DON'T** use `watch_patterns` for end-of-run markers — use `notify_on_complete` instead
- **DON'T** try to process 100+ API calls in one `execute_code` block — always batch
- **DON'T** forget to save incremental results — if the process crashes, you lose everything

## Best Practices

1. **Save incremental results** — Write CSV after each city or batch, not just at the end
2. **Deduplicate across batches** — Load all previous CSVs before starting a new batch
3. **Use small batches** — 20 cities per script is the sweet spot
4. **Add delays** — Respect API rate limits (2s for Google Places pagination, 0.2s between calls)
5. **Handle errors** — Wrap API calls in try/except and log failures
6. **Track progress** — Print status updates: `[5/20] Chicago, IL... (total leads: 847)`

## Example: Google Places API Scraping

See `scripts/google-places-batch-scraper.py` for a complete working example that:
- Loads existing leads from previous batches
- Processes 20 cities with 4 keywords each
- Handles pagination with 2-second delays
- Saves results to CSV
- Prints progress every city

## When to Use This Pattern

- Any API scraping job expected to take >5 minutes
- Bulk data collection with rate limits
- Multi-step workflows with network delays
- Jobs that must survive disconnections

## When NOT to Use This Pattern

- Simple single API calls (use `execute_code` or `curl`)
- Interactive tasks requiring user input
- Tasks that need real-time output streaming
