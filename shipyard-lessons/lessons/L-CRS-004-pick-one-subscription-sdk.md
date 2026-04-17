---
id: L-CRS-004
title: Pick one subscription SDK — never stack StoreKit + RevenueCat + Superwall + Adapty
severity: high
category: sdk
platforms: [ios-swiftui, android-kotlin, flutter, react-native-expo]
tags: [subscriptions, paywall, storekit, adapty, revenuecat, superwall]
polarity: avoid
applies_when: "App has in-app subscriptions or one-time purchases"
source_project: runlock
learned_at: 2026-04-11
last_verified: 2026-04-17
supersedes: []
superseded_by: null
---

## Mistake
Integrating more than one subscription/paywall SDK simultaneously. Each one wraps StoreKit 2 (iOS) or Play Billing (Android) and wants to own receipt validation, webhook delivery, entitlement state, and paywall rendering. Two of them = duplicated receipt storms, conflicting entitlement truth, and analytics event splits across vendors.

## Why it matters
Runlock briefly had `SubscriptionService` (native StoreKit) + `AdaptyService` + `SuperwallService` at the same time. Receipts got double-counted, entitlement state diverged between Adapty and native, and the analytics router had to dedupe `purchase_completed` events from three sources. Consolidation was a forced refactor.

## Detect

```shell
# detect: PRESENT=0 if ≤1 subscription SDK is integrated, ABSENT=1 if multiple
python3 - <<'PY'
import glob, sys
sdks = {"adapty": False, "revenuecat": False, "superwall": False, "storekit_direct": False}
for f in list(glob.glob("**/*.swift", recursive=True)) + list(glob.glob("**/*.kt", recursive=True)) + list(glob.glob("**/*.dart", recursive=True)) + list(glob.glob("**/*.ts*", recursive=True)):
    if "node_modules" in f or "build" in f: continue
    try: src = open(f, errors="ignore").read()
    except: continue
    if "import Adapty" in src or "adapty_flutter" in src or "@adapty" in src: sdks["adapty"] = True
    if "import RevenueCat" in src or "purchases_flutter" in src or "react-native-purchases" in src: sdks["revenuecat"] = True
    if "import SuperwallKit" in src or "@superwall" in src: sdks["superwall"] = True
    if "import StoreKit" in src and "class" in src and "Service" in src: sdks["storekit_direct"] = True
active = [k for k,v in sdks.items() if v]
print(f"Subscription SDKs active: {active}")
sys.exit(0 if len(active) <= 1 else 1)
PY
```

## Fix

1. Decide the winner. Defaults:
   - **Adapty** if you want paywall builder + A/B + revenue analytics out of the box.
   - **RevenueCat** if you want the most mature entitlement APIs and existing server-side integrations.
   - **Native StoreKit 2 / Play Billing** if you have a tiny catalog and don't need a dashboard.
2. Delete the losing services entirely — not with a feature flag, not with a "might bring it back later" comment. Clean deletion.
3. Move every paywall UI call to the winner's API.
4. Point webhooks (Apple Server Notifications V2 / RTDN) at the winner's endpoint only.
5. Verify entitlement truth in one place: the winner's SDK.

## Worked example

- Commit: `b4a89c8 feat: integrate Meta, PostHog, AppsFlyer, Adapty SDKs` consolidated three paywall stacks into Adapty.
- `Runlock/Services/AdaptyPaywallService.swift` — single entry point.

## Anti-patterns

- "Keep StoreKit as a fallback" — fallback = double-ledger = divergence.
- A/B testing two different subscription SDKs against each other — test paywall copy, not SDKs.

## Related

- L-CRS-001 — Lazy SDK init
- L-CRS-005 — AnalyticsRouter fan-out
