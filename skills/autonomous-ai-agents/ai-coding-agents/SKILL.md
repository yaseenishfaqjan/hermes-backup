---
name: ai-coding-agents
description: "Delegate coding tasks to autonomous AI agent CLIs: Claude Code, OpenAI Codex, and OpenCode."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [coding-agent, autonomous, claude-code, codex, opencode, delegation, pr-review, refactoring]
    related_skills: [hermes-agent, github, software-engineering]
---

# AI Coding Agents

Delegate coding tasks to autonomous AI agent CLIs. Covers Claude Code (Anthropic), Codex (OpenAI), and OpenCode (provider-agnostic).

## When to Use

- Building features or refactoring in existing codebases
- PR reviews and code audits
- Batch issue fixing across multiple worktrees
- Exploratory coding sessions
- Any task where an autonomous agent can work while you monitor

## Decision Map

| Agent | Vendor | Best For | Mode |
|-------|--------|----------|------|
| Claude Code | Anthropic | Multi-turn iterative work, complex reasoning | Print (`-p`) or Interactive (tmux) |
| Codex | OpenAI | One-shot tasks, batch PR reviews | `exec` (one-shot) or Background |
| OpenCode | Open-source / multi-provider | Provider flexibility, open-source preference | `run` (one-shot) or Interactive (TUI) |

---

## Claude Code (Anthropic)

### Installation

```bash
npm install -g @anthropic-ai/claude-code
claude auth login  # or --console for API key, --sso for Enterprise
```

### Print Mode (Preferred for One-Shots)

Non-interactive, exits when done. No PTY needed.

```bash
claude -p 'Add error handling to all API calls in src/' --allowedTools 'Read,Edit' --max-turns 10
```

**Key flags:**
- `-p, --print` — one-shot mode
- `--max-turns N` — limit agentic loops (prevents runaway)
- `--max-budget-usd N` — cost cap
- `--allowedTools <tools>` — whitelist (e.g., `Read,Edit,Bash`)
- `--output-format json` — structured output
- `--json-schema <schema>` — enforce schema
- `--bare` — skip plugins/hooks/MCP for fastest startup
- `--model <alias>` — `sonnet`, `opus`, `haiku`
- `--effort <level>` — `low`, `medium`, `high`, `max`

### Interactive Mode (tmux Required)

For multi-turn iterative work:

```bash
# Start tmux session
tmux new-session -d -s claude-work -x 140 -y 40

# Launch Claude
tmux send-keys -t claude-work 'cd /project && claude' Enter

# Handle trust dialog (first visit only)
sleep 5 && tmux send-keys -t claude-work Enter

# Send task
tmux send-keys -t claude-work 'Refactor auth module to use JWT' Enter

# Monitor
tmux capture-pane -t claude-work -p -S -50

# Exit
tmux send-keys -t claude-work '/exit' Enter
```

**Key interactive commands:**
- `/compact [focus]` — compress context to save tokens
- `/review` — request code review
- `/plan [description]` — enter plan mode
- `/model [model]` — switch models mid-session
- `/effort [level]` — adjust reasoning depth
- `/context` — visualize context usage
- `/cost` — token usage breakdown

### Session Management

```bash
claude -c                              # Continue most recent session
claude -r <session-id>                 # Resume specific session
claude -p 'task' --continue            # Continue in print mode
claude -p 'task' --resume <id> --fork-session  # Fork session
```

### PR Review

```bash
# Quick review (print mode)
git diff main...feature-branch | claude -p 'Review for bugs, security, style issues' --max-turns 1

# From PR number
claude -p 'Review this PR' --from-pr 42 --max-turns 10
```

### Pitfalls

- Interactive mode REQUIRES tmux — `pty=true` alone works but tmux gives `capture-pane` and `send-keys`
- `--dangerously-skip-permissions` dialog defaults to "No, exit" — send Down then Enter
- `--max-budget-usd` minimum is ~$0.05 (cache creation cost)
- Context quality degrades above 70% usage — monitor with `/context`
- Use `--bare` for CI/scripting to skip OAuth and plugin discovery

---

## Codex (OpenAI)

### Installation

```bash
npm install -g @openai/codex
# Auth: codex login (OAuth) or OPENAI_API_KEY env var
```

### One-Shot Tasks

```bash
codex exec 'Add dark mode toggle to settings'
```

**Key flags:**
- `exec "prompt"` — one-shot execution, exits when done
- `--full-auto` — auto-approves file changes in sandbox
- `--yolo` — no sandbox, no approvals (fastest, most dangerous)
- `--sandbox danger-full-access` — no sandbox (for gateway/service contexts)

