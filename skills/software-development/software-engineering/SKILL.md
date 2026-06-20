---
name: software-engineering
aliases: [systematic-debugging]
description: "Software engineering practices: debugging, testing, code review, exploration, and quality assurance."
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [debugging, testing, tdd, code-review, troubleshooting, root-cause, investigation, software-engineering]
    related_skills: [plan, github, python-debugpy, node-inspect-debugger]
---

# Software Engineering

Comprehensive software engineering practices: systematic debugging, test-driven development, code review workflows, exploratory coding, and quality assurance.

## When to Use

- Debugging any technical issue (tests, production, performance, build)
- Writing or reviewing code with proper testing
- Exploring ideas via throwaway experiments
- Conducting code reviews before commits
- Investigating root causes before fixing

## Decision Map

| Task | Section |
|------|---------|
| Bug investigation | § Systematic Debugging |
| Write tests first | § Test-Driven Development |
| Review code before commit | § Code Review |
| Quick experiment / spike | § Exploration |
| Debug Python remotely | § Python Debugging |
| Debug Node.js | § Node.js Debugging |

---

## Systematic Debugging

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

### The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

### The Four Phases

**Phase 1: Root Cause Investigation**
- Read error messages carefully (stack traces, line numbers, error codes)
- Reproduce consistently — exact steps, every time?
- Check recent changes: `git log --oneline -10`, `git diff`
- Gather evidence in multi-component systems: log data at each boundary
- Trace data flow upstream to find the source

**Phase 2: Pattern Analysis**
- Find working examples in the same codebase
- Compare against reference implementations completely
- Identify differences between working and broken
- Understand dependencies, config, assumptions

**Phase 3: Hypothesis and Testing**
- Form a single specific hypothesis: "I think X is the root cause because Y"
- Test minimally — smallest possible change, one variable at a time
- If it doesn't work, form a NEW hypothesis. Don't add more fixes.

**Phase 4: Implementation**
- Create failing test case first (simplest reproduction)
- Implement ONE fix addressing the root cause
- Verify: run specific test, then full suite
- **Rule of Three:** If 3+ fixes failed, STOP and question the architecture

### Red Flags — STOP and Follow Process

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "I don't fully understand but this might work"
- Proposing solutions before tracing data flow
- Each fix reveals a new problem in a different place

### Tools for Investigation

- `search_files` — find error strings, trace function calls
- `read_file` — read source with line numbers
- `terminal` — run tests, check git history, reproduce bugs
- `web_search`/`web_extract` — research errors, library docs
- `delegate_task` — dispatch investigation subagents for complex multi-component bugs

---

## Test-Driven Development

**RED → GREEN → REFACTOR. Never skip a step.**

### The Cycle

1. **RED** — Write a failing test before any production code
   - Test must fail for the RIGHT reason (assertion on expected behavior, not setup error)
   - Run test, confirm it fails
   - If test passes immediately, the test is wrong

2. **GREEN** — Write the MINIMUM production code to make the test pass
   - Hardcode if needed. Copy-paste acceptable. Ugly is fine.
   - Goal: pass the test, not write clean code
   - No refactoring during GREEN

3. **REFACTOR** — Clean up with tests passing as safety net
   - Only after GREEN is confirmed
   - Run tests after every refactor step
   - If tests break during refactor, the refactor was wrong

### Rules

- **No production code without a failing test first**
- **One concept per test** — if you need "and" in the test name, split it
- **Test behavior, not implementation** — assert on outputs, not internal state
- **Tests are documentation** — name them as sentences: `test_user_cannot_withdraw_negative_amount`
- **Fast feedback loop** — tests should run in seconds, not minutes
- **No mocking what you don't own** — mock boundaries, not internals

### Test Structure

```python
def test_user_can_withdraw_funds():
    # Arrange
    account = Account(balance=100)
    
    # Act
    account.withdraw(50)
    
    # Assert
    assert account.balance == 50
```

### Anti-Patterns

