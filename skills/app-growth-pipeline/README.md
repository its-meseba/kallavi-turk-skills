# app-growth-pipeline

A Claude Code skill for running a solo-indie-dev content pipeline across TikTok, Instagram Reels, and YouTube Shorts. Optimized for subscription mobile apps on a $100–300/month tool budget.

## Install

### Option A: Direct user-level install

```bash
# Clone or copy the skill into Claude Code's user-level skills dir
cp -r app-growth-pipeline ~/.claude/skills/

# Copy the env template and fill in the keys you plan to use
cd ~/.claude/skills/app-growth-pipeline
cp .env.example .env
nano .env   # fill in what your stack needs
```

Claude Code picks up new skills in this directory without a restart (file-watcher). Verify with a fresh session:

```
> What skills do you have access to?
```

Should list `app-growth-pipeline`.

### Option B: Symlink from `meseba-skills` (recommended for solo devs who version-control skills)

```bash
# Keep canonical copy in your skills repo
cd ~/dev/meseba-skills/skills
git add app-growth-pipeline
git commit -m "app-growth-pipeline: initial scaffold"

# Symlink into ~/.claude/skills so Claude Code sees it
ln -s ~/dev/meseba-skills/skills/app-growth-pipeline ~/.claude/skills/app-growth-pipeline
```

Edits to the repo are live; git history preserves skill evolution.

## Scaffold a new app

For each Lumio Studio app you want to run through the pipeline:

```bash
cd ~/dev/work/lumio-studio/<app-repo>
cp -r ~/.claude/skills/app-growth-pipeline/_template .growth
```

Then in Claude Code from that repo's directory:

```
> set up the growth pipeline for this app
```

Claude reads `SKILL.md`, interviews you to populate `.growth/config.yaml` + `.growth/accounts.yaml`, and generates the first `brief.md`.

## Daily / weekly usage

From inside any app repo with `.growth/`:

```
> new hook batch
> render the approved hooks
> schedule the batch
> pull yesterday's metrics
> run the full pipeline
```

See `SKILL.md` for all trigger phrases.

## What's included

- **`SKILL.md`** — the router Claude Code loads for triggering
- **`references/`** — 10 reference docs loaded on demand (brief template, hook formats, fal.ai catalog, FFmpeg recipes, posting protocol, tool costs, platform specs, track selection, etc.)
- **`_template/`** — copied into each app's `.growth/` on setup
- **`scripts/`** — Python workhorses (not yet implemented; see `scripts/README.md` for build order)
- **`assets/`** — fonts, caption styles, overlays (placeholders; see `assets/README.md`)

## What's not yet included

See `scripts/README.md` for the tiered build order. Short version:

- **Tier 1 (Track A):** `fetch_app_reviews.py`, `assemble_video.py`, `tts.py`, `validate_batch.py` — build these first
- **Tier 2 (Track B):** `fal_client.py`, `submagic_client.py`, `competitor_hooks.py`
- **Tier 3 (multi-account):** `schedule_post.py`, `pull_metrics.py`

Each script gets created on-demand by Claude Code when the pipeline first needs it, guided by the reference docs.

## Architecture at a glance

```
┌─────────────────────────────────────────────────────────┐
│ ~/.claude/skills/app-growth-pipeline/  (skill logic)   │
│ ├── SKILL.md                                            │
│ ├── references/  ← playbooks, tool docs                 │
│ ├── scripts/     ← Python workhorses                    │
│ ├── assets/      ← fonts, caption styles, overlays      │
│ └── _template/   ← scaffold for new apps                │
└─────────────────────────────────────────────────────────┘
                            │
                            │  reads from / writes to
                            ▼
┌─────────────────────────────────────────────────────────┐
│ <app-repo>/.growth/  (per-app data, travels with app)   │
│ ├── brief.md         ← living creative brief (git)      │
│ ├── config.yaml      ← per-app settings (git)           │
│ ├── accounts.yaml    ← social account cluster (git)     │
│ ├── hooks/           ← YAML batches (git)               │
│ ├── videos/          ← rendered MP4s (gitignored)       │
│ ├── ugc-library/     ← DansUGC clips (gitignored)       │
│ └── logs/            ← performance.jsonl (git)          │
└─────────────────────────────────────────────────────────┘
```

## Budget expectation

- **Stack A** (volume, no humans): ~$185–240/mo
- **Stack B** (human UGC hooks): ~$295/mo

See `references/tool-costs.md` for the full breakdown.

## Design principles

1. **Validation before spend.** Track A filters hooks for free; Track B amplifies only proven winners.
2. **One brief per app.** No shared creative across niches.
3. **Human approval gates.** Never auto-publish, never auto-render untested hooks.
4. **Data travels with the app.** Skill is portable; per-app creative history lives with the app's repo.
5. **Tool-agnostic where it matters.** Adapter scripts wrap fal.ai, Blotato, Submagic so replacements don't require rewriting the skill.

## License

Not yet decided — keep private within Lumio Studio / Kallavi until you decide whether to open-source.
