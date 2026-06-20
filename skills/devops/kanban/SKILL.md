---
name: kanban
description: "Hermes Kanban multi-agent orchestration: task routing, decomposition, worker lifecycle, and collaboration patterns."
version: 3.0.0
platforms: [linux, macos, windows]
environments: [kanban]
metadata:
  hermes:
    tags: [kanban, multi-agent, orchestration, routing, collaboration, workflow]
    related_skills: [hermes-agent]
---

# Kanban Multi-Agent Orchestration

Hermes Kanban system for routing work through a multi-agent fleet. Covers both the orchestrator role (decomposition, routing) and the worker role (execution, handoffs, pitfalls).

> The **core worker lifecycle** (6 steps: orient → work → heartbeat → block/complete) is auto-injected into every kanban worker's system prompt as `KANBAN_GUIDANCE`. This skill provides the deeper playbook for both orchestrators and workers.

## When to Use the Board

Create Kanban tasks when any of these are true:

1. **Multiple specialists are needed.** Research + analysis + writing = three profiles.
2. **The work should survive a crash or restart.** Long-running, recurring, or important.
3. **The user might want to interject.** Human-in-the-loop at any step.
4. **Multiple subtasks can run in parallel.** Fan-out for speed.
5. **Review / iteration is expected.** A reviewer profile loops on drafter output.
6. **The audit trail matters.** Board rows persist in SQLite forever.

If *none* apply — it's a small one-shot reasoning task — use `delegate_task` or answer directly.

---

## Part 1: Orchestrator — Decomposition & Routing

### Step 0: Discover Available Profiles

Before fanning out, ground decomposition in profiles that actually exist. The dispatcher silently fails on unknown assignee names.

- `hermes profile list` — prints configured profiles
- `kanban_list(assignee="<name>")` — sanity-check a single name (returns empty for unknown)
- **Ask the user:** "What profiles do you have set up?"

Cache the result for the rest of the conversation.

### The Anti-Temptation Rules

- **Do not execute the work yourself.** If you find yourself "just fixing this quickly" — stop and create a task.
- **For any concrete task, create a Kanban task and assign it.** Every single time.
- **Split multi-lane requests before creating cards.** Extract independent workstreams, create one card per lane.
- **Run independent lanes in parallel.** Leave them unlinked so the dispatcher fans them out. Link only true data dependencies.
- **Never create dependent work as independent ready cards.** Use `parents=[...]` in `kanban_create`.
- **If no specialist fits, ask the user.** Do not invent profile names.
- **Decompose, route, and summarize — that's the whole job.**

### Decomposition Playbook

**Step 1 — Understand the goal.** Ask clarifying questions if ambiguous.

**Step 2 — Sketch the task graph.** Draft the graph out loud before creating anything:
1. Extract lanes from the request.
2. Map each lane to an existing profile.
3. Decide independence vs. gating.
4. Create independent lanes as parallel cards.
5. Create synthesis/review cards with parent links.

**Step 3 — Create tasks and link.**

```python
t1 = kanban_create(
    title="research: cost comparison",
    assignee="<profile-A>",
    body="Compare estimated infrastructure costs over 3 years...",
)["task_id"]

t2 = kanban_create(
    title="research: performance comparison",
    assignee="<profile-A>",
    body="Compare query latency and throughput at expected volume...",
)["task_id"]

t3 = kanban_create(
    title="synthesize recommendation",
    assignee="<profile-B>",
    body="Read T1 and T2 findings. Produce 1-page recommendation...",
    parents=[t1, t2],
)["task_id"]
```

`parents=[...]` gates promotion — children stay in `todo` until all parents reach `done`, then auto-promote to `ready`.

**Step 4 — Complete your own task.** If you were spawned as a planner, mark done with a summary of what you created.

**Step 5 — Report back to the user.** Name the actual profiles used and the task graph.

### Common Patterns

- **Fan-out + fan-in:** N research cards (no parents) → 1 synthesis card (all as parents).
- **Parallel implementation + validation:** implementer + explorer in parallel; reviewer depends on both.
- **Pipeline with gates:** planner → implementer → reviewer. Each stage's `parents=[previous]`.
- **Same-profile queue:** N tasks to same profile, no dependencies. Dispatcher serializes them.
- **Human-in-the-loop:** Any task can `kanban_block()` to wait for input. Dispatcher respawns after `/unblock`.

### Goal-Mode Cards (Persistent Workers)

For open-ended cards where one turn rarely finishes:

```python
kanban_create(
    title="Translate the full docs site to French",
    body="Acceptance: every page translated, no English left, links intact.",
    assignee="<translator-profile>",
    goal_mode=True,
    goal_max_turns=15,
)["task_id"]
```

