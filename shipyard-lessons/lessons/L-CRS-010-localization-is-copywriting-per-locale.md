---
id: L-CRS-010
title: Localization is copywriting per locale, not 1:1 translation
severity: medium
category: localization
platforms: [ios-swiftui, android-kotlin, flutter, react-native-expo]
tags: [localization, aso, copy, tone, culture]
polarity: require
applies_when: "Shipping app in ≥2 locales, especially ASO copy / onboarding / paywall"
source_project: runlock
learned_at: 2026-04-16
last_verified: 2026-04-17
supersedes: []
superseded_by: null
---

## Pattern
High-impact copy (App Store screenshots, paywall headlines, onboarding hero lines, notification bodies) must be written natively per locale — not machine-translated, not 1:1 from English. The emotional register, word order, cultural hooks, and verb tense differ. Hire a native speaker or at minimum use a localization service with marketing-copy expertise.

## Why it matters
A line that converts in English flops in Turkish if you translate it literally. Imperative-first verbs work in Turkish ASO ("KİLİTLE / YÜRÜ") but sound harsh in English ("LOCK / WALK"). Softeners that work in Japanese are absent in German. Automated translation produces grammatically correct but emotionally flat copy → lower store conversion → lower install rate.

## Detect

- [ ] Is marketing copy (ASO, paywall, onboarding headlines) in `xcstrings`/`strings.xml`/`.arb`/`i18n` files reviewed by a native speaker per locale?
- [ ] Do screenshot copies for each locale use locale-native phrasing (not literal translations)?
- [ ] Does the notification service use `stringsdict` / plural variations for languages with complex plurals (Russian, Polish, Arabic)?

## Fix

1. Identify "hot" strings: ASO metadata, paywall headlines, onboarding hero lines, notification bodies, share card overlays. Everything else can be straight translation.
2. For each hot string, write a brief: "promise, emotion, audience." Give that + English source to the native-speaker translator.
3. Store translated variants in the catalog with `varies_by: locale` notes when the phrasing is not a direct translation.
4. Add a per-locale review checklist before every submission.

## Worked example

- Memory record: `aso_benefits.md` — Turkish headlines: KİLİTLE / YÜRÜ / SEÇ / TAKİP ET / MEYDAN OKU (imperative, verb-first). English equivalents would use different sentence structures.
- Plan: `docs/superpowers/plans/2026-04-14-french-localization-and-screenshots.md` — FR copy was re-written for ASO, not translated.

## Anti-patterns

- Running the whole catalog through DeepL/Google Translate and shipping — works for settings screens, fails for ASO.
- One "international" copy for everything that isn't English.

## Related

- L-CRS-008 — Three-locale launch is 2x not 3x
- L-CRS-009 — Never fabricate social proof (which is localized too)
