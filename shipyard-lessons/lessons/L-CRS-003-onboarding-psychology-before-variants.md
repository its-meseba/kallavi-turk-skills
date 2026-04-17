---
id: L-CRS-003
title: Run a psychology / positioning pass before building onboarding variants
severity: high
category: product
platforms: [ios-swiftui, android-kotlin, flutter, react-native-expo]
tags: [onboarding, product, ab-test, psychology]
polarity: require
applies_when: "Building a new onboarding flow from scratch"
source_project: runlock
learned_at: 2026-04-12
last_verified: 2026-04-17
supersedes: []
superseded_by: null
---

## Pattern
Before writing any SwiftUI (or Compose, or Flutter) onboarding code, nail the psychological promise: what does the user commit to? What emotional state must they be in at the paywall? What ONE insight do they have to internalize? Write this as a one-page brief. Only after that, design 1-3 flows. A/B test messaging variants with copy only — not full code variants.

## Why it matters
Building N full onboarding variants before product signal is engineering cost with product risk. Runlock shipped three A/B variants (discipline / health / meme) then scrapped all of them for a single Promise-centered flow. Days of SwiftUI work thrown away — not because the code was bad, but because the product thesis was unbaked.

## Detect

- [ ] Does the project have a one-page onboarding brief identifying the psychological core?
- [ ] Are there ≥3 onboarding variants already coded without qualitative user signal?
- [ ] Is the paywall hit rate / conversion rate instrumented per variant?

## Fix

1. Pause all variant work.
2. Use the `marketing-psychology` or `superpowers:brainstorming` skill to produce a one-pager:
   - Who is the user at screen 1? (emotional state, pain)
   - What single promise do they make by screen 4?
   - What's the paywall moment — scarcity? social proof? completion?
3. Build ONE variant that embodies that promise end-to-end.
4. Instrument every tap as a funnel event (`onboarding_screen_shown`, `onboarding_screen_completed`) so you can measure drop-off without a second variant.
5. Only branch into A/B when you have real drop-off data pointing at a specific screen.

## Worked example

- Plan: `docs/superpowers/plans/2026-04-09-onboarding-redesign.md` — built 3 variants.
- Plan: `docs/superpowers/plans/2026-04-12-promise-onboarding.md` — scrapped variants, built one Promise flow.
- Commit trail: variants live in history but current app ships a single flow.

## Anti-patterns

- "We'll split-test discipline vs. health messaging" — you can't measure that without traffic.
- Paywall inherited from a boilerplate without positioning work — converts at random.

## Related

- L-PRC-002 — One plan per feature (this is product planning, not engineering planning)
