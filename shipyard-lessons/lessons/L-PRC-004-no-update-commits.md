---
id: L-PRC-004
title: Never commit with just "update" as the message — it signals lost context
severity: low
category: process
platforms: [ios-swiftui, android-kotlin, flutter, react-native-expo]
tags: [commit-hygiene, git, code-review, blame]
polarity: avoid
applies_when: "Any active repo"
source_project: runlock
learned_at: 2026-04-17
last_verified: 2026-04-17
supersedes: []
superseded_by: null
---

## Mistake
Commits titled `update`, `wip`, `misc`, `stuff`, `fix` (with no object). These commits cluster during periods of active context-switching — mid-pivot, mid-refactor, mid-crunch — and destroy the git-blame signal that future-you needs.

## Why it matters
`git log --oneline | grep update` is the best diagnostic for where a project lost discipline. Runlock had a 12-commit streak of `update` messages during the mid-April branding/onboarding pivot. Three months from now, nobody — not even the author — will remember what any of them did. A later bug bisect through that range is brutal.

## Detect

```shell
# detect: PRESENT=0 if recent history has no "update"/"wip"/"misc" commits, ABSENT=1 otherwise
count=$(git log --all --pretty=format:'%s' -n 200 | grep -iE '^(update|wip|misc|stuff|fix|updates|changes)$' | wc -l | tr -d ' ')
if [ "$count" -ge 3 ]; then
  echo "Found $count low-signal commit messages in last 200 commits"
  exit 1
fi
exit 0
```

## Fix

1. Before committing, answer: "what would a future reader search for to find this commit?"
2. Use conventional-commit prefixes: `feat:`, `fix:`, `refactor:`, `docs:`, `chore:`, `perf:`, `ci:`.
3. If the current change doesn't fit one subject, split it into two commits.
4. If you must ship a WIP, use `wip(feature): <what's in progress>` — still searchable.
5. Rebase + amend meaningless messages before opening a PR.

## Worked example

- Anti-example streak from Runlock: `cfe043c update` / `55efe4c update` / `af88db3 update` / `2b5ec9b update` / `e7edc77 update` / `6344dc4 update` / `94c5bc4 update` / `6c5afdd update` / `2d2b1e5 update` / `a3fb671 update` — 10+ such commits during the mid-project pivot.
- Compare with `d4abdad refactor: route all analytics through AnalyticsRouter, add feature flags, set AppsFlyer App ID` — tells you exactly what happened.

## Anti-patterns

- Batch-committing a day's work with `git commit -am "update"`.
- Using a template that auto-fills "update" when message is empty.

## Related

- L-PRC-002 — One plan per feature (a plan file often gives you the commit message too)
