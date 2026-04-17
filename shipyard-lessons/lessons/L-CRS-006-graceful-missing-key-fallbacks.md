---
id: L-CRS-006
title: Ship graceful fallbacks for missing SDK API keys from day one
severity: high
category: sdk
platforms: [ios-swiftui, android-kotlin, flutter, react-native-expo]
tags: [sdk, api-keys, dev-experience, onboarding-new-devs]
polarity: require
applies_when: "Project integrates SDKs whose keys live in env/config files"
source_project: runlock
learned_at: 2026-04-12
last_verified: 2026-04-17
supersedes: []
superseded_by: null
---

## Pattern
Every SDK initialization reads its key from a config source. If the key is empty, nil, or a placeholder, the service logs `"<SDK>: key missing, skipping initialization"` and becomes a no-op. The app continues to run. No crash. No blocker for a dev opening the repo for the first time.

## Why it matters
A dev #2 opens the project, runs it, and crashes on first launch because `AppsFlyer.dev.key` wasn't in their `.env`. Onboarding new contributors requires 15 minutes of "wait, where's the AppsFlyer key?" Shared keys in a repo = security risk; missing keys with no fallback = dev friction. Graceful fallback resolves both.

## Detect

```shell
# detect: PRESENT=0 if SDK services check for empty keys before init, ABSENT=1 otherwise
python3 - <<'PY'
import glob, re, sys
# Look for any *Service.{swift,kt,dart,ts} that mentions an SDK but never checks empty/nil/null keys
sdk_names = ["PostHog", "Adapty", "AppsFlyer", "Meta", "Facebook", "Superwall", "Mixpanel", "Amplitude"]
violations = []
for ext in ("swift","kt","dart","ts","tsx"):
    for f in glob.glob(f"**/*Service.{ext}", recursive=True):
        try: src = open(f, errors="ignore").read()
        except: continue
        if not any(s in src for s in sdk_names): continue
        if "isEmpty" not in src and "== nil" not in src and ".empty" not in src and "=== null" not in src and '== ""' not in src:
            violations.append(f)
for v in violations: print(f"NO FALLBACK CHECK: {v}")
sys.exit(0 if not violations else 1)
PY
```

## Fix

1. In each SDK service's `start()` method, add a guard:
   ```swift
   guard !AppConfig.postHogKey.isEmpty,
         AppConfig.postHogKey != "REPLACE_ME" else {
     print("[PostHog] Key missing — service disabled")
     return
   }
   ```
2. Make every router dispatch a no-op when its underlying provider never started.
3. In `AppConfig`, default every key to an empty string (not to a committed placeholder that looks real).
4. Add a one-time console summary on launch: `[Shipyard] Active SDKs: PostHog, Adapty. Disabled: AppsFlyer, Meta.`

## Worked example

- Commit: `7febd1e feat: graceful SDK fallbacks when API keys are not yet set`.
- File: `Runlock/Services/PostHogService.swift` — guards at `start()`.

## Anti-patterns

- Force-unwrapping the key: `PostHog.start(key: AppConfig.postHogKey!)` — crash on missing key.
- Committing a "dev" key to the repo as the fallback — security hazard and analytics pollution.

## Related

- L-CRS-001 — Lazy SDK init
- L-CRS-005 — AnalyticsRouter fan-out
