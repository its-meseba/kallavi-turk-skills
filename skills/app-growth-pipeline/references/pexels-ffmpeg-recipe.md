# Pexels + FFmpeg Recipe — Track A Zero-Cost Pipeline

The exact assembly recipe for the 7-second-hook format using Pexels API + FFmpeg + TTS. Near-zero cost per video. This is the workhorse of the validation track.

## Prerequisites

```bash
# System
apt install ffmpeg -y   # or brew install ffmpeg on macOS

# Python
pip install requests python-dotenv pyyaml

# Free Pexels API key: https://www.pexels.com/api/
export PEXELS_API_KEY=<key>
```

Assets in `~/.claude/skills/app-growth-pipeline/assets/`:
- `fonts/Inter-Black.ttf` — caption font (bundled; Inter is SIL OFL licensed, free for commercial use)
- `caption-styles/bold-yellow.ass` — ASS subtitle preset
- `overlays/lumio-endcard-9x16.png` — optional brand end-card

## The 7-second hook recipe

Target spec:
- **Dimensions:** 1080×1920 (9:16)
- **Duration:** exactly 7.0 seconds
- **Framerate:** 30 fps
- **Audio:** 48kHz stereo, -16 LUFS normalized
- **Format:** H.264 yuv420p, MP4 (universal compat on TikTok/Reels/Shorts)

### Step 1 — Fetch b-roll from Pexels

```python
import requests, os, random

def fetch_pexels_video(query, min_duration=8):
    r = requests.get(
        "https://api.pexels.com/videos/search",
        params={"query": query, "orientation": "portrait", "per_page": 15},
        headers={"Authorization": os.environ["PEXELS_API_KEY"]}
    )
    videos = [v for v in r.json()["videos"] if v["duration"] >= min_duration]
    if not videos:
        raise Exception(f"No suitable Pexels video for: {query}")
    
    video = random.choice(videos[:5])  # from top 5 results
    # Pick the 1080p or closest vertical file
    files = sorted(video["video_files"],
                   key=lambda f: abs((f.get("width") or 0) - 1080))
    portrait_files = [f for f in files if (f.get("height") or 0) >= (f.get("width") or 0)]
    best = portrait_files[0] if portrait_files else files[0]
    
    # Download
    out_path = f"/tmp/pexels_{video['id']}.mp4"
    with requests.get(best["link"], stream=True) as dl:
        with open(out_path, "wb") as f:
            for chunk in dl.iter_content(chunk_size=8192):
                f.write(chunk)
    return out_path
```

Pexels rate limit: 200 req/hr (free). Plenty for 20 hooks/batch.

### Step 2 — Generate voiceover (optional)

For hooks with `voiceover:` set. Use edge-tts for zero-cost prototyping, swap to Kokoro for production.

```bash
# edge-tts (free, prototype only)
pip install edge-tts
edge-tts --voice "en-US-AriaNeural" \
         --text "Three habits killing your focus..." \
         --write-media /tmp/vo.mp3

# Kokoro (free, self-hosted, better than edge-tts for production)
# See scripts/tts.py for integration
```

Normalize the VO:
```bash
ffmpeg -y -i /tmp/vo.mp3 -af "loudnorm=I=-16:LRA=11:TP=-1.5" \
       -ar 48000 -ac 2 /tmp/vo_norm.wav
```

### Step 3 — Burn in the hook text overlay

Static text overlay (visible the entire 7 seconds). Uses the `drawtext` filter with the bundled Inter-Black font.

```bash
HOOK="The 3 habits killing your focus"
FONT="~/.claude/skills/app-growth-pipeline/assets/fonts/Inter-Black.ttf"

ffmpeg -y -i /tmp/pexels_raw.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,\
crop=1080:1920,\
drawtext=fontfile=${FONT}:\
text='${HOOK}':\
fontsize=72:fontcolor=white:\
borderw=6:bordercolor=black:\
x=(w-text_w)/2:y=h*0.15:\
line_spacing=10" \
  -t 7 -r 30 -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p \
  -an /tmp/hook_video.mp4
```

For the 4-7s "Read caption 👇" replay trigger, use `enable='between(t,4,7)'`:

```bash
-vf "...,drawtext=text='Read caption 👇':fontsize=64:\
enable='between(t,4,7)':x=(w-text_w)/2:y=h*0.8:..."
```

### Step 4 — Mux VO (if present)

```bash
ffmpeg -y -i /tmp/hook_video.mp4 -i /tmp/vo_norm.wav \
       -c:v copy -c:a aac -b:a 128k -shortest \
       /tmp/hook_video_withvo.mp4
```

### Step 5 — Final output + platform specs

The output lands in `<app-repo>/.growth/videos/<batch>/<hook-id>.mp4`.

Validate:
```bash
ffprobe -v error -show_entries stream=width,height,duration,codec_name \
        -of default=noprint_wrappers=1 out.mp4
```

Must see:
- width=1080, height=1920
- duration ≈ 7.000000
- codec_name=h264 (video), aac (audio)

## Scaled assembly (20 hooks in one go)

`scripts/assemble_video.py` parallelizes with `concurrent.futures.ProcessPoolExecutor` — 4 workers by default. Each worker:

1. Fetches its own Pexels video (rate-limit backoff)
2. Generates TTS
3. Runs FFmpeg
4. Writes to the batch output dir

~20 hooks renders in ~3–5 minutes on a modern laptop (FFmpeg is the bottleneck, fully CPU-bound).

## Caption burn-in (vs platform auto-captions)

**Burn in your own captions.** Don't rely on TikTok/IG auto-captions — they default off, styling is ugly, and words are missed. Use ASS subtitles with the bundled style preset.

```bash
ffmpeg -y -i input.mp4 -vf "ass=assets/caption-styles/bold-yellow.ass" \
       -c:a copy output.mp4
```

Generate the ASS file programmatically from the VO transcript — `scripts/tts.py` writes a matching `.ass` alongside every `.wav`. If no VO, generate captions by splitting the hook text into readable chunks (aim for max 4 words / 1.2 sec on screen).

## End card (optional)

Append a 1-second brand card for recognition:

```bash
ffmpeg -y -i hook_video.mp4 -i assets/overlays/lumio-endcard-9x16.png \
  -filter_complex "[0:v][1:v]overlay=enable='gte(t,6)':x=0:y=0" \
  out.mp4
```

Skip for the first 2 weeks — endcards hurt completion rate until the account has some follower baseline.

## Cost check (for real)

20 hooks × (Pexels free + edge-tts free + FFmpeg local) = **$0.00**

Even at 100 hooks/day, Pexels free tier (200 req/hr) is fine. The only failure mode is Pexels returning the same video for common queries — mitigate by randomizing from the top 5 results, not picking result #1.

## When to upgrade to Track B

Not until a hook on Track A shows signal. See `track-selection.md`. The point of Track A is to find winners; the point of Track B is to amplify them.

## Troubleshooting

- **"drawtext: could not load font"** → use absolute path, escape spaces, check font file exists.
- **Output video is 1920×1080 instead of 1080×1920** → your Pexels result was landscape. Filter with `orientation=portrait` in the API call.
- **Audio out of sync** → use `-shortest` and ensure VO is exactly 7 seconds or less. Pad or trim the VO to match.
- **Captions cut off** → reduce `fontsize` or check `line_spacing`; test with the longest expected caption.
- **Pexels 429** → client wrapper has exponential backoff. If persistent, switch to Pixabay API (`scripts/pixabay_fallback.py` — not built yet, add when needed).
