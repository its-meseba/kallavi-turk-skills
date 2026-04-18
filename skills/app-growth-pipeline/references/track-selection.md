# Track Selection

When generating a batch or rendering a single hook, which track should it use? Decision tree below. When in doubt, **default to Track A**. The validation-first principle is the core economic lever of this pipeline.

---

## Decision tree

```
Is this hook an angle with PROVEN performance history?
│
├── NO → Track A (cheap, fast, validate first)
│
└── YES → How much signal?
         │
         ├── Mild signal (few thousand views, no installs yet)
         │   → Track A again with a new variation
         │
         ├── Strong signal (viral view count OR actual install attribution)
         │   → Hybrid: Track B hero shot, Track A b-roll, Submagic polish
         │
         └── Proven + repeatable angle (2+ viral hits on this angle)
             → Full Track B: DansUGC reaction hook + fal.ai b-roll + Submagic
```

## Signal thresholds (rough)

These are floors, not ceilings — tune per app in `config.yaml` under `track_thresholds:`.

**Mild signal:**
- ≥5,000 views on any platform in 48 hours, OR
- ≥2% save rate on Instagram Reels, OR
- ≥5% comment-to-view ratio

**Strong signal:**
- ≥50,000 views in 72 hours, OR
- ≥1 install attributed via Singular/RevenueCat custom link, OR
- ≥10% share-to-view ratio

**Proven + repeatable:**
- 2+ hooks on the same angle hit "strong signal" in the last 30 days, OR
- An angle from the brief's § 5 "top-performing hooks" for 2 consecutive weeks

## Why validation-first

The research doc covered this but worth restating as a rule:

- Track A costs ~$0 per hook. Generating 20 of them burns pennies.
- Track B costs $0.75–8 per hook. Generating 20 of them burns $15–160.
- The hit rate of any hook batch is typically 1–3 winners out of 20.
- Running all 20 through Track B means spending $15–160 to find the same 1–3 winners you could have found for ~$0.

The only reason to skip Track A is when you already **know** an angle works and the bottleneck is production quality, not validation.

## Exceptions: when Track B is the right first move

- **Hero launch content.** App launch, major feature release, App of the Day coverage — you want maximum polish on the first wave.
- **Response to a trend window.** A TikTok sound or meme is peaking and will be dead in 48 hours. Skip validation, ship polished now.
- **Angle validated elsewhere.** A competitor is winning with this exact format; you're copying a known pattern, not testing a new one.
- **User has budget + wants volume.** User explicitly says "push 20 paid videos this week, budget approved" — respect it but remind them of the validation principle.

## Hybrid recipe (the sweet spot)

For a hook with mild-to-strong signal:

```yaml
track: hybrid
# Hero shot: paid AI or UGC (0-3 seconds, the scroll-stopper)
hero_prompt: "close-up of hands holding phone in morning light, natural"
hero_model: veo-3-fast
hero_duration_sec: 3
hero_with_audio: false

# B-roll: Track A / Pexels (the rest of the clip)
broll_query: "morning routine bed phone"
broll_duration_sec: 4

# Polish: Submagic for captions (worth it once you're already paying for hero)
submagic_polish: true
```

Cost: ~$0.45 (Veo 3.1 Fast @ 3s) + $0 Pexels + Submagic pro-rated = ~$0.85/hook. 10× cheaper than full Track B, most of the polish.

## Model selection within Track B

When `track: B` or `track: hybrid`, pick the hero model based on what the shot needs:

| Shot requirement | Best model | $/sec | Notes |
|---|---|---|---|
| Realistic human face + voice | `veo-3-fast` | $0.15 w/audio | Best UGC-believable human. |
| Cinematic b-roll w/ camera motion | `kling-2.5-turbo-pro` | $0.07 | Cheapest reputable cinematic. |
| 1080p product/app beauty shot | `hailuo-02-pro` | $0.08 | Strong physics, 1080p, no audio. |
| Multi-shot sequence in one pass | `seedance-2-fast` | $0.24 | Unique: multiple cuts in single call. |
| Stylized / effects / memes | `pika-2.5` | ~$0.09 | Bad for realism, good for stylized. |
| Budget volume | `hailuo-02-std-512p` | $0.017 | Cheapest serviceable; lower res. |

See `fal-backends.md` for the full catalog and `fal_client.py` wrapper API.

## What Track B is NOT for

- Testing whether an angle works. Use Track A.
- Replacing real human UGC when the hook is a testimonial/reaction. Real humans still outperform AI avatars on trial-to-paid conversion for subscription apps. Use DansUGC.
- Generating faces of specific real people. Don't.
- Generating content featuring minors. Don't.
