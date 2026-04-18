---
name: app-growth-pipeline
description: Run the Lumio Studio content pipeline for promoting subscription mobile apps on TikTok, Instagram Reels, and YouTube Shorts. Use this skill whenever the user asks to generate hooks, scripts, or videos for one of their apps; when they mention HabitAdd, Adımla, or any Lumio Studio app they want to market; when they want to research competitor content or mine app store reviews for hook ideas; when they want to batch-produce short-form social content; when they mention Pexels, Seedance, Veo, Kling, Hailuo, Submagic, fal.ai, DansUGC, Arcads, HeyGen, JoggAI, Blotato, or Postiz in the context of app marketing; when they reference a `.growth/` folder in an app repo; or any time they say "let's make content for [app]", "new hook batch", "grow [app]", "post for [app]", "run the pipeline", or similar. This skill is the single entry point for all app-marketing workflows — use it even when the user only asks for part of the pipeline (just a brief, just hooks, just a video assembly).
---

# App Growth Pipeline

A content pipeline for promoting Lumio Studio's subscription mobile apps on short-form social (TikTok, Instagram Reels, YouTube Shorts). Optimized for a solo indie dev running multiple apps with a $100–300/month tools budget.

## Where things live (IMPORTANT — read this first)

This skill has a strict separation between **skill logic** (portable, global) and **per-app data** (travels with each app's codebase).

**Skill logic — lives here (`~/.claude/skills/app-growth-pipeline/`):**
- `SKILL.md` (this file)
- `references/` — playbooks, tool docs, prompting templates
- `scripts/` — Python workhorses (assembly, scraping, scheduling)
- `assets/` — fonts, caption-style presets, Lumio logo overlays
- `_template/` — the scaffold copied into new apps

**Per-app data — lives in each app's repo under `.growth/`** (e.g. `~/dev/work/lumio-studio/habitadd/.growth/`):
- `brief.md` — living creative brief
- `config.yaml` — language, platforms, accounts, track preference, TTS voice, brand colors
- `accounts.yaml` — the 3–4 TikTok + 1–2 IG + 1 YT handles in this app's cluster
- `hooks/<date>-batch-<nn>.yaml` — generated hook batches
- `videos/<batch>/` — rendered MP4s (gitignore this)
- `ugc-library/` — DansUGC reaction clips, organized by hook style (gitignore)
- `logs/performance.jsonl` — one line per published post

**Why this split:** the app's git repo preserves its growth history (commits to `brief.md` tell the story of what was tried), renders stay out of git (too heavy), and the skill itself is upgradable without risking per-app data.

## How the skill finds the app

Three resolution strategies, in order of precedence:

1. **Explicit flag** — user says "run the pipeline for `/path/to/habitadd`" → use that path.
2. **Current working directory** — if `cwd/.growth/config.yaml` exists, use it.
3. **Walk up** — look for `.growth/` in parent directories (like git does for `.git`).

If none found and the user named an app (e.g. "HabitAdd"), ask them for the repo path. Do **not** guess.

Set `APP_GROWTH_ROOT` in the shell to override (e.g. `export APP_GROWTH_ROOT=~/dev/work/lumio-studio/habitadd/.growth`).

## When to use (trigger conditions)

Fire this skill for any of these regardless of wording:

- **Brief** — "new creative brief", "refresh the brief for [app]", "update strategy"
- **Hooks** — "give me 20 hooks for [app]", "new hook batch", "scripts for this week"
- **Research** — "what are competitors posting", "mine App Store reviews", "top hooks in [niche]"
- **Video** — "make the videos", "render this batch", "assemble with Pexels+FFmpeg", "use Seedance for this"
- **Posting** — "schedule the batch", "push to Blotato", "post across my accounts"
- **Metrics** — "pull yesterday's numbers", "what's working", "update performance log"
- **Full loop** — "run the pipeline for [app]", "do the full cycle"
- **Setup** — "add a new app", "scaffold `.growth/` for [app]"

## Architecture: two tracks in parallel

Stack A (volume/validation) and Stack B (scale winners) from the research doc, running side by side:

- **Track A — Validation/volume.** Pexels + FFmpeg + edge-tts or Kokoro. Near-zero cost. Use to test 20–40 hooks/week and filter for which actually convert.
- **Track B — Scale winners.** For hooks that showed Track A signal only: real-human DansUGC reaction clips ($3–8/video) OR paid AI video via fal.ai (Veo 3.1 Fast, Kling 2.5 Turbo Pro, Hailuo 02 Pro, Seedance 2.0 Fast), polished with Submagic API, published via Blotato.

**Never jump straight to Track B on untested hooks.** The whole point of Track A is filtering before spending real money. See `references/track-selection.md` for the decision tree.

## The five stages

Each request from the user hits one or more of these. When user asks for "full loop," run 1 → 5 with human approval gates.

### Stage 1 — Creative brief (weekly or on-demand)

Goal: fresh brief grounded in real data, not vibes.

1. Read existing `.growth/brief.md` (baseline — you're updating, not starting over).
2. Read last 7 days of `.growth/logs/performance.jsonl`.
3. Run `scripts/fetch_app_reviews.py --app-path <path>` — pulls App Store + Play Store reviews using free npm scrapers (see `references/tool-costs.md`).
4. Run `scripts/competitor_hooks.py --app-path <path>` — refreshes competitor hook inventory (uses Apify if configured, else yt-dlp + TikTok Creative Center).
5. Synthesize into updated `brief.md` using `references/creative-brief-template.md`.
6. **Show the user a diff.** Do not silently overwrite — brief changes are editorial decisions.

### Stage 2 — Hook + script generation

Goal: 20–40 hooks in the formats proven in `references/hook-formats.md`.

1. Load fresh `brief.md` + last batch's `performance.jsonl` to know what angles worked.
2. For each hook, pick a format from `references/hook-formats.md`:
   - `seven_second_pexels` — stock b-roll + text overlay + 3-sec "read caption" tail (Penelope Lopez format)
   - `ugc_reaction` — real-human reaction hook + screen recording (DansUGC pattern)
   - `before_after` — problem clip / solution clip / app screen
   - `screen_recording_narrated` — app demo with VO + captions
   - `founder_pov` — face-to-camera if user has AI Twin cloned in Captions.ai
3. Write to `.growth/hooks/<YYYY-MM-DD>-batch-<nn>.yaml` in the schema defined in `references/hook-schema.md`.
4. **Show the user the batch.** Never auto-render — hook selection is where human judgment matters most.

### Stage 3 — Video assembly

Decided per-hook by the `track` field in the hook YAML.

**Track A (zero-cost):**
```bash
python scripts/assemble_video.py --app-path <path> --batch <batch-file> --track A
```
Pexels b-roll, Kokoro/edge-tts narration, FFmpeg burn-in captions, 9:16 MP4 to `.growth/videos/<batch>/`. See `references/pexels-ffmpeg-recipe.md` for exact FFmpeg pipeline.

**Track B (paid):**
```bash
python scripts/assemble_video.py --app-path <path> --batch <batch-file> --track B --model veo-3-fast
```
Available models: `veo-3-fast`, `veo-3-standard`, `seedance-2-fast`, `seedance-2-standard`, `kling-2.5-turbo-pro`, `kling-2.6-pro`, `hailuo-02-pro`, `hailuo-02-std`, `luma-ray-flash-2`. See `references/fal-backends.md` for per-model pricing + selection logic.

**Hybrid (recommended default):** Track A for b-roll, Track B for hero shot only. Set both `broll_query` and `hero_prompt` in the hook YAML and assembler handles the split.

**UGC path (Stack B):** if hook specifies `ugc_clip_id`, splice a pre-purchased DansUGC clip from `.growth/ugc-library/` + screen recording + Submagic caption polish.

### Stage 4 — Scheduling + posting

```bash
python scripts/schedule_post.py --app-path <path> --batch <batch-file>
```

Reads `.growth/accounts.yaml`, stages posts via Blotato API (primary) or Postiz self-hosted (fallback). Enforces the **4-week warmup protocol** for new accounts from `references/posting-protocol.md` — skip this at your peril, TikTok will shadowban cold-start automation.

Caption variants are auto-generated so no two accounts post identical text. **User approves the schedule before push.**

### Stage 5 — Performance pull

```bash
python scripts/pull_metrics.py --app-path <path> --since yesterday
```

Appends to `.growth/logs/performance.jsonl`. Sources: TikTok Business API, Meta Graph API (IG), YouTube Data API, Singular (for install attribution if configured). Set up as a cron job on your VPS.

This **closes the loop** — Stage 1 reads from this file next time.

## Initial setup for a new app

When user says "add an app" or references an app with no `.growth/`:

1. Ask for the app's repo path (absolute).
2. `cp -r ~/.claude/skills/app-growth-pipeline/_template <repo>/.growth`
3. Interview the user to fill `.growth/config.yaml`:
   - App name, slug, bundle IDs
   - Primary language(s), target countries
   - Platform targets (TikTok / Reels / Shorts)
   - Budget ceiling per hook ($)
   - Preferred default track (A, B, or hybrid)
   - TTS voice preference
   - Brand colors (hex)
4. Ask for 3–5 competitor handles per platform; write to `config.yaml`.
5. Run Stage 1 to seed the first `brief.md`.
6. Instruct the user to add `.growth/videos/` and `.growth/ugc-library/` to `.gitignore`.
7. `git add .growth && git commit -m "growth: scaffold"`

## Environment variables

The scripts read from a `.env` file in the skill root (`~/.claude/skills/app-growth-pipeline/.env`). Never commit this. The `_template/.env.example` shows all keys.

```
FAL_API_KEY=              # Track B video generation (primary)
PEXELS_API_KEY=           # Track A b-roll (free tier fine)
SUBMAGIC_API_KEY=         # caption polish (Stack B)
BLOTATO_API_KEY=          # multi-account scheduling (Stack B)
POSTIZ_URL=               # self-hosted Postiz (Stack A alt)
POSTIZ_API_KEY=
APIFY_TOKEN=              # optional — competitor scraping
DEEPGRAM_API_KEY=         # transcription/captions (cheaper than Whisper API at volume)
HUME_API_KEY=             # optional — cheap expressive TTS
ELEVENLABS_API_KEY=       # optional — hero voices only
TIKTOK_BUSINESS_TOKEN=    # Stage 5 analytics
META_GRAPH_TOKEN=         # Stage 5 (IG)
YOUTUBE_API_KEY=          # Stage 5 (Shorts)
SINGULAR_API_KEY=         # optional — install attribution
```

## Guardrails (non-negotiable)

1. **Never auto-publish without user approval.** Batches get reviewed before they go live. The user approves batches, not individual posts, but the batch must be seen.
2. **Track A before Track B.** If user says "generate 20 Veo videos for HabitAdd" on a fresh brief with no performance history, push back: "validate on Track A first, or at minimum run 5 hooks through Track B and measure before scaling." Wasted paid video credits are the #1 failure mode.
3. **One brief per app.** Do not mix HabitAdd creative into Adımla accounts. Niche targeting collapses and both apps lose.
4. **Bilingual ≠ translated.** For Adımla (TR + EN), generate each language variant separately from the target audience's perspective. Never auto-translate hooks — humor, idioms, and pain-point phrasing don't transfer. See `references/hook-formats.md` § "Bilingual generation."
5. **Attribution links.** Every post's bio/caption link must route through the app's attribution tracker (RevenueCat custom link + Singular SKAN) so installs can be traced back to specific accounts + batches. If user hasn't configured this, tell them before helping them post.
6. **Content compliance.** No medical claims for habit/wellness apps. No inflated step-count claims for Adımla. The skill's scripts can't police this; Claude has to catch it at the hook-review stage.
7. **No minors in UGC.** If a DansUGC clip or any ad creative features a person who could plausibly be a minor, reject it regardless of what the marketplace says.

## Running the full loop

When user says "run the full pipeline for [app]" or "do the full loop":

1. Stage 1 — regenerate brief (if >7 days old; else skip).
2. Stage 2 — generate 20-hook batch (mix of Track A + B per brief's this-week angles).
3. **GATE: user approves which hooks to render.**
4. Stage 3 — assemble videos for approved hooks only.
5. **GATE: user approves rendered videos.** (Play a few, or at minimum watch the hook seconds.)
6. Stage 4 — stage the schedule across account cluster. **GATE: user approves schedule.**
7. Stage 5 — confirm cron for `pull_metrics.py` is running; if not, set one up.

Total time: ~45 min user time + 30–60 min script runtime per batch.

## Cost per batch (reference)

For 20 hooks, one app:

- Track A only (Pexels + Kokoro + FFmpeg): ~$0 (API credits negligible)
- Track A + Submagic polish: ~$2–4
- Track B (all Veo 3.1 Fast w/audio): ~$15 (20 × $0.75)
- Track B (all Kling 2.5 Turbo for b-roll): ~$8
- Hybrid (5 Track B hero + 15 Track A): ~$4–6
- DansUGC hero hooks (5 × $3–8): ~$15–40

Realistic monthly budget for 2 apps at ~3 batches/week: **~$80–120/month** on video generation, plus fixed SaaS (Submagic $41 + Blotato $29 + Apify $50 ≈ $120/mo for Stack B core). Total ~$200–240/mo. See `references/tool-costs.md` for the full stack breakdown.

## Reference files (loaded on demand)

Claude reads these only when the workflow needs them. Don't preload.

- `references/creative-brief-template.md` — the brief.md structure
- `references/hook-formats.md` — the 5+ proven short-form formats
- `references/hook-schema.md` — YAML schema for hook batches
- `references/platform-specs.md` — TikTok/Reels/Shorts dimensions, limits, algorithm quirks
- `references/pexels-ffmpeg-recipe.md` — Track A exact FFmpeg commands
- `references/fal-backends.md` — Track B model catalog + pricing + selection logic
- `references/submagic-api.md` — caption polish API usage
- `references/track-selection.md` — when to use Track A vs B vs hybrid
- `references/posting-protocol.md` — 4-week account warmup + anti-flag rules
- `references/tool-costs.md` — full stack cost reference with monthly totals

## What this skill does NOT do

- Paid ad management (Meta Ads Manager, TikTok Ads Manager) — separate workflow.
- Influencer outreach — manual.
- ASO (App Store listing optimization) — separate.
- Push notification / in-app campaign content — separate.
- Long-form YouTube or podcast distribution — this skill is short-form only.
- Website/landing-page copy — separate.

If the user asks for any of the above, say so and suggest the adjacent workflow rather than forcing it through this skill.
