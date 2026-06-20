---
name: pdf-documents
description: "PDF document processing: text extraction, OCR, editing, and manipulation."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [pdf, documents, ocr, extraction, editing, text-extraction, productivity]
    related_skills: [powerpoint, research]
---

# PDF Document Processing

Extract, edit, and manipulate PDF documents. Covers text extraction (pymupdf, marker-pdf), OCR for scanned documents, and natural-language editing.

## When to Use

- Extract text from PDFs or scanned documents
- Edit PDF content via natural language instructions
- Split, merge, or search PDFs
- Handle academic papers, reports, or scanned forms

## Decision Map

| Task | Tool | Section |
|------|------|---------|
| Extract text from text-based PDF | pymupdf | § Extraction |
| Extract from scanned PDF / OCR | marker-pdf | § Extraction |
| Edit PDF content | nano-pdf | § Editing |
| Split/merge/search | pymupdf | § Manipulation |

---

## Extraction

### Step 1: Try web_extract for URLs

If the document has a URL, use `web_extract` first:

```
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])
web_extract(urls=["https://example.com/report.pdf"])
```

### Step 2: Choose Local Extractor

| Feature | pymupdf (~25MB) | marker-pdf (~3-5GB) |
|---------|-----------------|---------------------|
| Text-based PDF | ✅ | ✅ |
| Scanned PDF (OCR) | ❌ | ✅ (90+ languages) |
| Tables | ✅ (basic) | ✅ (high accuracy) |
| Equations / LaTeX | ❌ | ✅ |
| Code blocks | ❌ | ✅ |
| Forms | ❌ | ✅ |
| Markdown output | ✅ | ✅ (higher quality) |
| Install size | ~25MB | ~3-5GB |
| Speed | Instant | ~1-14s/page (CPU) |

**Decision**: Use pymupdf unless you need OCR, equations, forms, or complex layout.

### pymupdf (Lightweight)

```bash
pip install pymupdf pymupdf4llm

# Extract text
python scripts/extract_pymupdf.py document.pdf

# Extract markdown
python scripts/extract_pymupdf.py document.pdf --markdown

# Extract tables
python scripts/extract_pymupdf.py document.pdf --tables

# Extract images
python scripts/extract_pymupdf.py document.pdf --images out/

# Specific pages
python scripts/extract_pymupdf.py document.pdf --pages 0-4
```

Inline:
```python
import pymupdf
doc = pymupdf.open('document.pdf')
for page in doc:
    print(page.get_text())
```

### marker-pdf (High-Quality OCR)

```bash
pip install marker-pdf

# Extract markdown
python scripts/extract_marker.py document.pdf

# Scanned PDF with OCR
python scripts/extract_marker.py scanned.pdf

# Batch processing
marker /path/to/folder --workers 4
```

---

## Editing

Edit PDFs using natural-language instructions with nano-pdf.

### Installation

```bash
uv pip install nano-pdf
# or: pip install nano-pdf
```

### Usage

```bash
nano-pdf edit <file.pdf> <page_number> "<instruction>"
```

### Examples

```bash
# Change a title on page 1
nano-pdf edit deck.pdf 1 "Change the title to 'Q3 Results'"

# Fix a typo
nano-pdf edit report.pdf 3 "Update the date from January to February 2026"

# Update content
nano-pdf edit contract.pdf 2 "Change the client name from 'Acme Corp' to 'Acme Industries'"
```

### Notes

- Page numbers may be 0-based or 1-based depending on version — retry with ±1 if wrong page
- Always verify output after editing
- Requires an LLM API key under the hood
- Works well for text changes; complex layout may need different approach

---

## Manipulation

Split, merge, and search PDFs with pymupdf:

```python
# Split: extract pages 1-5
import pymupdf
doc = pymupdf.open("report.pdf")
new = pymupdf.open()
for i in range(5):
    new.insert_pdf(doc, from_page=i, to_page=i)
new.save("pages_1-5.pdf")

# Merge multiple PDFs
result = pymupdf.open()
for path in ["a.pdf", "b.pdf", "c.pdf"]:
    result.insert_pdf(pymupdf.open(path))
result.save("merged.pdf")

# Search for text across all pages
for i, page in enumerate(doc):
    results = page.search_for("revenue")
    if results:
        print(f"Page {i+1}: {len(results)} match(es)")
```

---

## ArXiv Papers

```python
# Abstract (fast)
web_extract(urls=["https://arxiv.org/abs/2402.03300"])

# Full paper
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])
```

---

## Pitfalls

- Always try `web_extract` for URLs before local extraction
- pymupdf cannot OCR scanned documents — use marker-pdf for those
- marker-pdf downloads ~2.5GB of models on first use
- nano-pdf page numbers may be 0-based or 1-based — verify after edit
- For Word docs: use `python-docx` (better than OCR)
- For PowerPoint: see the `powerpoint` skill
