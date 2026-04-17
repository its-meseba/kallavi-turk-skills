---
id: L-PRC-001
title: Run a ship-wreck review commit after every major feature, same day
severity: high
category: process
platforms: [ios-swiftui, android-kotlin, flutter, react-native-expo]
tags: [code-review, quality, commit-hygiene, ship-wreck]
polarity: require
applies_when: "Any active project shipping features"
source_project: runlock
learned_at: 2026-04-17
last_verified: 2026-04-17
supersedes: []
superseded_by: null
---

## Pattern
After every feature lands, invoke `ship-wreck-check` (or `code-reviewer` agent) and commit its fixes as a single `fix: ship-wreck review — …` commit the same day. Before moving to the next feature. The context is still warm; reviewers haven't forgotten what they wrote.

## Why it matters
Every ship-wreck review on Runlock caught at least one real bug: a race condition (`a9a4b08`), an N+1 Firestore batch (`2f73906`), a missing URL scheme for OAuth callback (`a9a4b08`), a force-unwrap (`5ad576e`), a carousel bug + dead code (`4da37c7`). These would have compounded into a shipping-time crunch.

## Detect

```shell
# detect: PRESENT=0 if repo has ≥3 ship-wreck-style review commits recently, ABSENT=1 otherwise
git log --all --oneline -n 100 | grep -Ec "ship-wreck|^[a-f0-9]+ fix:.* review" | awk '{ exit ($1 >= 3 ? 0 : 1) }'
```

## Fix

1. After committing a feature, run the `ship-wreck-check` skill (or `code-reviewer` agent) on the feature's file set.
2. Address every CRITICAL and HIGH finding in the same session.
3. Commit the fixes as `fix: ship-wreck review — <short list>`.
4. Only then move to the next feature / plan.
5. Never batch reviews across multiple features — the context is lost.

## Worked example

- `4da37c7 fix: ship-wreck review — carousel, presenter, multiplier, dead code, locale`
- `2f73906 fix: ship-wreck review — error handling, Firestore batching, dead code, security`
- `a9a4b08 fix: ship-wreck review — crash race, dead events, unused import, missing URL scheme`
- `6d29167 fix: ship-wreck review — placeholder guards, private SDK services, dead code, build error`

## Anti-patterns

- "I'll batch review all features on Friday" — bugs compound, context is lost, Friday becomes a nightmare.
- Treating reviews as cosmetic — they consistently catch real bugs.

## Related

- L-PRC-002 — One plan per feature
- L-PRC-005 — Plan → build → review → commit loop
