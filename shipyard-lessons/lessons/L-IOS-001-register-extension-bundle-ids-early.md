---
id: L-IOS-001
title: Register every extension bundle ID in Apple Developer Portal in week 1
severity: critical
category: deployment
platforms: [ios-swiftui]
tags: [screen-time, family-controls, extensions, testflight, entitlements]
polarity: require
applies_when: "Project uses FamilyControls, DeviceActivity, ManagedSettings, WidgetKit, or any app extension"
source_project: runlock
learned_at: 2026-04-17
last_verified: 2026-04-17
supersedes: []
superseded_by: null
---

## Pattern
Every app-extension target has its own bundle identifier and needs its own registration in Apple Developer Portal plus its own entitlement requests (Family Controls, App Groups, Push, etc.). Register them the week you scaffold the project, not the week you cut the TestFlight build.

## Why it matters
Entitlement approvals (especially Family Controls) are manual and non-instant at Apple. If you discover a missing registration on release day, you either wait or ship without the extension — which means disabling features that were already built. `chore: temporarily disable RunlockShieldAction target for TestFlight build` is that exact scar.

## Detect

```shell
# detect: PRESENT=0 if every non-test target in project.yml has a matching entitlements file, ABSENT=1 otherwise
python3 - <<'PY'
import re, os, glob, sys
yml = open("project.yml").read() if os.path.exists("project.yml") else ""
targets = re.findall(r"^  ([A-Z][A-Za-z0-9]+):\s*\n    type:", yml, re.M)
ok = True
for t in targets:
    if t.endswith("Tests") or t.endswith("UITests"): continue
    ent = glob.glob(f"{t}/*.entitlements")
    if not ent:
        print(f"MISSING entitlements for target: {t}")
        ok = False
sys.exit(0 if ok else 1)
PY
```

## Fix

1. List every target in `project.yml` (main app + each extension + widget).
2. For each one that's missing, register its bundle ID in https://developer.apple.com/account/resources/identifiers.
3. Enable required capabilities per target (Family Controls, App Groups, HealthKit, Push, etc.).
4. Create / fill the `<Target>/<Target>.entitlements` file with matching keys.
5. Re-run `xcodegen` and a release build to confirm signing succeeds.
6. For Family Controls specifically, submit the entitlement request form and expect 1-5 day turnaround.

## Worked example

- Commit: `6542c3d chore: temporarily disable RunlockShieldAction target for TestFlight build` — exactly this mistake.
- File: `project.yml` — see the commented `RunlockShieldAction:` block with re-enable instructions.
- Targets that each need registration: `Runlock`, `RunlockWidget`, `RunlockMonitor`, `RunlockShield`, `RunlockShieldAction`.

## Anti-patterns

- Registering only the main app bundle ID and assuming extensions inherit.
- Waiting until the signing failure at build time to discover which capability is missing.

## Related

- L-IOS-002 — App Groups entitlement on every extension target
