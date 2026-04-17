---
id: L-IOS-004
title: Put cross-target code in a top-level Shared/ folder referenced by every target
severity: medium
category: architecture
platforms: [ios-swiftui]
tags: [extensions, xcodegen, modularity, dry]
polarity: require
applies_when: "Project has ≥2 targets (main app + at least one extension)"
source_project: runlock
learned_at: 2026-04-17
last_verified: 2026-04-17
supersedes: []
superseded_by: null
---

## Pattern
Create a top-level `Shared/` folder and add it to the `sources:` list of every target in `project.yml`. Keep shared constants (App Group id, suite keys, color tokens, localized string keys, model types) in that folder. The compiler treats the files as part of each target, so there's zero DI plumbing.

## Why it matters
Without this, each extension target duplicates constants as string literals — the widget hardcodes `"group.com.app"`, the shield hardcodes `"group.com.app"`, the main app hardcodes `"group.com.app"`. One typo breaks the widget silently. A single `SharedConstants.swift` prevents that entire class of bug.

## Detect

```shell
# detect: PRESENT=0 if a Shared/ folder exists and is referenced by multiple targets in project.yml
test -d Shared && grep -c "path: Shared" project.yml 2>/dev/null | awk '{ exit ($1 >= 2 ? 0 : 1) }'
```

## Fix

1. Create `Shared/` at the repo root.
2. Move shared types into it: `SharedConstants.swift`, `SharedDefaults.swift`, theme tokens, model types used by widget/shield.
3. In `project.yml`, add to every target's `sources:`:
   ```yaml
   sources:
     - path: Shared
     - path: Runlock
   ```
4. Re-run `xcodegen` and verify all targets build.
5. Grep for remaining duplicated literals (`group.com.`, bundle IDs) and fold them into shared constants.

## Worked example

- Folder: `Shared/` at repo root.
- `project.yml`: every target (`Runlock`, `RunlockWidget`, `RunlockMonitor`, `RunlockShield`) lists `- path: Shared` first.

## Anti-patterns

- Creating an SPM local package for 3 constants — overkill for a 1-app repo.
- Symlinking files across target folders — breaks xcodegen regeneration.

## Related

- L-IOS-002 — App Group entitlement on every extension
