---
name: research
description: "Research discovery and monitoring: academic papers, RSS feeds, and knowledge tracking."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, arxiv, papers, rss, feeds, academic, discovery, monitoring]
    related_skills: [llm-wiki, research-paper-writing, polymarket]
---

# Research Discovery

Discover, monitor, and track academic research and knowledge sources.

## When to Use

- Find academic papers on a topic
- Monitor RSS/Atom feeds for updates
- Track citations and related work
- Build a compounding knowledge base

## Decision Map

| Task | Tool | Section |
|------|------|---------|
| Search academic papers | arXiv API | § Academic Papers |
| Monitor blogs/feeds | Blogwatcher | § Feed Monitoring |
| Build knowledge base | LLM Wiki | See `llm-wiki` skill |
| Write research papers | Pipeline | See `research-paper-writing` skill |
| Prediction market data | Polymarket | See `polymarket` skill |

---

## Academic Papers (arXiv)

Search and retrieve papers from arXiv via their free REST API.

### Quick Reference

| Action | Command |
|--------|---------|
| Search papers | `curl "https://export.arxiv.org/api/query?search_query=all:QUERY&max_results=5"` |
| Get specific paper | `curl "https://export.arxiv.org/api/query?id_list=2402.03300"` |
| Read abstract | `web_extract(urls=["https://arxiv.org/abs/2402.03300"])` |
| Read full paper | `web_extract(urls=["https://arxiv.org/pdf/2402.03300"])` |

### Search Examples

```bash
# Basic search
curl -s "https://export.arxiv.org/api/query?search_query=all:GRPO+reinforcement+learning&max_results=5"

# Clean output with Python
python3 -c "
import sys, xml.etree.ElementTree as ET
ns = {'a': 'http://www.w3.org/2005/Atom'}
root = ET.parse(sys.stdin).getroot()
for entry in root.findall('a:entry', ns):
    title = entry.find('a:title', ns).text.strip().replace('\n', ' ')
    arxiv_id = entry.find('a:id', ns).text.strip().split('/abs/')[-1]
    authors = ', '.join(a.find('a:name', ns).text for a in entry.findall('a:author', ns))
    print(f'{arxiv_id}: {title} by {authors}')
"
```

### Query Syntax

| Prefix | Searches | Example |
|--------|----------|---------|
| `all:` | All fields | `all:transformer+attention` |
| `ti:` | Title | `ti:large+language+models` |
| `au:` | Author | `au:vaswani` |
| `abs:` | Abstract | `abs:reinforcement+learning` |
| `cat:` | Category | `cat:cs.AI` |

### Semantic Scholar (Citations)

```bash
# Get paper details + citations
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:2402.03300?fields=title,authors,citationCount,year,abstract"

# Get who cited it
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:2402.03300/citations?fields=title,authors,year&limit=10"

# Get recommendations
curl -s -X POST "https://api.semanticscholar.org/recommendations/v1/papers/" \
  -H "Content-Type: application/json" \
  -d '{"positivePaperIds": ["arXiv:2402.03300"]}'
```

### Common Categories

| Category | Field |
|----------|-------|
| `cs.AI` | Artificial Intelligence |
| `cs.CL` | Computation and Language (NLP) |
| `cs.CV` | Computer Vision |
| `cs.LG` | Machine Learning |
| `cs.CR` | Cryptography and Security |
| `stat.ML` | Machine Learning (Statistics) |

---

## Feed Monitoring (Blogwatcher)

Track blog and RSS/Atom feed updates.

### Installation

```bash
# Go
go install github.com/JulienTant/blogwatcher-cli/cmd/blogwatcher-cli@latest

# Binary (Linux amd64)
curl -sL https://github.com/JulienTant/blogwatcher-cli/releases/latest/download/blogwatcher-cli_linux_amd64.tar.gz | tar xz -C /usr/local/bin blogwatcher-cli
```

### Common Commands

```bash
# Add a blog
blogwatcher-cli add "My Blog" https://example.com

# Scan all blogs
blogwatcher-cli scan

# List unread articles
blogwatcher-cli articles

# Mark article read
blogwatcher-cli read 1

# Mark all read
blogwatcher-cli read-all
```

### Environment Variables

| Variable | Description |
|---|---|
| `BLOGWATCHER_DB` | Path to SQLite database |
| `BLOGWATCHER_WORKERS` | Concurrent scan workers (default: 8) |
| `BLOGWATCHER_SILENT` | Only output "scan done" |

---

## Complete Research Workflow

1. **Discover**: Search arXiv for papers on your topic
2. **Assess impact**: Check citation counts via Semantic Scholar
3. **Read**: Extract abstracts and PDFs
4. **Monitor**: Add relevant blogs/feeds to Blogwatcher
5. **Track**: Build a knowledge base with `llm-wiki` skill
6. **Write**: Use `research-paper-writing` skill for academic papers

## Rate Limits

| API | Rate | Auth |
|-----|------|------|
| arXiv | ~1 req / 3 seconds | None |
| Semantic Scholar | 1 req / second | None (100/sec with key) |

## Pitfalls

- arXiv returns Atom XML — use Python for clean parsing
- Semantic Scholar fields are double-encoded JSON strings — parse with `json.loads()`
- Blogwatcher database defaults to `~/.blogwatcher-cli/blogwatcher-cli.db`
- arXiv IDs: `arxiv.org/abs/ID` always resolves to latest version; `arxiv.org/abs/IDv1` for specific version
