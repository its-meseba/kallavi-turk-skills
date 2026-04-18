# Posting Protocol

Multi-account posting across TikTok, Instagram, and YouTube Shorts at any scale above "just me posting manually" has anti-spam countermeasures you will hit if you don't follow protocol. This file codifies what actually works as of April 2026, distilled from Blotato's published best practices + the Cal.ai multi-account playbook.

The single most common failure mode of this whole pipeline: **cold-start automation.** A brand-new TikTok account posts 4 videos on day one via API, account gets shadowbanned, user blames the tool. Don't do this.

---

## The 4-week account warmup (NON-NEGOTIABLE for new accounts)

Before any account is added to `accounts.yaml` as an active posting target, it must be warmed up for 4 weeks. No API posting during warmup — manual only, and the behavior must look like a real human creator.

### Week 1: Existence

- Create the account on the actual phone (not emulator).
- Profile photo, bio, 1 link.
- **Do not post.** Consume only.
- Daily: 20–30 min scrolling the For You feed, liking 5–10 posts, following 3–5 niche accounts.
- Watch 2–3 full videos per session (completion rate signal).
- Comment on 2–3 posts with real text (not emoji-only).

### Week 2: Engagement

- Continue daily scrolling + engagement (same as week 1).
- Post **2 videos this week, manually** — filmed/uploaded from the phone.
- These posts should look native: phone-filmed vibes, captions typed on the phone, no obvious AI.
- Respond to any comments within 2 hours.

### Week 3: Cadence

- 3–4 posts this week, still manual from the phone.
- Vary posting times (no pattern).
- Cross-post to IG from the same phone (same vibe), manual.
- Don't connect scheduling tools yet.

### Week 4: Integration

- 4–5 posts this week, still manual but from the desktop is OK now.
- Connect to Blotato / Postiz via official OAuth.
- Post **one** video via the scheduler — as a test.
- Post the rest manually.

After week 4: account is warm. Graduate it to `accounts.yaml` with a `warm_date: <week-4-end>` field.

## Active account caps (after warmup)

Per-platform, per-account, per-day maximums that won't trip rate limits or anti-spam heuristics:

| Platform | Max posts/day | Max posts/week | Notes |
|---|---|---|---|
| TikTok | 2–3 | 14 | Above 3/day triggers diminished reach. 4+ often shadowbans. |
| Instagram Reels | 1–2 | 10 | Above 2/day hurts reach per official IG guidance. |
| YouTube Shorts | 2–3 | 15 | More forgiving than TikTok/IG but diminishing returns above 3. |

For a 3-account-per-app cluster, that's ~42 TikTok posts/week/app max — which is more than enough. Don't push these numbers.

## The 3-4 account cluster strategy (Cal.ai playbook)

For each app, build a cluster of 3–4 TikTok accounts + 1–2 Instagram accounts + 1 YouTube channel. Each TikTok has a slightly different angle so they don't look like dupes of each other:

**Example for HabitAdd:**
- `@habitadd_focus` — ADHD/focus angle
- `@habitadd_am` — morning routines angle  
- `@habitadd_official` — brand voice, feature announcements
- `@habit_streak_daily` — unbranded "tips" voice, product plug in caption

**Why 3–4, not 10:** managing 10+ accounts manually is more than an indie dev can sustain, and the anti-flag protocol above means each account needs real manual engagement daily during warmup. 3–4 is the sustainable sweet spot.

**Content distribution rule:** any single hook video is posted to **at most 2 accounts**, with different captions, different posting times, and ideally ≥6 hours apart. Never the same caption to 2 accounts — Blotato's Spintax and the scheduler's `caption_variants` generator handle this.

## Caption variation

The scheduler auto-generates caption variants using one of these patterns, driven by `config.yaml:caption_variation_mode`:

1. **Spintax** (`{hello|hi|hey} {friend|there|yo}`) — cheapest, moderate quality
2. **LLM paraphrase** — Claude rewrites the caption per account with that account's persona, higher quality, small cost
3. **Manual** — user writes 3–4 caption variants in the hook YAML, scheduler picks round-robin

Default to option 2 for brand accounts, option 1 for unbranded filler accounts.

