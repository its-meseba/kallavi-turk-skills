---
id: L-IOS-007
title: Add every permission usage description to Info.plist on day one, in every locale
severity: critical
category: deployment
platforms: [ios-swiftui]
tags: [info-plist, permissions, privacy, usage-description, app-store]
polarity: require
applies_when: "Project requests any iOS permission (HealthKit, Camera, Notifications, Location, Contacts, Photos)"
source_project: runlock
learned_at: 2026-04-17
last_verified: 2026-04-17
supersedes: []
superseded_by: null
---

## Pattern
iOS rejects or crashes any permission request that doesn't have a matching `NS<Whatever>UsageDescription` in Info.plist. Add them the day you scaffold the project. Localize them alongside the rest of the app — `InfoPlist.xcstrings` or per-locale `InfoPlist.strings`.

## Why it matters
Missing usage descriptions cause immediate crash when the system prompt appears (not when the framework is imported) — so a dev build can look fine until a permission flow runs. App Store Review also rejects apps with generic usage descriptions ("We need this permission"). Write the real reason.

## Detect

```shell
# detect: PRESENT=0 if Info.plist contains usage descriptions for every requested permission, ABSENT=1 otherwise
python3 - <<'PY'
import plistlib, glob, re, sys, os
frameworks_to_keys = {
    "HealthKit": ["NSHealthShareUsageDescription", "NSHealthUpdateUsageDescription"],
    "AVFoundation": ["NSCameraUsageDescription", "NSMicrophoneUsageDescription"],
    "Photos": ["NSPhotoLibraryUsageDescription"],
    "CoreLocation": ["NSLocationWhenInUseUsageDescription"],
    "Contacts": ["NSContactsUsageDescription"],
    "FamilyControls": [],  # authorization via AuthorizationCenter, no NS key
}
needed = set()
for sf in glob.glob("**/*.swift", recursive=True):
    src = open(sf, errors="ignore").read()
    for fw, keys in frameworks_to_keys.items():
        if f"import {fw}" in src:
            needed.update(keys)
plists = glob.glob("**/Info.plist", recursive=True)
present = set()
for p in plists:
    try: present.update(plistlib.load(open(p,"rb")).keys())
    except Exception: pass
# Also check project.yml properties for xcodegen-generated plists
if os.path.exists("project.yml"):
    yml = open("project.yml").read()
    for k in needed:
        if k in yml: present.add(k)
missing = needed - present
for k in sorted(missing): print(f"MISSING: {k}")
sys.exit(0 if not missing else 1)
PY
```

## Fix

1. For each framework your app imports, add the corresponding `NS*UsageDescription` key to Info.plist (or `project.yml` properties block for xcodegen).
2. Write a real, user-facing reason. Not "We need this." Example: "Runlock reads your step count to know when your daily goal is reached and distracting apps can be unlocked."
3. Localize it in `InfoPlist.xcstrings` or per-locale `InfoPlist.strings`.
4. Test the first-launch flow on a fresh simulator — every permission prompt must show your text, not the system default.

## Worked example

- `project.yml` Info.plist properties block for HealthKit + Notifications usage.
- Family Controls uses `AuthorizationCenter.shared.requestAuthorization(for: .individual)` — no Info.plist key needed, but the app still needs the entitlement.

## Anti-patterns

- Generic text: "We need access to X." — App Store will reject.
- English-only descriptions — the system prompt is always localized; missing translations look unprofessional.

## Related

- L-IOS-001 — Extension bundle IDs
- L-IOS-008 — @Observable ViewModels
