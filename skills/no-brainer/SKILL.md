---
name: no-brainer
description: Boil down any input into a 3-point executive summary (Problem, Solution, Impact). Two sub-skills — `no-brainer:description` updates a Linear issue description with the summary, `no-brainer:summary` just presents it. Use when the user shares something verbose and wants the core takeaway distilled, says "summarize", "break this down", "tldr", "executive summary", or pastes a wall of text needing clarity.
---

# No-Brainer

Turn any input into a crystal-clear executive summary. Three points, no fluff.

## Why This Exists

People drown in details. Whether it's a Linear issue, a meeting recap, or a Slack thread — the actual point gets buried. This skill forces macro clarity: what's broken, how to fix it, and what changes when you do.

## The Format

Every summary follows this exact structure:

```
**Executive Summary**

**Problem:** [One sentence — what's broken or missing]

**Solution:** [One sentence — the approach or path forward]

**Impact:** [One sentence — what changes when this is done]
```

Three lines. If someone reads only these, they should fully understand the situation.

### When Context is needed

Sometimes the three lines aren't enough — there's background, prior decisions, resource links, or technical nuance. Add a Context section **after** the three points only when genuinely useful:

```
---

**Context**

[One paragraph max. Include relevant links, prior decisions, or technical constraints. Supplementary — the 3 points above must stand on their own.]
```

## How to Write Each Point

### Problem
State what's broken, missing, or blocking — not symptoms, not history. One sentence.
- Bad: "Users have been complaining about the checkout flow and we've seen a 12% drop in conversions over the last quarter"
- Good: "Checkout abandonment is 40% because the payment step requires 6 form fields"

### Solution
State the approach — not implementation details, not a task list. One sentence.
- Bad: "We need to create a new React component that integrates with Stripe's v3 API and handles card tokenization"
- Good: "Reduce payment to a single-step card input with Stripe's hosted checkout"

### Impact
State what changes — in measurable or observable terms. One sentence.
- Bad: "This will improve the user experience and make things better"
- Good: "Recover ~15% of abandoned checkouts, estimated $50K/month in recovered revenue"

## Core Process

1. **Read the input carefully.** Understand the full picture before summarizing.
2. **Identify the macro.** "If I had 10 seconds to explain this to a CEO, what would I say?" — Problem. "What are we doing about it?" — Solution. "Why should anyone care?" — Impact.
3. **Write the 3 points.** Each a single sentence. No compound sentences. One idea per line.
4. **Decide on Context.** Genuinely useful background? Add it. Otherwise skip.

## What This Skill is NOT

- Not a detailed analysis tool — it distills, not expands
- Not a project plan — it clarifies "what" and "why", not "how in 47 steps"
- Not a meeting notes formatter — it extracts the core point, not a chronological recap
