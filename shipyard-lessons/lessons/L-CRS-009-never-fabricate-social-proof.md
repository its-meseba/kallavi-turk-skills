---
id: L-CRS-009
title: Never fabricate social proof — no fake user counts, downloads, or testimonials
severity: high
category: product
platforms: [ios-swiftui, android-kotlin, flutter, react-native-expo]
tags: [aso, marketing, ethics, trust, app-store-review]
polarity: avoid
applies_when: "Writing ASO copy, onboarding screens, paywall copy, or landing page content"
source_project: runlock
learned_at: 2026-04-16
last_verified: 2026-04-17
supersedes: []
superseded_by: null
---

## Mistake
Writing "Join 50,000 users" or "4.9 stars from 10,000 reviews" before those numbers are real. Pulling fake testimonial names off the internet. Adding a "Featured in TechCrunch" badge without the coverage.

## Why it matters
Beyond ethics: App Store and Play Store reviewers check. Fake social proof triggers rejection, demotion, or removal. And if your product takes off, the fake numbers become the ceiling — you can't say "200k users" for a year and then reveal you have 8k.

## Detect

- [ ] Do any user-count, download-count, or review-count claims in the UI correspond to real, current data sources?
- [ ] Are testimonials attributed to real users who gave permission?
- [ ] Do "as featured in" logos correspond to actual press coverage you can link?

## Fix

1. Replace specific fabricated numbers with honest alternatives:
   - "Join a growing community" (no number) > "Join 50,000 users" (fake number).
   - Real App Store rating (even 4.3) > fake 5.0.
2. Gate social-proof UI behind a config flag that's empty by default and populated only from live data.
3. When you do have real numbers, update them from a data source (PostHog count, ASC reviews API, internal metrics) — don't hardcode.
4. For launch, use benefit-driven copy instead of social proof: "Lock apps. Walk. Unlock." beats "10,000 users trust us."

## Worked example

- Memory record: `feedback_no_fake_numbers.md` — user correction during ASO screenshot generation.
- Runlock's TR screenshots use imperative headlines (KİLİTLE / YÜRÜ / SEÇ / TAKİP ET / MEYDAN OKU) with zero fabricated numbers.

## Anti-patterns

- "Downloaded by 1M+ users" on a pre-launch landing page.
- Stock photos presented as customer testimonials.

## Related

- L-CRS-010 — Localization is copywriting (applies to ASO copy too)
