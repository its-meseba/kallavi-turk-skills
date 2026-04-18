# Hook Formats

The 6 short-form formats that actually convert for subscription mobile apps as of April 2026. Every hook in a batch should map to one of these. If a proposed hook doesn't fit any of these, it's either a new format worth explicitly adding to this doc, or (more likely) it's too vague.

---

## 1. `seven_second_pexels` — The Penelope Lopez format

The format that took Growy from zero to 1.3M views in 2 weeks. Works astonishingly well for subscription apps.

**Structure:**
- **0:00–0:04 (4 seconds):** Pexels b-roll loop relevant to the hook (person looking at phone, morning coffee, running shoes, etc.)
- **0:04–0:07 (3 seconds):** "Read caption 👇" or equivalent text overlay. Forces replays. Algorithm loves.
- **Text overlay from 0:00:** big, punchy, high-contrast. 1–2 lines max. THE HOOK LIVES HERE.
- **Voiceover:** optional. If present, reads the hook at :00–:04, pause at :04–:07.
- **Caption:** the actual value. List, story, or payoff. CTA at the end.

**When to use:** validation-stage hooks, Track A, zero-budget volume testing.

**Hook example:** "The 3 habits killing your focus (you do #2 every morning)"

**Why it works:** humans scroll → text hook catches attention → replay trigger extends watch time → algorithm amplifies → caption delivers value → CTA converts.

**YAML fields needed:**
```yaml
format: seven_second_pexels
hook_text: "The 3 habits killing your focus (you do #2 every morning)"
broll_query: "person on phone morning bed"
voiceover: "Three habits killing your focus..."   # optional
caption: "1. Checking phone in first 10 minutes...\n\nGet [App] free 👇"
cta: "Link in bio"
```

---

## 2. `ugc_reaction` — Real-human hook + screen recording

The format that actually converts for subscription apps in 2026, per the research doc. Outperforms pure-AI UGC on trial-to-paid by meaningful margins.

**Structure:**
- **0:00–0:03:** Real human reaction clip (DansUGC, $3–8 from marketplace). Shocked face, laughing, pointing at phone, etc.
- **0:03–0:10:** Screen recording of the app solving the problem.
- **0:10–end:** Human clip returns with reaction + verbal CTA, or text-only CTA over app screen.

**When to use:** post-validation — only for hooks that already showed Track A signal. Track B.

**YAML fields:**
```yaml
format: ugc_reaction
hook_text: "I didn't believe this app would work either..."
ugc_clip_id: "reaction_positive_female_25_v3"   # from .growth/ugc-library/
screen_recording: "habitadd_day_3_streak.mov"   # from app folder
voiceover: null                                  # UGC clip has its own audio
caption: "Day 3 and I'm hooked. Link in bio 💀"
cta: "Link in bio"
```

**Cost:** $3–8 per UGC clip + screen recording you shoot once. Reuse clips across 3–5 variations.

---

## 3. `before_after` — Problem / solution / proof

**Structure:**
- **0:00–0:02:** Problem state (frustrated person, chaotic phone, overwhelmed face) — Pexels OR AI-generated.
- **0:02–0:07:** Solution (app screen recording).
- **0:07–0:10:** After state — relief, success, clean phone, streak screen.

**When to use:** pain-point-heavy niches (productivity, fitness, finance).

**YAML fields:**
```yaml
format: before_after
hook_text: "From 6 unfinished habit trackers to one that actually sticks"
before_query: "frustrated person laptop"        # Pexels
app_demo: "habitadd_streak_demo_30sec.mov"
after_query: "relaxed person success"           # Pexels
voiceover: "I tried six different trackers..."
caption: "This is the only one I kept. Link below."
cta: "Bio link — 7 days free"
```

---

## 4. `screen_recording_narrated` — App demo with VO

The workhorse. Low effort, decent conversion when the app has a genuinely interesting moment to show.

**Structure:**
- **0:00–0:02:** Text hook overlay on first frame of app demo.
- **0:02–end:** App screen recording with voiceover walking through the feature.
- **Captions:** always — 85% of social is watched on mute.

**When to use:** feature launches, explainers, "how to use [app]" content.

**YAML fields:**
```yaml
format: screen_recording_narrated
hook_text: "The one setting that makes HabitAdd actually work"
screen_recording: "habitadd_smart_reminders_setting.mov"
voiceover: "Most habit apps bug you at random times. HabitAdd..."
caption: "Settings → Smart Reminders. Changed everything."
cta: "Try it — bio link"
```