## Posting time variation

Don't post all accounts at the same time — stagger by 2–8 hours, and randomize within windows:

```yaml
# In config.yaml
posting_windows:
  tiktok:
    - {start: "09:00", end: "11:00", weight: 0.3}
    - {start: "13:00", end: "15:00", weight: 0.2}
    - {start: "19:00", end: "22:00", weight: 0.5}  # prime time
  reels:
    - {start: "11:00", end: "13:00", weight: 0.4}
    - {start: "20:00", end: "22:00", weight: 0.6}
```

Scheduler picks a random time within a window, weighted by the weights. Different accounts get different windows for the same content.

## Anti-flag rules (follow all)

1. **Always official OAuth.** No session cookies, no scraping-based posting. Blotato/Postiz/Repurpose.io all use official platform APIs. Stick to these.
2. **Vary captions.** See above.
3. **Vary hashtags.** Don't paste the same hashtag block to every post. Rotate from a pool of ~30 relevant tags, pick 3–5 per post.
4. **Don't post rapid-fire.** Minimum 1 hour between posts on the same account even if daily cap allows more.
5. **Warm IP / device fingerprint.** If running scheduler from a server, make sure it's the same server OAuth'd on day 1 of week 4. Switching IPs mid-campaign looks suspicious.
6. **Respond to comments.** Accounts with zero comment engagement read as bots. Spend 10 min/day per account answering comments (or use Claude to draft responses you approve and post manually).
7. **Don't use URL shorteners in bio.** TikTok heavily suppresses bit.ly, tinyurl, etc. Use linktr.ee, beacons.ai, or your own domain.
8. **No watermarks.** If using Track B content from Veo/Seedance/Kling, make sure the model tier doesn't embed a visible corner watermark. TikTok demotes watermarked content heavily.
9. **Don't cross-post TikTok → Reels with the TikTok watermark.** Use Repurpose.io's watermark-stripping, or re-export from source. TikTok watermark on Reels = immediate reach tank on Meta.

## What Blotato / Postiz / Repurpose do differently

| Tool | Unique value | When to use |
|---|---|---|
| **Blotato** ($29 Starter) | Ships MCP for Claude Code; 4-week warmup doc; 20 accounts on Starter | **Primary scheduler** for this pipeline. |
| **Postiz** (self-host ~$7 VPS) | Unlimited accounts; full REST API; OSS | **Backup / scale-up** when account count exceeds Blotato tier. |
| **Repurpose.io** ($29 Starter) | TikTok watermark stripping; auto-syndication TikTok → Reels/Shorts/Threads | **Adjacent** — pair with either above for cross-platform multiply. |

Default config assumes Blotato as primary. Switch the adapter in `scripts/schedule_post.py` to Postiz if you self-host.

## User approval gate

`scripts/schedule_post.py` never publishes without user approval. Workflow:

1. Script generates a proposed schedule (all accounts, all posts, times, captions).
2. Writes to `.growth/schedules/<batch>-<date>.yaml`.
3. Shows the user a summary (which hook → which account → what time → what caption).
4. User types `y` to push to Blotato queue, `edit` to modify, `n` to abort.

Never auto-push. One wrong caption to a brand account can cost more than a week of gains.

## Performance feedback loop

After publishing, `scripts/pull_metrics.py` runs daily and writes one `performance.jsonl` line per post. This feeds back into Stage 1 (brief regeneration) so next week's batch is informed by what actually worked.

**Minimum metrics to capture per post:**
- Views at 24h, 48h, 7d
- Saves
- Shares  
- Comments
- Link clicks (if trackable)
- Installs attributed (from Singular Free)

## What this protocol does NOT promise

- Virality. Nothing promises virality. This protocol minimizes downside (bans, shadowbans, wasted effort) — it does not manufacture upside.
- Escape from platform rule changes. TikTok/IG change algorithms constantly. Revisit this doc quarterly and update.
- Protection from obvious spam. If your captions are spammy, your hooks are stale, and your content is low-effort, no anti-flag protocol saves you. The point of the rest of the pipeline (brief, hooks, track A validation) is to avoid shipping spam in the first place.
