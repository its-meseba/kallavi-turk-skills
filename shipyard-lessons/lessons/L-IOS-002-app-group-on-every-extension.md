---
id: L-IOS-002
title: Declare the App Group entitlement on every extension target, not just the main app
severity: high
category: platform
platforms: [ios-swiftui]
tags: [app-groups, extensions, widget, userdefaults, cross-target-state]
polarity: require
applies_when: "Project has any app extension (widget, shield, monitor, etc.) that reads shared state"
source_project: runlock
learned_at: 2026-04-17
last_verified: 2026-04-17
supersedes: []
superseded_by: null
---

## Pattern
App extensions run in separate sandboxes. If you want a widget to show the current step count, the shield to show the current goal, or the monitor to write progress — every extension target must declare the same App Group in its entitlements file. Use `UserDefaults(suiteName: "group.com.yourapp")` as the I/O bus, not HealthKit/direct storage reads inside the extension.

## Why it matters
A widget without the App Group entitlement compiles and runs but reads nothing — it renders zeros or placeholder data. The bug is silent until a user complains their widget is empty. This is the most common "why is my widget broken" cause.

## Detect

```shell
# detect: PRESENT=0 if every extension entitlements file declares the app group, ABSENT=1 otherwise
python3 - <<'PY'
import glob, sys
ents = glob.glob("*/**.entitlements", recursive=True)
missing = []
for e in ents:
    body = open(e).read()
    if "com.apple.security.application-groups" not in body:
        missing.append(e)
sys.exit(0 if not missing else (print("\n".join(f"MISSING app group: {m}" for m in missing)) or 1))
PY
```

## Fix

1. Choose one App Group id: `group.com.<company>.<app>`.
2. In each target's `.entitlements`, add:
   ```xml
   <key>com.apple.security.application-groups</key>
   <array><string>group.com.company.app</string></array>
   ```
3. In Apple Developer Portal, enable App Groups capability on each bundle ID and add them to the group.
4. In shared code (e.g. `Shared/SharedDefaults.swift`), expose a single `UserDefaults(suiteName:)` helper and route ALL cross-target reads/writes through it.
5. When the main app writes something the widget needs (goal, step count, blocked apps selection), write it to the suite defaults and call `WidgetCenter.shared.reloadAllTimelines()`.

## Worked example

- File: `Runlock/Config/SharedDefaults.swift` — single source of truth for the group suite.
- Every entitlements file in the project declares `group.com.lumiostudio.runlock`.
- The widget reads step count from the suite, never from HealthKit directly.

## Anti-patterns

- Using `UserDefaults.standard` in a widget — it reads the widget's own sandbox, not the app's.
- Duplicating the App Group constant as a string literal in multiple targets — put it in `Shared/`.

## Related

- L-IOS-001 — Register extension bundle IDs early
- L-IOS-004 — Use a `Shared/` folder for cross-target code
