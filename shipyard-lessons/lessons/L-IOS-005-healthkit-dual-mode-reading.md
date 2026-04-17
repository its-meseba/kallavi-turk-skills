---
id: L-IOS-005
title: Read HealthKit in two modes — foreground observers and background delivery
severity: high
category: platform
platforms: [ios-swiftui]
tags: [healthkit, background, battery, steps]
polarity: require
applies_when: "Project reads HealthKit quantity data (steps, heart rate, etc.) used in live UI"
source_project: runlock
learned_at: 2026-04-17
last_verified: 2026-04-17
supersedes: []
superseded_by: null
---

## Pattern
A HealthKit-driven UI needs two reading modes that don't overlap:
1. **Foreground**: `HKObserverQuery` + `HKAnchoredObjectQuery` for real-time updates while the user watches the screen.
2. **Background**: `enableBackgroundDelivery(for:frequency:)` + `HKStatisticsQuery` polled every 5-15 min to update widgets, notifications, and shield state.

Keep them in one service (`StepTrackingService`) with distinct methods. Don't try to make one query do both.

## Why it matters
One query doing both = battery drain (too-aggressive polling in background) or stale widget data (too-passive foreground updates). Widgets that show old step counts break the product promise — "you have to walk to unlock" — because the unlock trigger lags reality.

## Detect

- [ ] Service has distinct methods for foreground observation vs background polling.
- [ ] `HKHealthStore.enableBackgroundDelivery` is called once, during authorization grant.
- [ ] Widget reads from `UserDefaults(suiteName:)` (App Group), not HealthKit directly.
- [ ] Background poll frequency is `.hourly` or coarser — not `.immediate` for non-critical data.

## Fix

1. Split `StepTrackingService` into foreground API (returns `AsyncStream<Int>`) and background API (callback on delivery).
2. Call `enableBackgroundDelivery(for: .stepCount, frequency: .hourly)` inside the authorization success handler.
3. Implement `HKObserverQuery` handler that writes latest step count to the App Group suite and calls `WidgetCenter.shared.reloadAllTimelines()`.
4. Register a `BGAppRefreshTask` that re-runs the stats query when the OS wakes the app.
5. In the widget extension, read from the suite — never import HealthKit into the widget.

## Worked example

- Service: `Runlock/Services/StepTracking/` — foreground observer + background delivery.
- Widget reads `UserDefaults(suiteName: "group.com.lumiostudio.runlock")` only.

## Anti-patterns

- Polling HealthKit every 30 seconds in foreground (battery killer, and iOS throttles it anyway).
- Importing `HealthKit` in a widget target (it works but spikes memory and hits iOS widget memory caps).

## Related

- L-IOS-002 — App Groups for widget state
