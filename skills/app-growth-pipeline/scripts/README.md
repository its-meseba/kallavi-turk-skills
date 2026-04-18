# Scripts

Python workhorses referenced by `SKILL.md`. **Not yet implemented** — this directory is intentionally empty scaffolding. Claude Code will create each script on-demand the first time the pipeline hits a stage that needs it.

Build order (highest leverage first):

## Tier 1 — Build first (core Track A loop)

| Script | Purpose | Referenced by | Dependencies |
|---|---|---|---|
| `fetch_app_reviews.py` | Pull App Store + Play Store reviews for pain-point mining | Stage 1 (brief) | `app-store-scraper`, `google-play-scraper` (npm, via subprocess) or Python equivalents |
| `assemble_video.py` | Render hook YAML → MP4 (Track A: Pexels + FFmpeg + TTS) | Stage 3 | `ffmpeg`, `requests`, `pyyaml`, `tts.py` |
| `tts.py` | TTS adapter (edge-tts → Kokoro → Hume → ElevenLabs cascade) | Stage 3 | `edge-tts`, or Kokoro self-host |
| `validate_batch.py` | Check hook YAML for schema compliance before rendering | Stage 2 → 3 | `pyyaml`, `jsonschema` |

With just these four, Track A is fully operational.

## Tier 2 — Build when scaling to Track B

| Script | Purpose | Dependencies |
|---|---|---|
| `fal_client.py` | fal.ai wrapper with model selection + budget caps | `fal-client` pip |
| `submagic_client.py` | Submagic API integration for caption polish | `requests` |
| `competitor_hooks.py` | Scrape competitor TikTok/IG via Apify or yt-dlp fallback | `apify-client` or `yt-dlp` CLI |

## Tier 3 — Build when going multi-account

| Script | Purpose | Dependencies |
|---|---|---|
| `schedule_post.py` | Stage posts via Blotato API with account cluster rules | `requests`, `blotato-sdk` if exists |
| `pull_metrics.py` | Daily performance sync across TikTok/Meta/YT APIs → `performance.jsonl` | Platform SDKs |

## Tier 4 — Nice to have

| Script | Purpose |
|---|---|
| `pixabay_fallback.py` | B-roll fallback when Pexels rate-limits or returns nothing useful |
| `replicate_client.py` | Alternative video-gen backend for models fal.ai doesn't host |
| `caption_varianter.py` | Generate N caption variants from a base caption (Claude API call) |
| `ugc_library_organizer.py` | Index purchased DansUGC clips by emotion/demographic/angle |

## Shared conventions

All scripts:

1. Accept `--app-path <path>` pointing to the app's repo (or its `.growth/` directly). Resolve `config.yaml` and `brief.md` from there.
2. Read API keys from `~/.claude/skills/app-growth-pipeline/.env` via `python-dotenv`.
3. Enforce budget caps from `config.yaml:budget` before any paid API call. Abort with a clear error before spending.
4. Write outputs with `<app-path>/.growth/` as the root. Never write outside it.
5. Log to stderr in human-readable form; log to stdout as JSON for programmatic consumption where relevant.
6. Exit code 0 on success, non-zero on any failure. Scheduler loops depend on this.

## Python env

Recommended setup:

```bash
cd ~/.claude/skills/app-growth-pipeline
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

`requirements.txt` will be created alongside the first script.

## Running a script from a fresh Claude Code session

```
> /skill app-growth-pipeline
> run the brief stage for habitadd
```

Claude reads SKILL.md, locates the app via `.growth/config.yaml` in the cwd (or walks up), and invokes `fetch_app_reviews.py` + `competitor_hooks.py` + writes the brief. No script exists yet? Claude creates it first using the spec in this README + the relevant reference doc.
