# fal.ai Backends

Track B runs everything through [fal.ai](https://fal.ai) as the single video-generation aggregator. One API key, one bill, one SDK, all major models. This file documents which models are available, what they cost, and when to pick each. Cross-reference with `track-selection.md` for when to use Track B in the first place.

## Why fal.ai (vs Replicate or direct)

- **One SDK for all major models** (Veo, Kling, Seedance, Hailuo, Luma, Pika, Wan).
- **30–50% cheaper than Replicate** on overlapping models as of April 2026.
- **Fixes the Gemini API `aspectRatio: 9:16` bug** for Veo 3.1 — fal's wrapper handles vertical reliably.
- **Consolidated billing** — one invoice instead of five.
- Pay-per-generation, no monthly minimums.

## Model catalog (prices as of April 2026)

All prices cheapest-API-path via fal.ai. Re-verify quarterly (pricing moves fast — Luma cut Ray 3× in Jan 2026, Seedance 2.0 launched April 9 with discount).

### Veo (Google) — best UGC realism

| Model ID | $/sec | 5s clip | Audio | Best for |
|---|---|---|---|---|
| `veo-3-fast` | $0.15 | $0.75 w/audio | Yes, lip-sync | **Default for human face + dialogue.** Best UGC-believable human. |
| `veo-3-standard` | $0.40 | $2.00 w/audio | Yes | Hero spots only; Fast is usually good enough. |

**Known issue:** SynthID watermark always embedded; visible corner watermark on non-Ultra tiers. Acceptable for organic social; not for paid ads to platforms that reject watermarks.

### Kling (Kuaishou) — best cheap cinematic

| Model ID | $/sec | 5s clip | Audio | Best for |
|---|---|---|---|---|
| `kling-2.5-turbo-pro` | **$0.07** | $0.35 | No | **Default for b-roll volume.** Cheapest reputable cinematic. |
| `kling-2.6-pro` | $0.14 | $0.70 w/audio | Yes + voice ctrl | Best $/quality when audio needed. |
| `kling-3.0` | $0.17–0.39 | $0.85–1.96 | Yes | Top-tier multi-shot 4K; premium product shots. |

### Seedance (ByteDance) — best multi-shot

| Model ID | $/sec | 5s clip | Audio | Best for |
|---|---|---|---|---|
| `seedance-2-fast` | $0.24 | $1.21 | Yes, sync | **Unique: multi-shot sequence in one call.** Best for cinematic b-roll with camera motion + product close-ups together. |
| `seedance-2-standard` | $0.30 | $1.51 | Yes | Hero promo spots only. |

### Hailuo (MiniMax) — best cheap 1080p

| Model ID | $/sec | 5s clip | Audio | Best for |
|---|---|---|---|---|
| `hailuo-02-pro` | $0.08 | $0.48 (6s) | No | **Default for 1080p product/app shots.** Great physics. 10-sec cap. |
| `hailuo-02-std-512p` | **$0.017** | ~$0.10 | No | Cheapest serviceable hosted model, period. Entry-level quality. |

### Luma — cinematic HDR

| Model ID | $/sec | 5s clip | Audio | Best for |
|---|---|---|---|---|
| `luma-ray-flash-2` | $0.06 | $0.30 | No | Strong cinematic volume option. |
| `luma-ray-3.14` | ~$0.08 @ 1080p | varies | No | HDR + reasoning. Situational for product hero shots. |

### Pika — stylized / effects

| Model ID | $/sec | 5s clip | Audio | Best for |
|---|---|---|---|---|
| `pika-2.5` | ~$0.09 | ~$0.45 | Limited | Meme-y transitions and Pikaffects. **Bad for realism.** |

### Sora (OpenAI)

| Model ID | $/sec | 5s clip | Audio | Best for |
|---|---|---|---|---|
| `sora-2` | $0.10 | $1.00 (10s) | Yes | Competitive with Veo 3.1. Free tier killed Jan 10 2026. |
| `sora-2-pro` | $0.30–0.50 | $1.50–5.00 | Yes | 25-sec hero spots only. |

### Wan 2.5 (Alibaba) — open weights

| Model ID | $/sec | 5s clip | Audio | Best for |
|---|---|---|---|---|
| `wan-2.5` | $0.05 hosted | ~$0.25 | Yes | **Self-host option.** 1.3B variant runs on 8GB VRAM. Use for indefinite-scale volume if you're running a GPU. |

## Selection logic (the `fal_client.py` wrapper implements this)

Given a hook's requirements, pick the model:

```python
def pick_model(hook):
    # Real-human-looking face needed? Veo 3.1 Fast.
    if hook.format == "ugc_reaction" and hook.track != "ugc":
        return "veo-3-fast", {"with_audio": True}
    
    # Hero product shot, needs quality?
    if hook.is_hero and hook.needs_audio:
        return "kling-2.6-pro", {"with_audio": True}
    
    # Multi-shot sequence in one call?
    if hook.multi_shot_required:
        return "seedance-2-fast", {}
    
    # 1080p product shot, no audio needed?
    if hook.is_hero and hook.requires_1080p:
        return "hailuo-02-pro", {}
    
    # Generic b-roll volume?
    if not hook.is_hero:
        return "kling-2.5-turbo-pro", {}
    
    # Default fallback
    return "hailuo-02-pro", {}
```

The hook YAML can override with explicit `hero_model: <id>`.

## Budget guardrails (implemented in `fal_client.py`)

Before each API call, the wrapper checks:

1. **Per-hook cap** — from `config.yaml:budget.max_per_hook_usd`. Default $2. Abort if estimated cost exceeds.
2. **Per-batch cap** — from `config.yaml:budget.max_per_batch_usd`. Default $40. Abort mid-batch if total spent exceeds.
3. **Per-month cap** — tracked in `~/.claude/skills/app-growth-pipeline/.spend-log.jsonl`. Default $200. Abort if the month-to-date total exceeds.

Caps are advisory — the wrapper prints a warning and asks for explicit `--override-budget` to proceed. Never silently exceed.

## Rate limits

fal.ai's default rate limits are generous but not unlimited. For a 20-hook Track B batch, the wrapper:

- Queues up to 4 concurrent generations
- Exponential backoff on 429
- Writes partial results to `.growth/videos/<batch>/_partial/` so a crash doesn't lose work
- Resumable: re-running the same batch skips hooks that already have rendered MP4s

## Environment

```bash
export FAL_API_KEY=<your key>  # or put in ~/.claude/skills/app-growth-pipeline/.env
```

Install the client:

```bash
pip install fal-client
```

Reference docs: https://docs.fal.ai

## When fal.ai doesn't have a model

Fallback: `scripts/replicate_client.py` (not implemented in scaffold — add when needed). Replicate hosts more obscure models; worth the 30–50% markup only for models fal doesn't carry.

## When to self-host instead

If monthly Track B spend exceeds ~$150 consistently, self-hosting Wan 2.5 or HunyuanVideo on a rented A100 ($1–2/hr) becomes cheaper. See `references/self-host-notes.md` (not created yet — add when relevant). For now: use fal.ai.
