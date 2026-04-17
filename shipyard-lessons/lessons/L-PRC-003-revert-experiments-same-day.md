---
id: L-PRC-003
title: Revert failed experiments the same day — don't defend a bad 4-hour investment
severity: medium
category: process
platforms: [ios-swiftui, android-kotlin, flutter, react-native-expo]
tags: [experiments, sunk-cost, git-revert, product]
polarity: require
applies_when: "Shipping an experimental feature that needs on-device validation"
source_project: runlock
learned_at: 2026-04-16
last_verified: 2026-04-17
supersedes: []
superseded_by: null
---

## Pattern
Ship the experiment → test on real device → if it fails the bar (performance, aesthetics, UX), `git revert` the same day → replace with a known-good alternative. Don't keep bad code in the tree to defend the time you spent writing it.

## Why it matters
Sunk cost is the silent killer of shipped quality. Keeping a bad implementation because "I spent 4 hours on this" ensures bad code ships. Reverting cleanly — with a single revert commit — preserves the experiment in history for future reference without inflicting it on users.

## Detect

- [ ] Are there experimental features gated behind an `ENABLE_*` flag that's been on for weeks without a decision?
- [ ] Does the repo have any "keep for now, will fix later" comments older than 7 days?
- [ ] Is any PR description longer than the diff? (Often a sign of defending the approach.)

## Fix

1. On device, evaluate the experiment against a hard bar (frame rate, file size, aesthetic, conversion).
2. If it fails: `git revert <commit-hash>` as a single commit with a clear message.
3. Ship the known-good alternative in the next commit.
4. Document the learning in `docs/LESSONS-LEARNED.md` or as a new lesson in the central library.
5. Never `git reset` to erase the history — the revert is itself a learning artifact.

## Worked example

- Same-day revert pattern:
  - `93efcaa feat: add AI-generated background images to sharing story cards`
  - `d8cc57a Revert "feat: add AI-generated background images to sharing story cards"`
  - `1e313e6 feat: add static background images for sharing story cards` (the known-good alternative)

## Anti-patterns

- Adding feature flags to hide bad code that should be reverted.
- "We'll improve this later" — a year later, it's still there.
- Squash-merging experiments so the revert trail disappears.

## Related

- L-PRC-001 — Ship-wreck review (often surfaces experiment failures)
