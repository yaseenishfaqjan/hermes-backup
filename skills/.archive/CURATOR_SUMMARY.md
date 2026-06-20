## Curator Umbrella-Building Pass — Summary

### Clusters Processed

1. **github-*** (5 skills) → `github` umbrella
   - Merged `github-auth`, `github-code-review`, `github-issues`, `github-pr-workflow` into `github-repo-management` (renamed to `github`)
   - Result: Complete GitHub workflow skill covering auth, repos, PRs, issues, code review, CI/CD

2. **google-maps-*** (2 skills) → `google-maps-lead-generation`
   - Merged `google-maps-lead-scraping` into `google-maps-lead-generation` as extended scraping guide

3. **youtube-*** (3 skills) → `youtube` umbrella (in `media/youtube`)
   - Merged `youtube-automation` and `youtube-content` into `youtube-content-pipeline` (renamed to `youtube`)
   - Result: Full YouTube content pipeline with automation and analysis sections

4. **hermes-*** (2 skills) → `hermes-agent`
   - Merged `hermes-agent-skill-authoring` into `hermes-agent` as skill authoring subsection

5. **ascii-*** (2 skills) → `ascii-art`
   - Merged `ascii-video` into `ascii-art` as video subsection

6. **design/visual** (3 skills) → `claude-design`
   - Merged `architecture-diagram`, `excalidraw`, `sketch` into `claude-design` as diagram and sketch subsections
   - Kept `p5js`, `popular-web-designs`, `design-md`, `baoyu-infographic`, `manim-video`, `video-production-fallback`, `comfyui` as standalone (class-level already)

7. **apple-*** (5 skills) → Archived
   - All macOS-only skills archived: `apple-notes`, `apple-reminders`, `findmy`, `imessage`, `macos-computer-use`

8. **music/audio** (4 skills) → `music-production` umbrella
   - Merged `audiocraft-audio-generation`, `heartmula`, `songsee`, `songwriting-and-ai-music` into `music-production`

9. **dev/debug** (8 skills) → `software-engineering` umbrella
   - Merged `python-debugpy`, `node-inspect-debugger`, `systematic-debugging`, `test-driven-development`, `simplify-code`, `requesting-code-review`, `spike`, `dogfood` into `software-engineering`

10. **mlops** (5 skills) → `mlops-workflows` umbrella
    - Merged `evaluating-llms-harness`, `weights-and-biases`, `llama-cpp`, `serving-llms-vllm` into `mlops-workflows`
    - Kept `huggingface-hub` and `segment-anything-model` standalone (too general/specialized)

11. **ai-agents** (3 skills) → `ai-coding-agents` umbrella
    - Merged `codex`, `claude-code`, `opencode` into `ai-coding-agents`

12. **kanban-*** (2 skills) → `kanban` umbrella
    - Merged `kanban-worker` into `kanban-orchestrator` (renamed to `kanban`)

13. **research** (2 skills) → `research` umbrella
    - Merged `arxiv`, `blogwatcher` into `research`
    - Kept `llm-wiki`, `polymarket`, `research-paper-writing` standalone (distinct domains)

14. **pdf/documents** (2 skills) → `pdf-documents` umbrella
    - Merged `nano-pdf`, `ocr-and-documents` into `pdf-documents`

15. **narrow skills** (4 skills) → Archived
    - `gif-search`, `humanizer`, `pretext`, `touchdesigner-mcp` — too narrow, no class-level value

### Total Archives: 44 skills
### Consolidations: 39 (including 3 renamed variants)
### Prunings: 9