### Background Mode

```bash
# Start in background
terminal(command="codex exec --full-auto 'Refactor auth module'", workdir="~/project", background=true, pty=true)

# Monitor
process(action="poll", session_id="<id>")
process(action="submit", session_id="<id>", data="yes")  # Answer prompts
```

### Parallel Issue Fixing

```bash
# Create worktrees
git worktree add -b fix/issue-78 /tmp/issue-78 main
git worktree add -b fix/issue-99 /tmp/issue-99 main

# Launch in parallel
codex --yolo exec 'Fix issue #78. Commit when done.'  # in /tmp/issue-78
codex --yolo exec 'Fix issue #99. Commit when done.'  # in /tmp/issue-99

# Push and create PRs after completion
```

### PR Reviews

```bash
# Clone to temp directory for safe review
REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW
cd $REVIEW && gh pr checkout 42 && codex review --base origin/main
```

### Pitfalls

- ALWAYS use `pty=true` — Codex is an interactive terminal app
- Git repo REQUIRED — use `mktemp -d && git init` for scratch work
- In Hermes gateway contexts, sandbox may fail — use `--sandbox danger-full-access`
- Don't interfere with long tasks — monitor with `poll`/`log`, be patient

---

## OpenCode (Provider-Agnostic)

### Installation

```bash
npm i -g opencode-ai@latest
# or: brew install anomalyco/tap/opencode
opencode auth login  # or set provider env vars
```

### One-Shot Tasks

```bash
opencode run 'Add retry logic to API calls and update tests'
```

**Key flags:**
- `run 'prompt'` — one-shot execution
- `-f <file>` — attach context files
- `--thinking` — show model reasoning
- `--model provider/model` — force specific model
- `--format json` — machine-readable output

### Interactive Sessions

```bash
# Start TUI in background
opencode  # background=true, pty=true

# Send prompts
process(action="submit", session_id="<id>", data="Implement OAuth refresh flow")

# Exit with Ctrl+C (NOT /exit)
process(action="write", session_id="<id>", data="\x03")
```

**Key TUI keybindings:**
- `Enter` (×2) — submit message
- `Tab` — switch between agents (build/plan)
- `Ctrl+P` — command palette
- `Ctrl+X N` — new session
- `Ctrl+C` — exit

### Session Management

```bash
opencode -c                    # Continue last session
opencode -s <session-id>       # Resume specific session
opencode session list          # List past sessions
opencode stats                 # Token usage and costs
```

### PR Review

```bash
opencode pr 42  # Built-in PR command
```

### Pitfalls

- `/exit` is NOT valid — opens agent selector instead. Use Ctrl+C.
- `pty=true` needed for interactive TUI; `opencode run` does NOT need pty
- PATH mismatch can select wrong binary — verify with `which -a opencode`
- Enter may need to be pressed twice in TUI

---

## Common Patterns

### Parallel Task Execution

Run multiple agents simultaneously in isolated workdirs:

```bash
# Claude Code
tmux new-session -d -s task1 && tmux send-keys -t task1 'cd /project && claude -p "Fix auth bug" --max-turns 10' Enter

# Codex
terminal(command="codex exec 'Fix auth bug'", workdir="/tmp/task2", background=true, pty=true)

# OpenCode
terminal(command="opencode run 'Fix auth bug'", workdir="/tmp/task3", background=true, pty=true)
```

### Worktree-Based Isolation

```bash
# Create isolated worktrees for each task
git worktree add -b fix/a /tmp/fix-a main
git worktree add -b fix/b /tmp/fix-b main

# Run agents in parallel
# Agent A in /tmp/fix-a
# Agent B in /tmp/fix-b

# After completion, push and create PRs
git push -u origin fix/a  # from /tmp/fix-a
gh pr create --head fix/a --title "fix: ..."
```

### Monitoring Long Tasks

```bash
# Check if agent is still working or waiting for input
# Claude Code: tmux capture-pane -t <session> -p -S -10
# Look for: ❯ = waiting, ● = actively working

# Codex: process(action="poll", session_id="<id>")
# OpenCode: process(action="log", session_id="<id>")
```

---

## Pitfalls (All Agents)

- **Not setting `workdir`** — agents operate on the wrong project
- **Not using `pty=true`** for interactive modes — agents hang without terminal
- **Killing slow sessions too early** — agents may be doing multi-step work
- **Sharing working directories across parallel sessions** — file conflicts
- **Not monitoring background processes** — agents may ask for input and hang
- **Ignoring cost limits** — always set `--max-budget-usd` or `--max-turns`
- **Not cleaning up tmux sessions** — resource leaks over time
