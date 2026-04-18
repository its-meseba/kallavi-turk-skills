# Submagic API

Submagic's Business tier ($41/mo annual) ships a **public API** that accepts a raw video and returns a finished vertical styled MP4 with burn-in captions, b-roll insertions, and auto-cuts. This is the single most useful paid SaaS API in the pipeline — it returns rendered video, not just data.

Use when: a hook on Track B or hybrid needs caption polish beyond what FFmpeg burn-in produces. Don't use on every Track A video — it's overkill for $0 validation clips.

## When NOT to use Submagic API

- Track A validation hooks — FFmpeg burn-in is good enough.
- Hooks where the caption style needs to match an exact brand template not in Submagic's library.
- When the input is already fully edited (you're paying for editing you don't need).

## When TO use

- All Track B hero videos.
- Hooks that have >5 words of dialogue (VO-heavy content benefits from Submagic's word-level caption animation).
- Content destined for YouTube Shorts specifically — YT Shorts rewards captioned content more heavily than TikTok/Reels.

## Integration

```python
# scripts/submagic_client.py (to be implemented)
import requests, os, time

def polish_video(input_mp4_path, style="neon-bold", language="en"):
    """Upload raw MP4 to Submagic, poll for completion, download result."""
    with open(input_mp4_path, "rb") as f:
        upload = requests.post(
            "https://api.submagic.co/v1/projects",
            headers={"Authorization": f"Bearer {os.environ['SUBMAGIC_API_KEY']}"},
            files={"video": f},
            data={"style": style, "language": language}
        )
    
    project_id = upload.json()["id"]
    
    # Poll
    for _ in range(60):
        status = requests.get(
            f"https://api.submagic.co/v1/projects/{project_id}",
            headers={"Authorization": f"Bearer {os.environ['SUBMAGIC_API_KEY']}"}
        ).json()
        if status["status"] == "completed":
            download_url = status["output_url"]
            break
        elif status["status"] == "failed":
            raise Exception(f"Submagic failed: {status.get('error')}")
        time.sleep(10)
    else:
        raise TimeoutError("Submagic timeout after 10 minutes")
    
    # Download
    output_path = input_mp4_path.replace(".mp4", "_submagic.mp4")
    with requests.get(download_url, stream=True) as r:
        with open(output_path, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
    return output_path
```

(Actual API endpoint paths need verification against current Submagic docs — this is a scaffold to start from.)

## Style presets

Store app-preferred styles in `.growth/config.yaml`:

```yaml
submagic:
  default_style: "neon-bold"
  hero_style: "cinematic-white"
  list_style: "bold-yellow"   # for list_payoff format
```

## Cost per video

At Submagic Business $41/mo annual with reasonable fair-use on the ~100 video/month cap: ~$0.41/video. Cheap relative to the production cost of Track B video generation.

## Fallback

If the Submagic API is unavailable or the account hits its cap:

- Fall back to FFmpeg + ASS subtitle rendering (`pexels-ffmpeg-recipe.md` § caption burn-in).
- Lower-fidelity but functional.

Never block a scheduled post on Submagic availability. Fall back and flag for human review.
