# Shipyard Lessons — Master Index

Every lesson in `lessons/`, one row. Scan this table to see what applies to the current project, then open the individual file for `Detect` / `Fix` / worked examples.

**Last updated:** 2026-04-17
**Total lessons:** 22 (seeded from runlock)

## Table

| ID | Severity | Category | Platforms | Polarity | Title |
|---|---|---|---|---|---|
| [L-IOS-001](lessons/L-IOS-001-register-extension-bundle-ids-early.md) | critical | deployment | ios-swiftui | require | Register every extension bundle ID in Apple Developer Portal in week 1 |
| [L-IOS-002](lessons/L-IOS-002-app-group-on-every-extension.md) | high | platform | ios-swiftui | require | Declare the App Group entitlement on every extension target, not just the main app |
| [L-IOS-003](lessons/L-IOS-003-string-localized-in-viewmodels.md) | high | localization | ios-swiftui | avoid | Return String(localized:) from ViewModels and Services, never raw English strings |
| [L-IOS-004](lessons/L-IOS-004-shared-folder-for-extension-code.md) | medium | architecture | ios-swiftui | require | Put cross-target code in a top-level Shared/ folder referenced by every target |
| [L-IOS-005](lessons/L-IOS-005-healthkit-dual-mode-reading.md) | high | platform | ios-swiftui | require | Read HealthKit in two modes — foreground observers and background delivery |
| [L-IOS-006](lessons/L-IOS-006-prefer-xcstrings-over-strings.md) | medium | localization | ios-swiftui | require | Use String Catalogs (.xcstrings) from day one — never .strings files |
| [L-IOS-007](lessons/L-IOS-007-info-plist-usage-strings-day-one.md) | critical | deployment | ios-swiftui | require | Add every permission usage description to Info.plist on day one, in every locale |
| [L-CRS-001](lessons/L-CRS-001-lazy-sdk-init-order.md) | critical | sdk | all | require | Initialize every third-party SDK lazily — never eagerly in property initializers |
| [L-CRS-002](lessons/L-CRS-002-centralize-design-tokens-before-any-views.md) | high | design | all | require | Centralize design tokens (colors, radii, spacing) before writing any view |
| [L-CRS-003](lessons/L-CRS-003-onboarding-psychology-before-variants.md) | high | product | all | require | Run a psychology / positioning pass before building onboarding variants |
| [L-CRS-004](lessons/L-CRS-004-pick-one-subscription-sdk.md) | high | sdk | all | avoid | Pick one subscription SDK — never stack StoreKit + RevenueCat + Superwall + Adapty |
| [L-CRS-005](lessons/L-CRS-005-analytics-router-fan-out.md) | critical | architecture | all | require | Route all analytics through a single AnalyticsRouter that fans out to providers |
| [L-CRS-006](lessons/L-CRS-006-graceful-missing-key-fallbacks.md) | high | sdk | all | require | Ship graceful fallbacks for missing SDK API keys from day one |
| [L-CRS-007](lessons/L-CRS-007-virality-needs-all-four-pieces.md) | high | product | all | require | A share/challenge loop needs all four pieces — UI + deep link + landing page + backend |
| [L-CRS-008](lessons/L-CRS-008-three-locale-launch-is-2x-not-3x.md) | medium | localization | all | require | Launch in 3 locales from day 1 — the cost is 2x, not 3x |
| [L-CRS-009](lessons/L-CRS-009-never-fabricate-social-proof.md) | high | product | all | avoid | Never fabricate social proof — no fake user counts, downloads, or testimonials |
| [L-CRS-010](lessons/L-CRS-010-localization-is-copywriting-per-locale.md) | medium | localization | all | require | Localization is copywriting per locale, not 1:1 translation |
| [L-PRC-001](lessons/L-PRC-001-ship-wreck-review-same-day.md) | high | process | all | require | Run a ship-wreck review commit after every major feature, same day |
| [L-PRC-002](lessons/L-PRC-002-one-plan-per-feature-15-30kb.md) | medium | process | all | require | One plan per feature — 15-30 KB sweet spot, task checklist format |
| [L-PRC-003](lessons/L-PRC-003-revert-experiments-same-day.md) | medium | process | all | require | Revert failed experiments the same day — don't defend a bad 4-hour investment |
| [L-PRC-004](lessons/L-PRC-004-no-update-commits.md) | low | process | all | avoid | Never commit with just "update" as the message — it signals lost context |
| [L-PRC-005](lessons/L-PRC-005-plan-build-review-commit-loop.md) | critical | process | all | require | Run the Plan → Build → Ship-Wreck Review → Commit loop every day |

## By category

- **architecture**: L-IOS-004, L-CRS-005
- **deployment**: L-IOS-001, L-IOS-007
- **design**: L-CRS-002
- **localization**: L-IOS-003, L-IOS-006, L-CRS-008, L-CRS-010
- **platform**: L-IOS-002, L-IOS-005
- **process**: L-PRC-001, L-PRC-002, L-PRC-003, L-PRC-004, L-PRC-005
- **product**: L-CRS-003, L-CRS-007, L-CRS-009
- **sdk**: L-CRS-001, L-CRS-004, L-CRS-006

## By platform

- **ios-swiftui**: L-IOS-* (7) + L-CRS-* + L-PRC-*
- **android-kotlin**: L-CRS-* + L-PRC-* (Android-specific lessons pending — add via `/shipyard:learn-lessons`)
- **flutter**: L-CRS-* + L-PRC-* (Flutter-specific lessons pending)
- **react-native-expo**: L-CRS-* + L-PRC-* (RN-specific lessons pending)

## Source projects

| Project | Lessons contributed | Date range |
|---|---|---|
| runlock (iOS Screen Time app) | 22 (all current) | 2026-04-08 → 2026-04-17 |
