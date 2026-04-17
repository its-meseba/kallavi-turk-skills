---
id: L-CRS-002
title: Centralize design tokens (colors, radii, spacing) before writing any view
severity: high
category: design
platforms: [ios-swiftui, android-kotlin, flutter, react-native-expo]
tags: [theme, design-tokens, branding, rebrand, tech-debt]
polarity: require
applies_when: "Project has a design identity with brand colors (i.e., always)"
source_project: runlock
learned_at: 2026-04-13
last_verified: 2026-04-17
supersedes: []
superseded_by: null
---

## Pattern
Define a single `Theme` enum/object with semantic color tokens (`primary`, `primaryMuted`, `accent`, `surface`, `onSurface`, `danger`, …) on day one. Every view consumes from it. Every gradient is built from it. No hex literal ever appears in a view file.

## Why it matters
Brand colors change. Runlock started green and finished orange — and the rebrand swept 36 view files because inline hex literals had leaked. One token file = one file changed for a rebrand. 36 view files = a full day of careful sweep + visual QA + risk of missing instances.

## Detect

```shell
# detect: PRESENT=0 if view files contain no raw hex literals for colors, ABSENT=1 otherwise
python3 - <<'PY'
import glob, re, sys
pat = re.compile(r'#[0-9A-Fa-f]{6}|Color\(red:|rgb\(|hex:\s*"')
hits = []
view_exts = {"swift": "/Views/", "kt": "/ui/", "dart": "/screens/", "tsx": "/screens/"}
for ext, view_dir in view_exts.items():
    for f in glob.glob(f"**/*.{ext}", recursive=True):
        if view_dir not in f: continue
        for i, line in enumerate(open(f, errors="ignore"), 1):
            if pat.search(line): hits.append(f"{f}:{i}")
for h in hits[:20]: print(h)
if len(hits) > 20: print(f"... +{len(hits)-20} more")
sys.exit(0 if not hits else 1)
PY
```

## Fix

1. Create `Config/Theme.swift` (or `ui/theme/Theme.kt`, `theme/theme.dart`, `theme/tokens.ts`) with a single source of semantic tokens.
2. Replace every inline hex literal with `Theme.Colors.primary` etc. Use find/replace in view files first, then a grep sweep for stragglers.
3. Add a Gradients sub-enum for common gradient presets — rebrand = change one file.
4. Add a CI grep that fails the build if a view file contains a hex literal.
5. Export dark-mode variants from the same tokens so theming toggles for free.

## Worked example

- Commit: `2026-04-13-branding-redesign.md` plan — 36 files touched for the green→orange pivot.
- File: `Runlock/Config/Theme.swift` → `RunlockTheme.Colors.primary` token consumed everywhere.

## Anti-patterns

- "We'll extract tokens later" — later = 36-file refactor.
- Per-feature theme files (`OnboardingColors.swift`, `DashboardColors.swift`) — recentralize.

## Related

- L-CRS-003 — Run psychology pass before onboarding variants (same "build right the first time" principle)
