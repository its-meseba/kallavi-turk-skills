---
id: L-PRC-002
title: One plan per feature — 15-30 KB sweet spot, task checklist format
severity: medium
category: process
platforms: [ios-swiftui, android-kotlin, flutter, react-native-expo]
tags: [planning, superpowers, subagent-driven-development, process]
polarity: require
applies_when: "Any non-trivial feature being built (≥4h work)"
source_project: runlock
learned_at: 2026-04-17
last_verified: 2026-04-17
supersedes: []
superseded_by: null
---

## Pattern
Every non-trivial feature gets one plan file in `docs/superpowers/plans/YYYY-MM-DD-<slug>.md`. Target 15-30 KB (a few hundred lines). Top: goal + architecture + tech stack in 3 bullets. Middle: file map (new/modified/deleted). Bottom: task list with `- [ ]` checkboxes. Use `superpowers:subagent-driven-development` or `superpowers:executing-plans` to execute.

## Why it matters
Runlock's 114 KB kickoff plan was a roadmap — useful. The 15-30 KB feature plans (`2026-04-14-onboarding-fixes-and-polish.md`, `2026-04-13-branding-redesign.md`) actually got executed cleanly. Plans under 5 KB skipped too many details; plans over 50 KB drifted from reality by day 2.

## Detect

```shell
# detect: PRESENT=0 if docs/superpowers/plans or similar directory has ≥1 plan files, ABSENT=1 otherwise
find docs -path '*/plans/*.md' 2>/dev/null | grep -q . && exit 0
find . -path '*plan*.md' -not -path '*/node_modules/*' 2>/dev/null | head -1 | grep -q . && exit 0
exit 1
```

## Fix

1. Create `docs/superpowers/plans/` directory if missing.
2. Invoke `superpowers:writing-plans` skill (or the `planner` agent) before starting any feature >4h.
3. Save plans with ISO date prefix: `2026-05-01-<feature-slug>.md`.
4. Structure:
   ```
   # <Feature Name> Implementation Plan
   > REQUIRED SUB-SKILL: superpowers:subagent-driven-development
   **Goal:** <one sentence>
   **Architecture:** <one paragraph>
   **Tech Stack:** <one line>
   ---
   ## File Map
   | Action | File | Responsibility |
   ## Phase 1: ...
   - [ ] Task 1
   - [ ] Task 2
   ```
5. Execute via `superpowers:executing-plans` — it updates the checklist in place.

## Worked example

- Sweet-spot plan: `2026-04-13-branding-redesign.md` (25 KB, ~600 lines) — executed cleanly.
- Oversized plan: `2026-04-09-runlock-ios-implementation.md` (114 KB) — useful as roadmap, drifted as task list.
- Plan directory: `docs/superpowers/plans/` — 17 plans over 10 days.

## Anti-patterns

- A single master plan for the whole app.
- Plans without checkboxes — no execution trail.
- Plans dated "Q2 2026" — too coarse, not ISO.

## Related

- L-PRC-001 — Ship-wreck review after each plan
- L-PRC-005 — Plan → build → review → commit loop