---

## 5. `founder_pov` — Face-to-camera (real or AI Twin)

**Structure:**
- **0:00–0:10:** Face-to-camera hook + story + CTA, ~10–20 seconds.
- **Optional B-roll cutaways** to app screen at key moments.

**When to use:** origin stories, "why I built this," behind-the-scenes, response to user feedback. Trust-building format. Works especially well for solo founders.

**Two variants:**
- **5a. Real founder** — you film yourself on a phone. Zero API cost. Captions.ai Pro ($9.99/mo) for subtitle polish.
- **5b. AI Twin** — cloned version of yourself via Captions.ai AI Twin (one-time clone, then unlimited reuse). Good for bilingual content if you don't speak the target language natively.

**YAML fields:**
```yaml
format: founder_pov
variant: real   # or ai_twin
hook_text: "I built this app because I failed 4 other habit trackers"
script: "Full script goes here, ~30-50 words for ~15 seconds..."
broll_cutaways:
  - at: 0:05
    asset: "habitadd_home_screen.mov"
caption: "Real story. Link in bio if you want to try it."
cta: "Link in bio"
```

---

## 6. `list_payoff` — "5 things" / "3 reasons" format

**Structure:**
- **0:00–0:02:** Numbered hook ("5 habits that ruined my sleep — #3 shocked me")
- **0:02–end:** Rapid-fire list, 2–4 sec per item, each item = one b-roll clip + text.
- **Final item:** build suspense, highest-value item last.
- **End card:** the CTA.

**When to use:** listicle-friendly niches, educational angles.

**Pairs well with:** Pexels b-roll (cheap) OR Kling 2.5 Turbo for stylized cinematic (cheap-ish at $0.07/sec).

**YAML fields:**
```yaml
format: list_payoff
hook_text: "5 habits that ruined my sleep (#3 shocked me)"
items:
  - text: "1. Phone in bed"
    broll_query: "person scrolling phone dark"
  - text: "2. Late coffee"
    broll_query: "coffee mug evening"
  - text: "3. THIS one actually"    # highest-value
    broll_query: "person stressed laptop night"
  - text: "4. No wind-down"
    broll_query: "busy evening routine"
  - text: "5. Irregular schedule"
    broll_query: "clock chaos"
voiceover: "Five habits that ruined my sleep..."
caption: "HabitAdd tracks all 5 automatically. Bio link."
cta: "Bio link"
```

---

## Bilingual generation (IMPORTANT)

For apps targeting multiple languages (e.g., Adımla in TR + EN):

**Do NOT translate.** Generate each variant separately with the target audience's context in mind.

- **TR variant:** prompted with Turkish cultural references, Turkish YouTube/TikTok humor patterns, and Turkish pain-point phrasing mined from Turkish App Store reviews.
- **EN variant:** prompted with global-English audience framing, often more direct/ironic.

Translated hooks almost always underperform because:
- Idioms don't transfer ("gelmek gör" ≠ "come see" emotionally)
- Humor cadence is different
- Pain points are framed differently by culture (Turkish users complain differently about fitness apps than American users do)

The YAML captures this with a `language` field per hook, and a batch can (and usually should) contain both languages distributed across the right accounts.

```yaml
- id: h007
  format: seven_second_pexels
  language: tr
  hook_text: "Günde 10 bin adım atmayı nasıl başardım (tek hile)"
  ...

- id: h008
  format: seven_second_pexels
  language: en
  hook_text: "I finally hit 10k steps daily — one weird trick"
  ...
```

The scheduler (`schedule_post.py`) routes TR hooks only to TR accounts and EN hooks only to EN accounts based on `accounts.yaml`.

---

## Format selection heuristics

When generating a batch, aim for this distribution across the 20 hooks:

| Format | % of batch | Track | Cost |
|---|---|---|---|
| `seven_second_pexels` | 40% (8 hooks) | A | ~$0 |
| `list_payoff` | 20% (4 hooks) | A or hybrid | ~$0–2 |
| `screen_recording_narrated` | 15% (3 hooks) | A | ~$0 |
| `before_after` | 10% (2 hooks) | A | ~$0–1 |
| `ugc_reaction` | 10% (2 hooks) | B | $6–16 |
| `founder_pov` | 5% (1 hook) | A if real / B if AI Twin | ~$0 |

This keeps the batch majority-cheap for validation while seeding a few Track B hooks for the ones most likely to scale. Tune per-app in `.growth/config.yaml` under `batch_distribution:`.
