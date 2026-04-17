---
id: L-CRS-007
title: A share/challenge loop needs all four pieces — UI + deep link + landing page + backend
severity: high
category: product
platforms: [ios-swiftui, android-kotlin, flutter, react-native-expo]
tags: [virality, universal-links, deep-linking, landing-page, share-sheet]
polarity: require
applies_when: "Product has a share, challenge, referral, or invite feature"
source_project: runlock
learned_at: 2026-04-16
last_verified: 2026-04-17
supersedes: []
superseded_by: null
---

## Pattern
A share loop that crosses the App Store wall needs four cooperating pieces:
1. **In-app UI** to create the share payload (button, story card renderer, share sheet).
2. **Deep link** (Universal Links on iOS, App Links on Android) with a registered AASA / asset-links file.
3. **Landing page** that (a) renders a preview for users without the app installed, (b) redirects installed users into the app, (c) sends uninstalled users to the store.
4. **Backend** (Firestore, KV, Postgres — whatever) so the landing page can render the shared artifact's state.

Missing any one = dead share flow.

## Why it matters
Runlock's viral features commit (`f8b7274`) shipped the UI. The challenge flow didn't actually work until the landing page (`8945117`) and the backend wiring (`1703488`) landed days later. Story cards look great in Figma and die in the wild without the other three pieces.

## Detect

- [ ] AASA file (`apple-app-site-association`) served at `https://<domain>/.well-known/apple-app-site-association` with correct `appID`.
- [ ] Android `assetlinks.json` at `https://<domain>/.well-known/assetlinks.json`.
- [ ] Associated Domains entitlement includes `applinks:<domain>` on iOS.
- [ ] App delegate / SwiftUI `.onOpenURL` handler parses the incoming URL.
- [ ] Landing page exists and reads the shared artifact (e.g., challenge) from the backend by ID.
- [ ] Landing page shows App Store / Play Store buttons for users without the app.
- [ ] OG/Twitter meta tags on the landing page render a preview on social platforms.

## Fix

1. Set up the landing page first (Next.js + Vercel is the 2-hour path).
2. Serve the two well-known files. Validate with Apple's `https://search.developer.apple.com/appsearch-validation-tool/`.
3. Add the Associated Domains entitlement and the `applinks:` entry.
4. Write a minimal URL router: `/c/<challenge-id>` → landing reads Firestore → renders preview.
5. In-app, handle `.onOpenURL` (SwiftUI) / `Linking` (RN) / `uni_links` (Flutter) / intent filters (Android) to open the matching in-app screen.
6. Test the end-to-end flow on TWO devices — the sharer and a receiver without the app installed.

## Worked example

- Plan: `docs/superpowers/plans/2026-04-16-challenge-flow-and-landing-page.md`.
- Landing: `landing-page/` (Next.js + Vercel).
- Commit chain: `f8b7274 viral UI` → `8945117 landing page` → `1703488 challenge flow with Universal Links` → `fc03bf8 fix: update landing page domain`.

## Anti-patterns

- Shipping the share sheet with a direct App Store link — breaks the post-install deep link.
- Firebase Dynamic Links (retired in 2025) — use Universal Links / App Links directly.

## Related

- L-CRS-010 — Localization is copywriting (the landing page needs locale routing too)