## Structured summary (required)
```yaml
consolidations:
  - from: github-auth
    into: github
    reason: Merged into GitHub workflow umbrella covering auth, repos, PRs, issues, code review, CI/CD
  - from: github-code-review
    into: github
    reason: Merged into GitHub workflow umbrella as code review subsection
  - from: github-issues
    into: github
    reason: Merged into GitHub workflow umbrella as issues subsection
  - from: github-pr-workflow
    into: github
    reason: Merged into GitHub workflow umbrella as PR workflow subsection
  - from: google-maps-lead-scraping
    into: google-maps-lead-generation
    reason: Merged into lead generation umbrella as extended scraping guide subsection
  - from: youtube-automation
    into: youtube
    reason: Merged into YouTube content pipeline umbrella as automation subsection
  - from: youtube-content
    into: youtube
    reason: Merged into YouTube content pipeline umbrella as content analysis subsection
  - from: hermes-agent-skill-authoring
    into: hermes-agent
    reason: Merged into hermes-agent umbrella as skill authoring subsection
  - from: ascii-video
    into: ascii-art
    reason: Merged into ASCII art umbrella as video subsection
  - from: architecture-diagram
    into: claude-design
    reason: Merged into design umbrella as diagram subsection
  - from: excalidraw
    into: claude-design
    reason: Merged into design umbrella as diagram subsection
  - from: sketch
    into: claude-design
    reason: Merged into design umbrella as sketch subsection
  - from: audiocraft-audio-generation
    into: music-production
    reason: Merged into music production umbrella as generation tools subsection
  - from: heartmula
    into: music-production
    reason: Merged into music production umbrella as audio analysis subsection
  - from: songsee
    into: music-production
    reason: Merged into music production umbrella as audio analysis subsection
  - from: songwriting-and-ai-music
    into: music-production
    reason: Merged into music production umbrella as songwriting craft subsection
  - from: python-debugpy
    into: software-engineering
    reason: Merged into software engineering umbrella as Python debugging subsection
  - from: node-inspect-debugger
    into: software-engineering
    reason: Merged into software engineering umbrella as Node.js debugging subsection
  - from: systematic-debugging
    into: software-engineering
    reason: Merged into software engineering umbrella as systematic debugging subsection
  - from: test-driven-development
    into: software-engineering
    reason: Merged into software engineering umbrella as TDD subsection
  - from: simplify-code
    into: software-engineering
    reason: Merged into software engineering umbrella as code simplification subsection
  - from: requesting-code-review
    into: software-engineering
    reason: Merged into software engineering umbrella as code review subsection
  - from: spike
    into: software-engineering
    reason: Merged into software engineering umbrella as spike investigation subsection
  - from: dogfood
    into: software-engineering
    reason: Merged into software engineering umbrella as dogfooding subsection
  - from: evaluating-llms-harness
    into: mlops-workflows
    reason: Merged into MLOps umbrella as LLM evaluation subsection
  - from: weights-and-biases
    into: mlops-workflows
    reason: Merged into MLOps umbrella as experiment tracking subsection
  - from: llama-cpp
    into: mlops-workflows
    reason: Merged into MLOps umbrella as local inference subsection
  - from: serving-llms-vllm
    into: mlops-workflows
    reason: Merged into MLOps umbrella as vLLM serving subsection
  - from: codex
    into: ai-coding-agents
    reason: Merged into AI coding agents umbrella as Codex subsection
  - from: claude-code
    into: ai-coding-agents
    reason: Merged into AI coding agents umbrella as Claude Code subsection
  - from: opencode
    into: ai-coding-agents
    reason: Merged into AI coding agents umbrella as OpenCode subsection
  - from: kanban-worker
    into: kanban
    reason: Merged into kanban umbrella as worker execution subsection
  - from: arxiv
    into: research
    reason: Merged into research umbrella as academic papers subsection
  - from: blogwatcher
    into: research
    reason: Merged into research umbrella as feed monitoring subsection
  - from: nano-pdf
    into: pdf-documents
    reason: Merged into PDF documents umbrella as editing subsection
  - from: ocr-and-documents
    into: pdf-documents
    reason: Merged into PDF documents umbrella as extraction subsection
  - from: audiocraft
    into: music-production
    reason: Renamed variant of audiocraft-audio-generation, merged into music-production
  - from: lm-evaluation-harness
    into: mlops-workflows
    reason: Renamed variant of evaluating-llms-harness, merged into mlops-workflows
  - from: vllm
    into: mlops-workflows
    reason: Renamed variant of serving-llms-vllm, merged into mlops-workflows
prunings:
  - name: apple-notes
    reason: macOS-only skill, unsupported on Linux platform
  - name: apple-reminders
    reason: macOS-only skill, unsupported on Linux platform
  - name: findmy
    reason: macOS-only skill, unsupported on Linux platform
  - name: imessage
    reason: macOS-only skill, unsupported on Linux platform
  - name: macos-computer-use
    reason: macOS-only skill, unsupported on Linux platform
  - name: gif-search
    reason: Too narrow — just GIF search via Tenor, no unique experiential knowledge
  - name: humanizer
    reason: Too narrow — text humanization tool, no class-level instructional value
  - name: pretext
    reason: Too narrow — browser demo tool with minimal usage, no class-level value
  - name: touchdesigner-mcp
    reason: Too narrow — visual programming niche, no class-level instructional value
```