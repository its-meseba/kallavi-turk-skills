---
id: L-IOS-006
title: Use String Catalogs (.xcstrings) from day one — never .strings files
severity: medium
category: localization
platforms: [ios-swiftui]
tags: [xcstrings, string-catalog, localization, xcode]
polarity: require
applies_when: "Project targets iOS 17+ and needs localization"
source_project: runlock
learned_at: 2026-04-17
last_verified: 2026-04-17
supersedes: []
superseded_by: null
---

## Pattern
`Localizable.xcstrings` (String Catalogs, iOS 17+) beats `Localizable.strings` on every axis: visual editor in Xcode, automatic extraction of `Text(...)` keys, JSON storage (diff-able), built-in pluralization/variations, per-locale translation state tracking. Start here. Don't "migrate later."

## Why it matters
Migrating from `.strings` to `.xcstrings` mid-project means merging 3+ files per locale manually and re-extracting all keys. Starting with xcstrings costs nothing and gives you translation progress at a glance (Xcode shows % complete per locale).

## Detect

```shell
# detect: PRESENT=0 if project uses xcstrings, ABSENT=1 if .strings files are present
if find . -name "*.xcstrings" | grep -q .; then exit 0; fi
if find . -name "Localizable.strings" | grep -q .; then exit 1; fi
exit 1
```

## Fix

1. Create `Resources/Localizable.xcstrings` via Xcode → New File → String Catalog.
2. Add locales: File Inspector → Localizations → +.
3. Delete old `.strings` files after confirming every key migrated.
4. For programmatic keys, use `String(localized: "key", table: nil, bundle: .main)` — Xcode auto-populates the catalog.
5. Review the catalog per-locale state column; translate anything yellow before shipping.

## Worked example

- File: `Runlock/Resources/Localizable.xcstrings` (~6,676 lines, 308 keys × 3 locales).
- Adding French was a JSON patch, not a new file system setup — commit `d53547b`.

## Related

- L-IOS-003 — String(localized:) in ViewModels
- L-CRS-008 — Three-locale launch is 2x not 3x
