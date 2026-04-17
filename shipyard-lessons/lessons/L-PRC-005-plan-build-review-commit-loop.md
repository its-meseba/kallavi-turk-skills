---
id: L-PRC-005
title: Run the Plan → Build → Ship-Wreck Review → Commit loop every day
severity: critical
category: process
platforms: [ios-swiftui, android-kotlin, flutter, react-native-expo]
tags: [process, superpowers, workflow, daily-rhythm]
polarity: require
applies_when: "Any active solo or small-team project"
source_project: runlock
learned_at: 2026-04-17
last_verified: 2026-04-17
supersedes: []
superseded_by: null
---

## Pattern
The core shipping rhythm is four stages repeated:

1. **Plan** — `superpowers:writing-plans` writes `docs/superpowers/plans/YYYY-MM-DD-<slug>.md`.
2. **Build** — `superpowers:subagent-driven-development` or `executing-plans` executes the plan task-by-task.
3. **Ship-wreck review** — `ship-wreck-check` or `code-reviewer` agent catches real bugs before they compound.
4. **Commit** — single conventional-commit message summarizing the feature; ship-wreck fixes as a second commit.

Then repeat — next feature, next plan.

## Why it matters
When this loop held, Runlock stayed TestFlight-ready every night. When it broke (the 12-commit `update` streak), quality dipped within hours. This is the single highest-leverage habit. Everything else in the lessons library is a corollary.

## Detect

- [ ] Plans live in `docs/superpowers/plans/` (or similar) with ISO date prefixes.
- [ ] Every major feature commit has a matching plan file.
- [ ] Ship-wreck review commits appear in history.
- [ ] Commits use conventional prefixes.
- [ ] No long streak (>3) of low-signal commit messages.

## Fix

1. Install / enable the `superpowers` plugin if missing.
2. For every feature ≥4h: run `superpowers:writing-plans` before code.
3. Execute via `superpowers:subagent-driven-development` (or `executing-plans`).
4. Run `ship-wreck-check` before the commit.
5. Commit. Repeat.

## Worked example

- 60 commits / 17 plans / ~5 ship-wreck reviews / 10 days on Runlock.
- Days where the loop held: `feat: viral features — premium story cards, challenge a friend, celebration share` → `fix: ship-wreck review — carousel, presenter, multiplier, dead code, locale` — clean commit trail.
- Days where it broke: 12× `update` commits. Quality metrics and velocity both dropped.

## Anti-patterns

- Skipping planning for "quick" features that turn out to take 6h.
- Reviewing at the end of the week — by then, the bugs have compounded.
- Using the loop for trivial changes (<30 min) — creates overhead; just commit.

## Related

- L-PRC-001 — Ship-wreck review same day
- L-PRC-002 — One plan per feature
- L-PRC-004 — No "update" commits
