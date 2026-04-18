# Tool Costs

Full pricing reference for every tool the pipeline can integrate with. Cross-reference with the research doc; re-verify quarterly. Prices as of April 2026.

## Quick-pick: the two sanctioned stacks

### Stack A — Volume + no humans (~$200/mo)

| Tool | Monthly | Usage |
|---|---|---|
| fal.ai (pay-as-you-go, video) | $40–80 | Track B hero shots only |
| Submagic API (Business) | $41 | Caption polish on Track B output |
| Repurpose.io (Starter) | $29 | Cross-post TikTok→Reels/Shorts, watermark strip |
| Postiz (self-host on $5 VPS) | $5 | Scheduling, unlimited accounts |
| Apify Starter | ~$50 | Weekly competitor sweeps |
| Claude API (Haiku 4.5 batch) | ~$17–34 | Script generation |
| Pexels + Pixabay APIs | $0 | Track A b-roll |
| edge-tts / Kokoro self-host | $0 | TTS for Track A |
| Singular Free + RevenueCat | $0 | Install attribution |
| **Total** | **~$185–240/mo** | |

### Stack B — Human UGC, hybrid (~$295/mo)

| Tool | Monthly | Usage |
|---|---|---|
| DansUGC (a la carte) | ~$60 | ~10–15 real-human reaction clips @ $3–8 |
| JoggAI Creator or HeyGen Creator | $29–39 | AI UGC for hook-testing volume |
| Captions.ai (Max) | $25 | Polish + AI Twin founder clips |
| fal.ai (pay-as-you-go) | $30 | B-roll for hybrid hooks |
| Hume Octave 2 + ElevenLabs (hero) | ~$28 | TTS |
| Blotato (Starter) | $29 | Multi-account scheduling + MCP |
| Apify Starter | $50 | Competitor intel |
| Firecrawl Hobby | $16 | Landing pages / web research |
| Envato Elements Core | $17 | Stock + templates + audio |
| Claude API (Sonnet 4.6 batch) | ~$50 | Higher-quality script generation |
| **Total** | **~$334/mo** (slightly over; optimize by dropping Envato if not used) | |

## By category

### AI video generation (Track B)

| Tool | Pricing model | Best for | Verdict |
|---|---|---|---|
| fal.ai | Pay-per-generation | Everything — aggregates all major models | **Primary** |
| Replicate | Pay-per-GPU-second | Models fal doesn't host | Fallback |
| Direct (Google Gemini, Runway) | Varies | None at our scale | Skip |

Per-model pricing: see `fal-backends.md`.

### AI UGC platforms

| Tool | Monthly | Per-video | API | Fit |
|---|---|---|---|---|
| **DansUGC** | $0 (a la carte) | $3–8 | Yes + free MCP | **Best for real-human hooks.** |
| HeyGen (Creator) | $29 | ~$3 | Paid API tier | Multilingual scale. |
| JoggAI (Creator) | $39 | Cheap | Yes | Best $/feature. AppSumo LTDs exist. |
| Arcads.ai | $110–220 | ~$11 | Pro only | Burns 1/3 of budget; situational. |
| Creatify (Business) | $99 | 2–20 credits | Yes | Mid realism, recognizable. |
| Synthesia | $89+ | — | Enterprise | **Skip for social.** Corporate vibe. |
| Captions.ai (Pro) | $10 | — | No (Scale tier only) | Best mobile editor + AI Twin. |

### Video repurposing / captions

| Tool | Monthly | API | Fit |
|---|---|---|---|
| **Submagic** (Business + API) | $41 | **Yes, indie-priced** | **Primary caption polish.** |
| Opus Clip | $15–29 | No (Business+ only) | Manual workflow only. |
| Klap | $29–79 | Yes (per-op) | ~$1.24/clip — pricey at volume. |
| Captions.ai | $10–25 | Limited | Mobile-first alternative. |
| Ssemble | $15 | Yes | Sleeper; low volume. |
| Vugola | $14–99 | No | Cheap manual; no API. |

### Social scheduling

| Tool | Monthly | Accounts | API | Fit |
|---|---|---|---|---|
| **Blotato** (Starter) | $29 | 20 (3 TikTok ×10/day) | **Yes + MCP** | **Primary** |
| Postiz (self-host) | ~$5–7 VPS | Unlimited | **Yes, REST** | **Backup / scale-up** |
| Upload-Post | $16 | 5 profiles | Yes | Alternative |
| Publer | $12–21 | Varies | Yes on paid | Budget option |
| Metricool | $18–53 | Brand-slot | Limited | Analytics-first |
| Repurpose.io | $29 | 3–10 networks | Limited | Watermark strip + cross-post |

### Competitor / trend intel

| Tool | Monthly | API | Fit |
|---|---|---|---|
| **Apify** (Starter + per-result) | ~$50 realistic | **Yes, REST** | **Primary for weekly sweeps** |
| Firecrawl (Hobby) | $16 | Yes | Landing pages |
| TikTok Creative Center + Meta Ads Library | $0 | No | **Essential — always use** |
| yt-dlp + npm scrapers | $0 | CLI/lib | Free fallbacks |
| PhantomBuster | $69+ | Limited | Skip — fragile on TT/IG |
| Sensor Tower / AppTweak / Pentos | $79+ | — | Skip — priced out |

