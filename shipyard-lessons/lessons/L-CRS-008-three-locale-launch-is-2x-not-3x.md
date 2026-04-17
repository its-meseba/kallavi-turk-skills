---
id: L-CRS-008
title: Launch in 3 locales from day 1 — the cost is 2x, not 3x
severity: medium
category: localization
platforms: [ios-swiftui, android-kotlin, flutter, react-native-expo]
tags: [localization, i18n, aso, markets]
polarity: require
applies_when: "Target markets include ≥1 non-English region (TR, FR, DE, JP, etc.)"
source_project: runlock
learned_at: 2026-04-14
last_verified: 2026-04-17
supersedes: []
superseded_by: null
---

## Pattern
If the app will support ≥2 languages eventually, set up the localization infrastructure for N+1 languages from commit #1. Adding the 3rd language is a JSON patch (translations only) — same files, same pipeline, no new architecture work.

## Why it matters
The architectural cost of localization (string catalogs, locale routing, RTL readiness, App Store metadata per locale, screenshot generation per locale) is paid once for language #2. Language #3, #4, #5 are translation hours only. Shipping mono-language then retrofitting = doing that architectural work twice.

## Detect

```shell
# detect: PRESENT=0 if project has ≥2 locales configured, ABSENT=1 otherwise
python3 - <<'PY'
import json, glob, sys
locales = set()
for f in glob.glob("**/Localizable.xcstrings", recursive=True):
    try:
        data = json.load(open(f))
        for key, v in data.get("strings", {}).items():
            for loc in v.get("localizations", {}).keys():
                locales.add(loc)
    except: pass
for f in glob.glob("**/values-*/strings.xml", recursive=True):
    loc = f.split("values-")[1].split("/")[0]
    locales.add(loc)
for f in glob.glob("**/l10n/app_*.arb", recursive=True):
    loc = f.split("app_")[1].split(".")[0]
    locales.add(loc)
for f in glob.glob("**/locales/*/translation.json", recursive=True):
    loc = f.split("/locales/")[1].split("/")[0]
    locales.add(loc)
print(f"Locales detected: {sorted(locales)}")
sys.exit(0 if len(locales) >= 2 else 1)
PY
```

## Fix

1. Pick the primary (source) language and 1 secondary locale before any UI code.
2. Set up string catalogs / strings.xml / ARB / i18next with both.
3. Add the ASC / Play Console locale slots for both.
4. Budget a screenshot-generator that accepts a locale parameter — adding a 3rd locale = one CLI run.
5. When it's time for locale #3, it's a translation ticket, not an engineering ticket.

## Worked example

- Commit: `d53547b feat: add French localization, marketing capture system, and onboarding improvements` — added FR as a JSON patch to the existing EN+TR xcstrings. 308 keys × 1 locale = hours of translation.
- Plan: `docs/superpowers/plans/2026-04-14-french-localization-and-screenshots.md` — mostly translation work.

## Anti-patterns

- "We'll localize once we hit product-market fit" — PMF with a 600M-person English-speaking market is very different from PMF with 8B humans. Your TAM is locale-gated.
- Hand-translating in the app — use string catalog files + translation service.

## Related

- L-IOS-003 — String(localized:) in ViewModels
- L-IOS-006 — Prefer xcstrings
- L-CRS-010 — Localization is copywriting per locale
