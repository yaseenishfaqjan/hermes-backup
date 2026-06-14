---
title: Scalaro Agency Workflow
version: 1.0
name: scalaro-agency-workflow
description: Complete workflow for running an AI automation agency targeting local businesses (roofing, lawn care, golf courses).
category: business
tags: [lead-generation, roofing, automation, sales, outreach]
---

# Scalaro Agency Workflow

## Phase 1: Lead Generation (Google Maps API)

1. **Target cities**: Major US cities + secondary markets
2. **Search keywords**: `roofing`, `roof repair`, `roof contractor`, `roofing company`, `roof replacement`
3. **Radius**: 50km per city
4. **Pagination**: 2 pages per keyword (max 60 results)
5. **Deduplication**: Track `place_id` across all batches
6. **Batch size**: 20-50 cities per batch to avoid timeouts
7. **Rate limits**: 0.2s between requests, 2s for next_page_token

**Output**: CSV with `place_id`, `name`, `address`, `location`, `rating`, `user_ratings_total`, `business_status`, `types`, `keyword`, `lat`, `lng`

## Phase 2: Lead Enrichment

1. **Phone numbers**: Use Google Place Details API (`formatted_phone_number`)
2. **Websites**: Check `website` field in details
3. **Manual score**: 
   - High = no website + <50 reviews
   - Medium = no website
   - Low = has website
4. **Full address**: `formatted_address` from details

## Phase 3: Software Improvements (Codex Workflow)

For each improvement task:
1. Write detailed spec (what, why, how)
2. Delegate to `codex` skill with spec
3. Review generated code
4. Deploy to client site
5. Test and iterate

**Priority order**:
1. Pricing page (3 tiers + enterprise)
2. ROI calculator
3. Fix stats/counters
4. Demo video
5. Case studies
6. Landing pages
7. Email sequences
8. Chat widget
9. Calendar booking
10. Proposal generator

## Phase 4: Outreach System

**Channels**:
- Cold email (100/day)
- LinkedIn automation
- SMS campaigns (90% open rate)
- Retargeting ads

**Tools needed**:
- OpenAI GPT-4 for copywriting
- ElevenLabs for voiceovers
- DALL-E/Midjourney for images
- Runway/Pika for videos
- Canva API for templates

## Phase 5: Content Machine

**Daily output targets**:
- 50 blog posts
- 200 social posts
- 20 marketing videos
- 100 images
- 50 AI avatar videos

## GitHub Backup

1. Create local backup directory
2. `git init`
3. `git remote add origin https://github.com/yaseenishfaqjan/hermes-backup.git`
4. Requires GitHub Personal Access Token with `repo` scope
5. Push all leads, scripts, and generated content

## Key Metrics

- Month 1-2: 10 clients at $2k/month = $20k MRR
- Month 3-4: 25 clients = $50k MRR
- Month 5-6: 50 clients = $100k MRR = $1.2M ARR