### App Store review mining

| Tool | Monthly | API | Fit |
|---|---|---|---|
| app-store-scraper / google-play-scraper npm | $0 | Lib | **Primary** |
| Appfigures | ~$10 | Yes | Cheapest paid with API |
| Appbot Small | $49 annual | Yes | Best sentiment/theme mining |
| AppFollow | Free–$29 | Yes | Indie discount exists |

### TTS

| Tool | Cost/1M chars | Clone | Fit |
|---|---|---|---|
| edge-tts (unofficial) | $0 | No | **Prototype only** |
| Kokoro-82M (self-host) | ~$0–10 | No | **Production baseline** |
| Hume Octave 2 | ~$8 | Yes | **Best value expressive** |
| OpenAI gpt-4o-mini-tts | ~$10–20 | No | Steerable |
| Azure Neural TTS | $15 | Paid | Reliable |
| ElevenLabs Pro | $99 | Yes | **Hero voices only** |
| PlayHT | $31–99 | Yes | Acquisition uncertainty |

### Transcription / captions (raw)

| Tool | $/min | Fit |
|---|---|---|
| OpenAI GPT-4o Mini Transcribe | $0.003 | **Cheapest mainstream** |
| **Deepgram Nova-3** (batch) | $0.0043 | **Best value at scale** ($200 signup credit) |
| AssemblyAI Universal-2/3 | $0.0025+ | Bundled features |
| Whisper self-host | ~$0.005–6 infra | Only at 500+ hrs/mo |
| Submagic API | Bundled in $41 | Returns rendered video |

### Stock footage

| Tool | Monthly | API | Fit |
|---|---|---|---|
| **Pexels API** | $0 | **Yes** | **Primary video** |
| **Pixabay API** | $0 | **Yes** | Permissive license |
| Mixkit | $0 | No | Ad-safe supplements |
| Coverr / Videvo | $0–20 | No | Vertical loops |
| Envato Elements | $16.50 annual | No | Best paid breadth |
| Storyblocks | $21 annual | Enterprise | Volume, gated API |
| Artgrid | $20–50 annual | No | Premium cinematic |

### Attribution (app installs)

| Tool | Monthly | Free tier | Fit |
|---|---|---|---|
| **RevenueCat** | Free <$2.5k MTR | Yes | **Primary orchestrator** |
| **Singular Free** | $0 | **Full SKAN 4/5** | **Primary MMP** |
| Tenjin Paid | $20–200 flat | Free Starter (2k conv) | Once running paid UA |
| Firebase + GA4 | $0 | Yes | Android baseline |
| AppsFlyer / Adjust | $500–5000+ | Limited | **Skip until >$5k/mo UA** |

### Orchestration

| Tool | Monthly | Self-host | Fit |
|---|---|---|---|
| **Direct Python + cron** | $0 | — | **Default** |
| n8n self-host | ~$5–7 VPS | Yes | GUI when wanted |
| Make.com | $9–16+ | No | Per-op pricing inflates |
| Zapier | $30+ | No | **Skip** — too expensive |
| Activepieces / Windmill | Free OSS / $8–25 | Yes | Code-first alternatives |

### LLM (script generation, scraping synthesis)

Claude API pricing (April 2026):

| Model | Input $/M | Output $/M | Batch discount |
|---|---|---|---|
| Haiku 4.5 | $1 | $5 | −50% |
| Sonnet 4.5/4.6 | $3 | $15 | −50% |
| Opus 4.6/4.7 | $5 | $25 | −50% |

Prompt caching: up to −90% on repeated context. Use it aggressively for the brief — the brief is ~3k tokens and gets read ~10x/week per app.

Rough monthly estimate for 2 apps, 3 batches/week:
- Haiku for batches: ~$17–34/mo
- Sonnet for briefs: ~$20/mo
- Total: ~$40–55/mo

## Fixed vs variable

**Fixed monthly costs** (pay regardless of volume):
- Submagic $41 (if using)
- Blotato $29 (if using)
- Apify $50 (if using; can drop to $0 some weeks)
- Envato Elements $17 (if using)
- VPS for Postiz/n8n $5–7

**Variable** (scales with volume):
- fal.ai video generation
- DansUGC clip purchases
- Claude API tokens
- Deepgram/OpenAI transcription
- ElevenLabs (if hero VOs)

Keep variable under ~$100/mo by biasing toward Track A and only scaling Track B on validated winners.

## What's NOT in budget

- **AppsFlyer / Adjust paid** — $500+/mo, don't need until >$5k/mo UA.
- **Sensor Tower / AppTweak / data.ai paid** — $79–thousands, enterprise-priced.
- **Hootsuite / SocialPilot enterprise** — $99+/mo, cheaper options cover the need.
- **Zapier paid** — $30+/mo, Python + cron covers it.
- **Arcads Pro** — $220/mo, DansUGC + JoggAI hybrid is more cost-effective.
