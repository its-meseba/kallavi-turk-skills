---
id: L-CRS-005
title: Route all analytics through a single AnalyticsRouter that fans out to providers
severity: critical
category: architecture
platforms: [ios-swiftui, android-kotlin, flutter, react-native-expo]
tags: [analytics, router, fan-out, posthog, firebase, meta, appsflyer]
polarity: require
applies_when: "Project integrates ≥2 analytics providers (PostHog, Firebase, Meta, AppsFlyer, Mixpanel, Amplitude)"
source_project: runlock
learned_at: 2026-04-11
last_verified: 2026-04-17
supersedes: []
superseded_by: null
---

## Pattern
One enum of event cases is the single source of truth. One router method `track(_ event:)` fans out to every provider. Individual SDK services are `private` — no ViewModel ever imports PostHog, Firebase, Meta, or AppsFlyer directly.

```
Views → ViewModels → AnalyticsRouter → [Firebase, PostHog, Meta, AppsFlyer]
```

## Why it matters
Without this, every feature touches 4 SDKs, event names drift (`goal_reached` vs `goalReached` vs `goal.reached`), and privacy gating (ATT, GDPR) has to be re-implemented per provider. With it, adding a provider is one switch case; removing one is deleting one destination method.

## Detect

```shell
# detect: PRESENT=0 if an AnalyticsRouter exists and providers are private, ABSENT=1 otherwise
python3 - <<'PY'
import glob, re, sys
router = None
for f in glob.glob("**/*.{swift,kt,dart,ts,tsx}", recursive=True, flags=0) if hasattr(__builtins__, "glob") else glob.glob("**/*Analytics*", recursive=True):
    if "AnalyticsRouter" in f or "analytics-router" in f.lower():
        router = f; break
# Lightweight fallback
if router is None:
    for ext in ("swift","kt","dart","ts","tsx"):
        for f in glob.glob(f"**/*.{ext}", recursive=True):
            try:
                if "AnalyticsRouter" in open(f, errors="ignore").read():
                    router = f; break
            except: pass
        if router: break
if not router:
    print("MISSING: no AnalyticsRouter found"); sys.exit(1)
# Check for direct SDK calls outside the router
leaks = []
for ext in ("swift","kt","dart","ts","tsx"):
    for f in glob.glob(f"**/*.{ext}", recursive=True):
        if f == router or "Router" in f or "Test" in f or "node_modules" in f: continue
        try: src = open(f, errors="ignore").read()
        except: continue
        for pat in ("PostHogSDK.shared.capture", "Analytics.logEvent(", "AppEventsLogger.log", "AppsFlyerLib.shared().trackEvent", "posthog.capture("):
            if pat in src: leaks.append(f"{f}: {pat}")
for l in leaks[:10]: print(f"LEAK: {l}")
sys.exit(0 if not leaks else 1)
PY
```

## Fix

1. Create `AnalyticsRouter.swift` (or `.kt`, `.dart`, `.ts`) with:
   - An enum of every event case (with associated properties).
   - One `track(_ event:)` method.
   - Private instances of each provider service.
2. Move every provider SDK service to `private` visibility.
3. Grep for direct calls outside the router (`PostHogSDK.shared.capture`, `Analytics.logEvent`, `AppEventsLogger.log`, `AppsFlyerLib.shared().trackEvent`) and route them through the router.
4. Standardize event name format: `snake_case` for PostHog, auto-map to provider-native on the way out.
5. Centralize consent / ATT gating: the router checks consent before dispatching.

## Worked example

- Refactor commit: `d4abdad refactor: route all analytics through AnalyticsRouter, add feature flags, set AppsFlyer App ID`.
- File: `Runlock/Services/AnalyticsRouter.swift`.

## Anti-patterns

- One router per provider ("PostHogRouter") — that's not a router.
- Calling `router.track("goal_reached")` with a string — lose compile-time safety of the enum.

## Related

- L-CRS-001 — Lazy SDK init
- L-CRS-006 — Graceful missing-key fallbacks
