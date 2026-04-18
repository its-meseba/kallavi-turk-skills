# Hook Batch Schema

Every generated hook batch lives at `.growth/hooks/<YYYY-MM-DD>-batch-<nn>.yaml` and follows this schema. The assembler and scheduler both parse it.

## Full schema

```yaml
# Batch metadata
batch_id: 2026-04-18-batch-01
app_slug: habitadd
generated_at: 2026-04-18T14:32:00+03:00
brief_version: <git sha of brief.md at time of generation>
total_hooks: 20

# Defaults applied if not overridden per-hook
defaults:
  platform_targets: [tiktok, reels, shorts]
  tts_voice: hume_octave_warm_female_en
  caption_style: lumio_bold_yellow
  cta_variant_rotation: true   # pick from brief.md §9 in round-robin

# The hooks themselves
hooks:
  - id: h001
    status: draft   # draft | approved | rendered | scheduled | published | killed
    format: seven_second_pexels
    track: A        # A | B | hybrid | ugc
    language: en
    
    # Content
    hook_text: "The 3 habits killing your focus (you do #2 every morning)"
    voiceover: "Three habits killing your focus. Number two..."
    caption: |
      1. Checking phone in first 10 minutes
      2. Skipping the first hour plan  ← most people do this
      3. Ignoring your sleep signal
      
      HabitAdd tracks all three. Link 👇
    cta: "Link in bio — 7 days free"
    
    # Track A fields
    broll_query: "person on phone morning bed"   # Pexels search
    broll_duration_sec: 7
    
    # Track B fields (if track: B or hybrid)
    hero_prompt: null
    hero_model: null              # veo-3-fast | kling-2.5-turbo-pro | hailuo-02-pro | seedance-2-fast
    hero_duration_sec: null
    hero_with_audio: null
    
    # UGC fields (if track: ugc or hybrid with UGC hero)
    ugc_clip_id: null             # reference to .growth/ugc-library/
    screen_recording: null        # path relative to .growth/
    
    # Polish
    submagic_polish: false        # true = POST to Submagic API after assembly
    
    # Platform-specific tuning
    platform_overrides:
      tiktok:
        caption: "...TikTok-optimized version..."
      reels:
        caption: "...IG-optimized version with hashtags..."
      shorts:
        caption: "...YT-optimized with #Shorts..."
    
    # Performance tracking (filled in later by pull_metrics.py)
    published_posts: []
    # format once published:
    # - platform: tiktok
    #   account: "@habitadd_focus"
    #   post_id: "7234..."
    #   published_at: "2026-04-19T09:00:00+03:00"
    #   url: "https://tiktok.com/..."

  - id: h002
    # ...
```

## Status lifecycle

- **draft** — generated, not yet reviewed by user
- **approved** — user approved for rendering
- **rendered** — MP4 exists in `.growth/videos/<batch>/`
- **scheduled** — queued in Blotato/Postiz
- **published** — live on at least one platform
- **killed** — user rejected; keep in YAML for record but don't render/post

Scripts update the `status` field in place. Never delete hooks from a batch — keeping killed ones in the record helps future brief regeneration learn what to avoid.

## Validation

`scripts/validate_batch.py` checks:
- All required fields present per `format`
- Track A hooks have `broll_query`
- Track B hooks have `hero_prompt` + `hero_model`
- UGC hooks have `ugc_clip_id` that exists in `.growth/ugc-library/`
- Languages in `hook.language` are in `config.yaml`'s supported languages
- No duplicate `id` values within the batch

Always validate before passing to `assemble_video.py`. Invalid batches fail fast with a clear error.

## Why YAML not JSON

- Readable by humans during review (the user is the primary reader before rendering)
- Supports multi-line captions cleanly with `|`
- Comments allowed (`# kill this one, too similar to h005`)
- Claude Code can view/edit it as a text file without JSON parser ceremony

## Why one file per batch, not one per hook

- A batch is the unit of human review
- Easier to diff and version in git (`git log .growth/hooks/`)
- Avoids tiny-file sprawl (20 files per week adds up)