After each turn, a judge evaluates against title+body (acceptance criteria). Not done + budget remains → worker continues in the same session. Budget exhausted → card blocked for human review.

---

## Part 2: Worker — Execution & Handoffs

### Workspace Handling

| Kind | What it is | How to work |
|---|---|---|
| `scratch` | Fresh tmp dir | Read/write freely; GC'd when archived. |
| `dir:<path>` | Shared persistent directory | Other runs read what you write. Treat as long-lived state. |
| `worktree` | Git worktree | If `.git` missing, run `git worktree add <path> ${HERMES_KANBAN_BRANCH:-wt/$HERMES_KANBAN_TASK}` first, then commit work here. |

### Good Summary + Metadata Shapes

**Coding task:**
```python
kanban_complete(
    summary="shipped rate limiter — token bucket, 14 tests pass",
    metadata={
        "changed_files": ["rate_limiter.py", "tests/test_rate_limiter.py"],
        "tests_run": 14, "tests_passed": 14,
        "decisions": ["user_id primary, IP fallback for unauthenticated"],
    },
)
```

**Review-required (block instead of complete):**
```python
kanban_comment(body="review-required handoff:\n" + json.dumps({
    "changed_files": [...], "tests_run": 14, "tests_passed": 14,
    "diff_path": "/path/to/worktree",
}))
kanban_block(reason="review-required: rate limiter shipped, 14/14 tests pass — needs eyes on user_id/IP fallback choice")
```

**Research task:**
```python
kanban_complete(
    summary="3 libraries reviewed; vLLM wins on throughput",
    metadata={"sources_read": 12, "recommendation": "vLLM"},
)
```

### Claiming Cards You Created

If you produced new tasks via `kanban_create`, pass their ids in `created_cards`:

```python
c1 = kanban_create(title="fix SQL injection", assignee="security-worker")
c2 = kanban_create(title="fix CSRF", assignee="web-worker")
kanban_complete(
    summary="Review done; spawned remediations.",
    created_cards=[c1["task_id"], c2["task_id"]],
)
```

The kernel verifies each id exists and was created by your profile. Phantom ids block completion with an error.

### Block Reasons That Get Answered Fast

Bad: `"stuck"`. Good: one sentence naming the specific decision.

```python
kanban_comment(body="Full context: I have user IPs from Cloudflare headers but some users are behind NATs...")
kanban_block(reason="Rate limit key choice: IP (simple, NAT-unsafe) or user_id (requires auth)?")
```

### Heartbeats

Good: `"epoch 12/50, loss 0.31"`, `"scanned 1.2M/2.4M rows"`. Bad: `"still working"`, sub-second intervals. Every few minutes max; skip for tasks under ~2 minutes.

### Retry Diagnostics

If `kanban_show` shows closed runs, read their `outcome`/`summary`/`error`:
- `timed_out` → chunk work or shorten it
- `crashed` → reduce memory footprint
- `spawn_failed` → profile config issue; ask human via `kanban_block`
- `reclaimed` + `archived` → check status; you may not need to run
- `blocked` → unblock comment should be in thread

---

## Pitfalls (Both Roles)

**Inventing profile names.** Dispatcher silently fails — card sits in `ready` forever. Always use discovered profiles.

**Bundling independent lanes into one card.** "Fix blockers and check model variants" → two cards, not one.

**Over-linking because of wording.** "Finally check X" may still be parallel if X is static config/docs.

**Forgetting dependency links.** Use `parents=[...]` so implement/review can't run before inputs exist.

**Reassignment vs. new task.** If reviewer blocks with "needs changes," create a NEW task linked from the reviewer's task — don't re-run the same one.

**Task state changes between dispatch and startup.** Always `kanban_show` first. If `blocked` or `archived`, stop.

**Workspace stale artifacts.** `dir:` and `worktree` workspaces can have files from previous runs. Read the comment thread.

**Using CLI in containerized backends.** `hermes kanban <verb>` fails in Docker/Modal/SSH backends. Use `kanban_*` tools instead.

**Don't use `delegate_task` as substitute for `kanban_create`.** `delegate_task` is for short reasoning subtasks inside YOUR run; `kanban_create` is for cross-agent handoffs that outlive one API loop.

**Don't use `clarify` in headless mode.** There's no live user. Use `kanban_comment` + `kanban_block` instead.

**Don't modify files outside `$HERMES_KANBAN_WORKSPACE`** unless the task body says to.

**Don't create follow-up tasks assigned to yourself.** Assign to the right specialist.

**Don't complete a task you didn't finish.** Block it instead.
