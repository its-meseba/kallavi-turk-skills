# Platform Specs

Quick reference for the three target platforms. Re-verify quarterly; platform specs drift.

## TikTok

- **Dimensions:** 1080×1920 (9:16). 720×1280 acceptable.
- **Duration:** 15s min for decent reach; 21–34s is the algorithmic sweet spot per creator data mid-2026. 60s still fine. Longer is allowed but save rate drops.
- **File size:** 287.6 MB max.
- **Frame rate:** 30 fps recommended.
- **Codec:** H.264, AAC audio.
- **Captions:** bake them in. Auto-captions are opt-in and default off.
- **Hashtags:** 3–5 per post. Mix: 1–2 broad (~M views), 2–3 niche (~100k–1M views), 0–1 trending.
- **Anti-pattern:** don't cross-post with visible TikTok watermark to other platforms; don't use URL shorteners in caption/bio.
- **API for analytics:** TikTok Business API (apply via TikTok for Developers). For posting: use Blotato/Postiz official OAuth; do NOT try direct API integration as an indie without business approval.

## Instagram Reels

- **Dimensions:** 1080×1920 (9:16).
- **Duration:** 15–90s. Algorithmic sweet spot is 15–30s per Meta Business guidance.
- **File size:** 4 GB max.
- **Frame rate:** 30 fps (60 fps downscales).
- **Codec:** H.264, AAC.
- **Captions:** bake in. IG auto-captions exist but inconsistent.
- **Hashtags:** 3–5 in the caption, or put them in the first comment (tools like Blotato support first-comment posting).
- **Link in caption:** not clickable. Bio link is the only click surface — use a link-in-bio page.
- **Anti-pattern:** don't post the same Reel verbatim to multiple accounts — IG algorithmic dup detection is aggressive.
- **API:** Meta Graph API for IG — requires a connected Facebook Page + IG Business account.

## YouTube Shorts

- **Dimensions:** 1080×1920 (9:16). Will accept square/landscape; 9:16 is the only one that gets Shorts treatment.
- **Duration:** up to 60 seconds for Shorts designation. Above 60s becomes a regular video.
- **File size:** no hard limit for Shorts uploads via official apps.
- **Frame rate:** 30/60 fps.
- **Codec:** H.264, AAC.
- **Captions:** YT auto-captions are decent. Still recommended to bake in for style.
- **Hashtags:** use `#Shorts` explicitly in title or description. Plus 2–3 content-relevant tags.
- **Link:** clickable in description (below the fold on mobile — often missed). Pinned comment works better as CTA.
- **API:** YouTube Data API v3 for upload + analytics.

## Cross-platform considerations

### Audio on Reels/Shorts vs TikTok

- TikTok rewards **original sounds** heavily — even repurposed content, use an "Original sound" posture.
- Reels discourages TikTok-watermarked content and sounds pulled from TikTok.
- Shorts: music library is copyright-safer.

### Captions

One burned-in caption file works across all three. Don't maintain platform-specific captions unless the VO language differs.

### Durations

If targeting all three, optimize for **21–27 seconds**: within all platforms' sweet spots, long enough for real hook + payoff + CTA, short enough for completion rate.

## File conventions

All rendered videos in this pipeline are written with consistent naming so platform adapters know what to pick up:

```
.growth/videos/<batch-id>/<hook-id>.mp4
```

Single file per hook, targeted for all three platforms. Scheduler adapts caption + hashtags per platform; video itself is the same.

If a hook needs platform-specific video variants (e.g., different durations), encode them as:

```
.growth/videos/<batch-id>/<hook-id>__tiktok.mp4
.growth/videos/<batch-id>/<hook-id>__reels.mp4
.growth/videos/<batch-id>/<hook-id>__shorts.mp4
```

The scheduler's adapter picks the platform-specific file if present; falls back to the default `<hook-id>.mp4` if not.

## When platform specs conflict with hook format

Example: `seven_second_pexels` is 7 seconds, but TikTok's sweet spot is 21–34s.

**The 7-second format is a hook delivery, not a post length.** Either:
1. Extend the b-roll loop to ~22 seconds with the text hook fixed for the first 7s + "Read caption 👇" for 3s + the rest on natural b-roll. Caption delivers full payoff.
2. Or let the 7-second video stand; 7s gets plenty of reach on IG Reels and works fine on TikTok when the caption is strong.

The assembler defaults to option 1 if `config.yaml:extend_to_platform_sweet_spot: true`. Default off until user tests both.