| Anti-Pattern | Why It's Wrong | Fix |
|-------------|---------------|-----|
| Writing all tests upfront | Lose RED feedback | One test at a time |
| Writing production code before test | Can't verify test catches bug | Test first, always |
| Big-bang refactoring | Lose safety net | Small steps, test after each |
| Testing implementation details | Brittle tests | Test behavior, not internals |
| Slow tests | Kills feedback loop | Keep unit tests < 100ms |
| No tests for edge cases | Bugs in production | Test boundaries: null, empty, max, min |

---

## Code Review

Pre-commit review workflow to catch issues before they enter the codebase.

### Review Checklist

**Security:**
- [ ] No secrets in code (API keys, passwords, tokens)
- [ ] Input validation on all external data
- [ ] No SQL injection / XSS / command injection vectors
- [ ] Proper authentication/authorization checks
- [ ] No sensitive data in logs

**Quality:**
- [ ] Tests cover new behavior (not just lines)
- [ ] Error handling is explicit, not silent
- [ ] No dead code, unused imports, or commented-out blocks
- [ ] Naming is clear and intention-revealing
- [ ] Functions are focused (single responsibility)
- [ ] No magic numbers — use named constants

**Architecture:**
- [ ] Changes fit existing patterns
- [ ] No unnecessary coupling introduced
- [ ] Dependencies are justified
- [ ] API contracts are documented

### Review Process

1. **Self-review first** — read your own diff before asking others
2. **Run the checklist** — don't rely on memory
3. **Check test coverage** — `pytest --cov=src tests/`
4. **Verify no regressions** — full test suite passes
5. **Review in small chunks** — <400 lines per review session

### Simplify Code

When code is complex, simplify before shipping:

- **Remove duplication** — extract functions, use loops/maps
- **Reduce nesting** — early returns, guard clauses
- **Clarify names** — variable names should explain intent
- **Delete unused code** — commented code, unreachable branches
- **Break large functions** — <20 lines ideal, <50 acceptable
- **Replace conditionals with polymorphism** — when type switches grow

Use `delegate_task` with parallel subagents for systematic cleanup of recent changes.

---

## Exploration

### Spike (Throwaway Experiments)

When validating an idea before building:

- **Timebox:** 1-4 hours maximum
- **Goal:** Answer ONE specific question ("Can library X do Y?")
- **Output:** Working code + decision record (yes/no + why)
- **Scope:** No tests, no polish, no production concerns
- **Cleanup:** Delete after decision, or promote to real code with tests

**Process:**
1. Define the question clearly
2. Set a timer (1-4 hours)
3. Hack together the fastest possible working demo
4. Document findings: what worked, what didn't, blockers
5. Decision: proceed, pivot, or abandon

### Dogfood (Self-Testing)

Before shipping, use your own code as a real user would:

- Run the full workflow end-to-end
- Test with realistic data, not just fixtures
- Try to break it: invalid inputs, edge cases, stress
- Check error messages — are they helpful?
- Verify documentation matches actual behavior
- Test on a clean environment (no local setup assumptions)

---

## Language-Specific Debugging

### Python (debugpy)

Remote debugging for Python processes.

**Setup:**
```python
import debugpy
debugpy.listen(("0.0.0.0", 5678))
debugpy.wait_for_client()  # Block until debugger attaches
```

**Attach:**
```bash
python -m debugpy --listen 0.0.0.0:5678 --wait-for-client script.py
```

**VS Code launch.json:**
```json
{
  "name": "Python: Remote Attach",
  "type": "debugpy",
  "request": "attach",
  "connect": { "host": "localhost", "port": 5678 }
}
```

**Key features:** breakpoints, step over/into/out, watch variables, evaluate expressions, conditional breakpoints, logpoints, exception breakpoints, multi-threading support.

**Common issues:** port conflicts (use `lsof -i :5678`), firewall blocking, `0.0.0.0` vs `127.0.0.1`, timeout on `wait_for_client`.

### Node.js (--inspect)

Remote debugging for Node.js processes.

