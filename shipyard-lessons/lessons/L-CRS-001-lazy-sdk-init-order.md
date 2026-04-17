---
id: L-CRS-001
title: Initialize every third-party SDK lazily — never eagerly in property initializers
severity: critical
category: sdk
platforms: [ios-swiftui, android-kotlin, flutter, react-native-expo]
tags: [sdk, initialization, crash, firebase, posthog, adapty]
polarity: require
applies_when: "Project integrates ≥1 third-party SDK"
source_project: runlock
learned_at: 2026-04-11
last_verified: 2026-04-17
supersedes: []
superseded_by: null
---

## Pattern
Never instantiate SDK clients as stored properties that initialize at type-load time. Wrap each SDK behind a service with a lazy getter and an explicit `start()` method called from `AppViewModel.setup()` (or the platform equivalent). This guarantees ordering: `FirebaseApp.configure()` runs first, Firestore second, PostHog third, etc.

## Why it matters
Eager SDK instantiation triggers framework-level assertions before the app's main entry point has a chance to configure them. Firestore will crash if accessed before `FirebaseApp.configure()`. PostHog will drop events if accessed before the SDK key is set. These crashes happen on first launch — your first user's first impression.

## Detect

```shell
# detect: PRESENT=0 if no eager-init patterns like `static let shared = Firestore.firestore()` exist
python3 - <<'PY'
import glob, re, sys
bad = []
for ext, pat in [("swift", r"(static\s+let\s+shared\s*=\s*(Firestore|Firebase|PostHog|Amplitude|Mixpanel)|Firestore\.firestore\(\)\s*$)"),
                 ("kt", r"(val\s+\w+\s*=\s*(FirebaseFirestore|PostHog)\.getInstance\(\))"),
                 ("dart", r"(final\s+\w+\s*=\s*(FirebaseFirestore|PostHog)\.instance)"),
                 ("ts", r"(const\s+\w+\s*=\s*(getFirestore|PostHog|initializeApp)\()")]:
    for f in glob.glob(f"**/*.{ext}", recursive=True):
        if "node_modules" in f or "build" in f or "Pods" in f: continue
        for i, line in enumerate(open(f, errors="ignore"), 1):
            if re.search(pat, line): bad.append(f"{f}:{i}: {line.strip()}")
print("\n".join(bad))
sys.exit(0 if not bad else 1)
PY
```

## Fix

1. Convert each SDK service from a property initializer to a class with `lazy var` or explicit `start()`.
2. Create a single `AppViewModel.setup()` (iOS) / `Application.onCreate()` (Android) / `main()` bootstrap (Flutter/RN) that calls services in strict order:
   ```
   Firebase.configure()     // always first if using Firebase
   → PostHog.start(key:)
   → Adapty.activate(key:)
   → AppsFlyer.start(key:)
   → AnalyticsRouter.start() // only after all providers exist
   ```
3. Make every SDK accessor `private` — route all calls through `AnalyticsRouter` / `SubscriptionService`.
4. Add a smoke test: launch a clean simulator, watch for any pre-`configure()` framework log.

## Worked example

- Commit: `a3cfdc5 fix: lazy Firestore init to prevent crash before FirebaseApp.configure()` — exactly this class of bug.
- Service: `Runlock/Services/FirebaseService.swift` — lazy accessors, explicit `start()`.

## Anti-patterns

- Injecting Firestore via `@EnvironmentObject` or `@StateObject` of a `FirestoreService()` at the App root — runs before `FirebaseApp.configure()`.
- Using singletons with eager initialization: `static let shared = MyService()`.

## Related

- L-CRS-005 — AnalyticsRouter fan-out
- L-CRS-006 — Graceful fallbacks for missing API keys
