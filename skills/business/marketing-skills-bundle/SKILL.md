---
name: marketing-skills-bundle
description: Complete marketing skills bundle from coreyhaines31/marketingskills. Includes CRO, SEO, copywriting, ads, analytics, email marketing, content strategy, competitor research, and 40+ other marketing skills. Use when user asks about marketing strategy, optimization, campaigns, or any marketing task.
---

# Marketing Skills Bundle

This skill integrates the complete marketing skills repository from https://github.com/coreyhaines31/marketingskills

## Available Skills

### Core Marketing
- **cro** - Conversion Rate Optimization
- **copywriting** - Sales copy and persuasion
- **copy-editing** - Improve existing copy
- **content-strategy** - Content planning and calendars
- **marketing-plan** - Strategic marketing planning
- **marketing-ideas** - Campaign ideation

### Traffic & SEO
- **ai-seo** - AI-powered SEO optimization
- **seo-audit** - Technical SEO audits
- **programmatic-seo** - Scale SEO with templates
- **schema** - Structured data markup
- **site-architecture** - Website structure optimization
- **analytics** - GA4, Mixpanel, Segment

### Advertising
- **ads** - Paid advertising strategy
- **ad-creative** - Ad design and copy
- **ab-testing** - Test and optimize ads

### Email & Communication
- **emails** - Email marketing campaigns
- **cold-email** - Outreach sequences
- **sms** - SMS marketing
- **signup** - Signup flow optimization

### Social Media
- **social** - Social media strategy
- **video** - Video marketing
- **community-marketing** - Community building

### Sales & Revenue
- **sales-enablement** - Sales tools and processes
- **prospecting** - Lead generation
- **referrals** - Referral programs
- **lead-magnets** - Lead capture tools
- **paywalls** - Monetization strategy
- **pricing** - Pricing optimization

### Research & Intelligence
- **competitors** - Competitor analysis
- **competitor-profiling** - Deep competitor research
- **customer-research** - User research
- **churn-prevention** - Retention strategy

### Tools & Integrations
- **tools/clis/** - 51 CLI tools for marketing APIs
- **Composio** - MCP integration for 50+ tools
- **GA4, Stripe, Mailchimp, Resend, Zapier** - Native MCP

## Quick Commands

### Research Competitors
```bash
node /root/marketingskills/tools/clis/ahrefs.js --help
node /root/marketingskills/tools/clis/clearbit.js --help
```

### SEO Analysis
```bash
node /root/marketingskills/tools/clis/dataforseo.js --help
```

### Email Campaigns
```bash
node /root/marketingskills/tools/clis/customer-io.js --help
node /root/marketingskills/tools/clis/brevo.js --help
```

### Social Media
```bash
node /root/marketingskills/tools/clis/buffer.js --help
```

## How to Use

1. **Load specific skill**: `skill_view(name='marketing-skills-bundle')`
2. **View individual skill**: `skill_view(name='cro')` or `skill_view(name='copywriting')`
3. **Run CLI tool**: `node /root/marketingskills/tools/clis/[tool].js [command]`

## Integration with Other Skills

- **youtube-finance** - Use `video` and `content-strategy` skills for YouTube
- **zernio-social-media** - Use `social` skill for social media strategy
- **scalaro** - Use `cro`, `copywriting`, `ads` for roofing business

## Repository Location

Cloned at: `/root/marketingskills/`
Update: `cd /root/marketingskills && git pull`
