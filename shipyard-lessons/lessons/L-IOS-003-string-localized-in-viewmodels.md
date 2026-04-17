---
id: L-IOS-003
title: Return String(localized:) from ViewModels and Services, never raw English strings
severity: high
category: localization
platforms: [ios-swiftui]
tags: [localization, xcstrings, viewmodel, service]
polarity: avoid
applies_when: "Project targets >1 locale and has ViewModels/Services that return user-facing Strings"
source_project: runlock
learned_at: 2026-04-17
last_verified: 2026-04-17
supersedes: []
superseded_by: null
---

## Mistake
Returning raw English strings like `return "Great job!"` from a ViewModel, Service, or Model. SwiftUI's `Text("key")` auto-extracts to the string catalog; a raw Swift `String` does not. Non-English users see English.

## Why it matters
The bug is invisible during Swift compilation and Xcode doesn't flag it — Xcode's catalog extractor only runs on `Text(...)`, `LocalizedStringKey`, and `String(localized:)`. Every `String` return path from non-View code is a localization leak. We shipped 3 locales but several leaks reached users.

## Detect

```shell
# detect: PRESENT=0 if no bare string literals returned from ViewModels/Services, ABSENT=1 otherwise
# Flags `return "SomeText"` in any non-View Swift file
python3 - <<'PY'
import glob, re, sys
pattern = re.compile(r'return\s+"[A-Z][^"]{3,}"')
hits = []
for f in glob.glob("**/*.swift", recursive=True):
    if "/Views/" in f or f.endswith("View.swift"): continue
    if "Test" in f or "Mock" in f: continue
    for i, line in enumerate(open(f, errors="ignore"), 1):
        if pattern.search(line) and "String(localized:" not in line:
            hits.append(f"{f}:{i}: {line.strip()}")
print("\n".join(hits))
sys.exit(0 if not hits else 1)
PY
```

## Fix

1. For each hit, replace `return "Some text"` with `return String(localized: "semantic_key")`.
2. Add the key to `Resources/Localizable.xcstrings` with source (EN) + every target locale.
3. Add a CLAUDE.md rule enforcing this (human-readable) AND a lint check (CI-enforced) so it doesn't regress.
4. For plural/formatted strings, use `String(localized: "key_\(count)_items")` with xcstrings variations.

## Worked example

- Rule: `CLAUDE.md` → `MANDATORY_LOCALIZATION` section.
- Fix sweep commit: `78f2313 feat: goal celebration system, enhanced progress ring, complete localization`.
- Catalog: `Runlock/Resources/Localizable.xcstrings` — 308 keys × 3 locales.

## Anti-patterns

- Storing strings in Swift enums: `case good = "Great job"` — bypasses localization.
- Using `NSLocalizedString(_:)` inconsistently alongside `String(localized:)` — pick one.
- Building the English string with interpolation then passing to `String(localized:)` — breaks extraction.

## Related

- L-IOS-006 — Prefer `.xcstrings` over `.strings`
- L-CRS-010 — Localization is copywriting per locale
