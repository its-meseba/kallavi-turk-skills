---
name: no-brainer
description: Boil down any input into a 3-point executive summary (Problem, Solution, Impact) plus optional Context. Three sub-skills — `no-brainer:summary` presents the summary, `no-brainer:description` updates a Linear issue with it, `no-brainer:brief` prepares you to communicate a topic to executives with full Linear context. Use when the user shares something verbose and wants the core takeaway distilled, says "summarize", "break this down", "tldr", "executive summary", "brief me", or pastes a wall of text needing clarity.
---

# No-Brainer

Turn any input into a crystal-clear executive summary. Three points, no fluff.

## Why This Exists

People drown in details. Whether it's a Linear issue, a meeting recap, or a Slack thread — the actual point gets buried. This skill forces macro clarity: what's broken, how to fix it, and what changes when you do.

## The Format

Every summary follows this exact structure:

```markdown
# Executive Summary

1. **Problem:** [One sentence — what's broken or missing]
2. **Solution:** [One sentence — the approach or path forward]
3. **Impact:** [One sentence — what changes when this is done]

**Context**

[One paragraph max. Include relevant links, prior decisions, or technical constraints. Supplementary — the 3 points above must stand on their own.]

---
```

Formatting rules:
- `# Executive Summary` is always an H1 header
- Problem, Solution, Impact are a numbered ordered list (1. 2. 3.) with bold labels
- No divider before Context — it flows naturally after the 3 points
- Divider (`---`) goes AFTER Context, before any remaining content below
- Context section is optional — only include when genuinely useful

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

## Sub-Skills

| Command | Purpose |
|---------|---------|
| `/no-brainer:summary` | Just present the executive summary — no Linear updates |
| `/no-brainer:description` | Generate summary + update Linear issue description |
| `/no-brainer:brief` | Full executive communication prep — reads Linear context, gives talking points |
| `/no-brainer:walk-me-through` | Post a numbered step-by-step activity log as a Linear issue comment |
| `/no-brainer:help` | Show help — what No-Brainer does and how to use it |

## Help (`/no-brainer:help`)

When this sub-command is invoked, present the following to the user:

---

### No-Brainer

Distills any input into a 3-point executive summary: **Problem, Solution, Impact** — plus optional Context. Feed it a wall of text, get back the core takeaway.

#### The Format

Every summary follows this structure:

```
1. Problem:   [One sentence — what's broken or missing]
2. Solution:  [One sentence — the approach or path forward]
3. Impact:    [One sentence — what changes when this is done]

Context: [One paragraph max — links, prior decisions, constraints. Optional.]
```

#### Commands

| Command | What it does |
|---------|-------------|
| `/no-brainer` or `/no-brainer:summary` | Present the executive summary only |
| `/no-brainer:description` | Generate summary + update a Linear issue description with it |
| `/no-brainer:brief` | Full executive communication prep — reads Linear context, gives talking points for presenting to leadership |
| `/no-brainer:walk-me-through` | Post a numbered step-by-step activity log as a Linear issue comment — plain-language steps + technical context |

#### When to use

Say "summarize this", "tldr", "break this down", "executive summary", or just paste a wall of text. Works on meeting recaps, Slack threads, Linear issues, technical writeups — anything verbose that needs the core point extracted.

#### What it's NOT

- Not a detailed analysis tool — it distills, not expands
- Not a project plan — it clarifies "what" and "why", not "how in 47 steps"
- Not a meeting notes formatter — it extracts the core point, not a chronological recap

## Walk-Me-Through (`/no-brainer:walk-me-through`)

Generate a numbered step-by-step activity log and post it as a comment on a Linear issue. Designed for team visibility — anyone can follow what was done without drowning in implementation details.

### Input

The user provides:
- A Linear issue ID/URL (required) — or issue IDs are passed from another skill (e.g., `/qgit`)
- Context about what was done — from conversation history, git commits, or explicit description

### The Format

Each step has two parts:

```markdown
### n/total — [Plain-language meaning of what was done]

**Technical Context:** [Implementation details — files changed, APIs used, key decisions. To the point.]
```

**Line 1 (the title):** What happened, in words anyone on the team can understand. No jargon. This is for PMs, designers, executives — anyone following the issue.

**Line 2 (technical context):** Implementation specifics for engineers — file paths, function names, architectural decisions. Brief and reference-heavy, not prose.

### Example Output

```markdown
## Activity Walk-Through

### 1/4 — Added subscription duration column to the cancellation table

**Technical Context:** New `subscription_days` column in `CancellationCommentsTable.tsx`. Computed from `subscription.startDate` via `daysSince()` utility in `src/utils/dates.ts`.

### 2/4 — Added total notes count for each churned user

**Technical Context:** Added `notesCount` field to the cancellation query in `src/services/posthog.ts`. Aggregates from `notes` table joined on `user_id`.

### 3/4 — Styled new columns to match existing table layout

**Technical Context:** Reused `MetricCell` component from `src/components/MetricCell.tsx`. No new CSS — followed existing column width pattern.

### 4/4 — Updated dashboard filters to support sorting by new columns

**Technical Context:** Extended `SortConfig` type in `src/types/dashboard.ts`. Added sort handlers in `useCancellationTable` hook.
```

### Process

1. **Gather what was done.** Read conversation history, git log, diff — whatever is available. Understand the full scope of work.
2. **Break into logical steps.** Each step = one meaningful unit of work. Not every file change — every *meaningful change*. Group related file changes into a single step.
3. **Write the plain-language title first.** Ask: "Would a PM understand this in 5 seconds?" If not, simplify.
4. **Add technical context.** Reference specific files, functions, components. Keep it to 1-2 sentences max. Engineers can click through to the code.
5. **Number as `n/total`.** Total count goes in every step so readers know the full scope at a glance.
6. **Post as a Linear comment** on the issue using `save_comment`.

### Rules

- Steps are ordered chronologically — the sequence tells a story
- Total step count should be between 3-8 for most tasks. If you have 15 steps, you're too granular. Group related changes.
- Plain-language titles must NOT use code terms (no `refactor`, `implement`, `initialize`). Say what the user/team gains.
- Technical context references files with relative paths, not absolute
- Never post without showing the user first for confirmation
- If no Linear issue is provided, ask for one

## What This Skill is NOT

- Not a detailed analysis tool — it distills, not expands
- Not a project plan — it clarifies "what" and "why", not "how in 47 steps"
- Not a meeting notes formatter — it extracts the core point, not a chronological recap
