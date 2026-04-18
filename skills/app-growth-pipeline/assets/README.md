# Assets

Bundled assets for video rendering: fonts, caption styles, brand overlays.

## What needs to be added

**None of these are bundled yet.** Placeholders only. Add as you need them.

### `fonts/`

For FFmpeg `drawtext` burn-in. Need a TrueType font file that:
- Is free for commercial use (SIL OFL, Apache 2.0, or public domain)
- Has a heavy/black weight for caption readability
- Supports Turkish characters (ı, İ, ğ, Ğ, ş, Ş, ç, Ç) — important for Adımla

**Recommended:** download Inter (SIL OFL) from https://github.com/rsms/inter/releases and drop `Inter-Black.ttf` in this directory.

```bash
cd ~/.claude/skills/app-growth-pipeline/assets/fonts
curl -L -o Inter-Black.ttf https://github.com/rsms/inter/raw/master/docs/font-files/Inter-Black.ttf
```

### `caption-styles/`

ASS (SubStation Alpha) subtitle presets. Each is a template with `{text}` and `{start}`/`{end}` placeholders that `assemble_video.py` fills in.

Suggested presets to start with:
- `lumio-bold-yellow.ass` — yellow text, black border, bottom-middle position
- `cinematic-white.ass` — clean white with subtle drop shadow for Track B hero shots
- `list-numbered.ass` — for the `list_payoff` format with animated item transitions

### `overlays/`

PNG overlays composited on top of rendered video.

- `lumio-endcard-9x16.png` — 1080×1920 brand end-card, mostly transparent with Lumio logo + "Link in bio" text in the last 1-2 seconds. Disabled by default (`config.yaml:brand.endcard_seconds: 0`) until the account has follower baseline.

## Licensing

Every file committed to this directory must be either:
- Free for commercial use with license docs committed alongside (e.g., `Inter-LICENSE.txt`)
- Owned by Lumio Studio (brand assets)

Do **not** commit purchased stock assets (Envato, Storyblocks, etc.) — those violate most licenses when redistributed via a public skill.