**Start with inspector:**
```bash
node --inspect script.js        # Start, wait for debugger
node --inspect-brk script.js    # Break on first line
node --inspect=0.0.0.0:9229 script.js  # Custom host/port
```

**Attach with Chrome DevTools:**
1. Open `chrome://inspect`
2. Click "Open dedicated DevTools for Node"
3. Select target from list

**Attach with VS Code:**
```json
{
  "name": "Attach to Node",
  "type": "node",
  "request": "attach",
  "port": 9229,
  "restart": true
}
```

**Programmatic attachment:**
```javascript
const inspector = require('inspector');
inspector.open(9229, '0.0.0.0');
inspector.waitForDebugger();  // Block until attached
```

**Key features:** breakpoints, step over/into/out, console evaluation, heap snapshots, CPU profiling, async stack traces, worker thread debugging.

**Common issues:** port already in use, firewall blocking, source map problems, async call stack gaps, worker thread complexity.

---

## Pitfalls

- **Debugging:** Skipping Phase 1 investigation → symptom fixes that create new bugs
- **TDD:** Writing tests after code → tests that always pass, no regression safety
- **Code review:** Rubber-stamping → bugs and security issues in production
- **Exploration:** Spikes that become production code without tests
- **Python debugpy:** Using `127.0.0.1` in Docker containers → debugger can't attach
- **Node.js:** `--inspect` without `--inspect-brk` → missing initialization bugs

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- Someone wants it fixed NOW (systematic is faster than thrashing)

## The Four Phases

You MUST complete each phase before proceeding to the next.

---

## Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

### 1. Read Error Messages Carefully

- Don't skip past errors or warnings
- They often contain the exact solution
- Read stack traces completely
- Note line numbers, file paths, error codes

**Action:** Use `read_file` on the relevant source files. Use `search_files` to find the error string in the codebase.

### 2. Reproduce Consistently

- Can you trigger it reliably?
- What are the exact steps?
- Does it happen every time?
- If not reproducible → gather more data, don't guess

**Action:** Use the `terminal` tool to run the failing test or trigger the bug:

```bash
# Run specific failing test
pytest tests/test_module.py::test_name -v

# Run with verbose output
pytest tests/test_module.py -v --tb=long
```

### 3. Check Recent Changes

- What changed that could cause this?
- Git diff, recent commits
- New dependencies, config changes

**Action:**

```bash
# Recent commits
git log --oneline -10

# Uncommitted changes
git diff

# Changes in specific file
git log -p --follow src/problematic_file.py | head -100
```

### 4. Gather Evidence in Multi-Component Systems

**WHEN system has multiple components (API → service → database, CI → build → deploy):**

**BEFORE proposing fixes, add diagnostic instrumentation:**

For EACH component boundary:
- Log what data enters the component
- Log what data exits the component
- Verify environment/config propagation
- Check state at each layer

Run once to gather evidence showing WHERE it breaks.
THEN analyze evidence to identify the failing component.
THEN investigate that specific component.

### 5. Trace Data Flow

**WHEN error is deep in the call stack:**

- Where does the bad value originate?
- What called this function with the bad value?
- Keep tracing upstream until you find the source
- Fix at the source, not at the symptom

**Action:** Use `search_files` to trace references:

```python
# Find where the function is called
search_files("function_name(", path="src/", file_glob="*.py")

# Find where the variable is set
search_files("variable_name\\s*=", path="src/", file_glob="*.py")
```

### Phase 1 Completion Checklist

- [ ] Error messages fully read and understood
- [ ] Issue reproduced consistently
- [ ] Recent changes identified and reviewed
- [ ] Evidence gathered (logs, state, data flow)
- [ ] Problem isolated to specific component/code
- [ ] Root cause hypothesis formed

**STOP:** Do not proceed to Phase 2 until you understand WHY it's happening.

---

## Phase 2: Pattern Analysis

**Find the pattern before fixing:**

### 1. Find Working Examples

- Locate similar working code in the same codebase
- What works that's similar to what's broken?

**Action:** Use `search_files` to find comparable patterns:

```python
search_files("similar_pattern", path="src/", file_glob="*.py")
```

### 2. Compare Against References

- If implementing a pattern, read the reference implementation COMPLETELY
- Don't skim — read every line
- Understand the pattern fully before applying

### 3. Identify Differences

- What's different between working and broken?
- List every difference, however small
- Don't assume "that can't matter"

### 4. Understand Dependencies

- What other components does this need?
- What settings, config, environment?
- What assumptions does it make?

---

## Phase 3: Hypothesis and Testing

**Scientific method:**

### 1. Form a Single Hypothesis

- State clearly: "I think X is the root cause because Y"
- Write it down
- Be specific, not vague

### 2. Test Minimally

- Make the SMALLEST possible change to test the hypothesis
- One variable at a time
- Don't fix multiple things at once

### 3. Verify Before Continuing

- Did it work? → Phase 4
- Didn't work? → Form NEW hypothesis
- DON'T add more fixes on top

### 4. When You Don't Know

- Say "I don't understand X"
- Don't pretend to know
- Ask the user for help
- Research more

---

## Phase 4: Implementation

**Fix the root cause, not the symptom:**

### 1. Create Failing Test Case

- Simplest possible reproduction
- Automated test if possible
- MUST have before fixing
- Use the `test-driven-development` skill

### 2. Implement Single Fix

- Address the root cause identified
- ONE change at a time
- No "while I'm here" improvements
- No bundled refactoring

### 3. Verify Fix

```bash
# Run the specific regression test
pytest tests/test_module.py::test_regression -v

# Run full suite — no regressions
pytest tests/ -q
```

### 4. If Fix Doesn't Work — The Rule of Three

- **STOP.**
- Count: How many fixes have you tried?
- If < 3: Return to Phase 1, re-analyze with new information
- **If ≥ 3: STOP and question the architecture (step 5 below)**
- DON'T attempt Fix #4 without architectural discussion

### 5. If 3+ Fixes Failed: Question Architecture

**Pattern indicating an architectural problem:**
- Each fix reveals new shared state/coupling in a different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

**STOP and question fundamentals:**
- Is this pattern fundamentally sound?
- Are we "sticking with it through sheer inertia"?
- Should we refactor the architecture vs. continue fixing symptoms?

**Discuss with the user before attempting more fixes.**

This is NOT a failed hypothesis — this is a wrong architecture.

---

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals a new problem in a different place**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (Phase 4 step 5).

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question the pattern, don't fix again. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence, trace data flow | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare, identify differences | Know what's different |
| **3. Hypothesis** | Form theory, test minimally, one variable at a time | Confirmed or new hypothesis |
| **4. Implementation** | Create regression test, fix root cause, verify | Bug resolved, all tests pass |

## Hermes Agent Integration

### Investigation Tools

Use these Hermes tools during Phase 1:

- **`search_files`** — Find error strings, trace function calls, locate patterns
- **`read_file`** — Read source code with line numbers for precise analysis
- **`terminal`** — Run tests, check git history, reproduce bugs
- **`web_search`/`web_extract`** — Research error messages, library docs

### With delegate_task

For complex multi-component debugging, dispatch investigation subagents:

```python
delegate_task(
    goal="Investigate why [specific test/behavior] fails",
    context="""
    Follow systematic-debugging skill:
    1. Read the error message carefully
    2. Reproduce the issue
    3. Trace the data flow to find root cause
    4. Report findings — do NOT fix yet

    Error: [paste full error]
    File: [path to failing code]
    Test command: [exact command]
    """,
    toolsets=['terminal', 'file']
)
```

### With test-driven-development

When fixing bugs:
1. Write a test that reproduces the bug (RED)
2. Debug systematically to find root cause
3. Fix the root cause (GREEN)
4. The test proves the fix and prevents regression

## Real-World Impact

From debugging sessions:
- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: Near zero vs common

**No shortcuts. No guessing. Systematic always wins.**
