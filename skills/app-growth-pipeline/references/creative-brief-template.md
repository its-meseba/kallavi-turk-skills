# Creative Brief Template

This is the structure for `<app-repo>/.growth/brief.md`. Every app's brief follows this shape. Regenerate weekly (or after any viral hit / notable dud) based on performance data and research.

The brief is the **single source of truth** for an app's content direction. Hooks, videos, and captions all derive from it. If the brief is vague, the content will be vague.

---

## Template

```markdown
# Creative Brief: <App Name>

*Last updated: <date> | Next refresh: <date+7>*

## 1. One-line positioning

<One sentence, under 20 words. Specific niche + specific audience + specific hook.>

Good: "The habit tracker for ADHD founders who have tried 5 other trackers and dropped them all."
Bad: "A habit tracking app." (too broad, no conversion angle)

## 2. Target user

- **Demographics:** age range, gender skew, country/language
- **Psychographic hook:** what they complain about on TikTok/Reddit/Twitter
- **Current workarounds:** what they use instead of your app today
- **Why they'd switch:** one sentence in their language, not yours

## 3. Core pain points (from reviews + community mining)

5–10 real quotes from App Store reviews or Reddit/TikTok comments. These are hook gold.

Each entry:
- Quote (paraphrased, under 15 words)
- Source (App Store / Reddit / TikTok comment)
- Hook angle this enables

## 4. Competitor account inventory

Top 3–5 accounts in the niche. For each:
- Handle(s) on TikTok + IG
- Follower count
- Average views on top 10 recent posts
- Their top hook format
- One hook worth adapting (not copying)

## 5. Top-performing hooks (your own, last 7 days)

From `logs/performance.jsonl`:
- Top 5 by views
- Top 5 by install attribution (if available)

Views and installs often disagree. Both matter — views feed algorithm, installs fund the app.

## 6. Angles to test this week

Ranked list of 5–10 new hook angles. Each:
- Angle name (e.g., "Morning routine mistake")
- Why now (what competitor/trend signal makes this timely)
- Format to use (see hook-formats.md)
- Track A or B?

## 7. Banned / avoid list

- Claims the app can't legally make (medical, financial, guaranteed results)
- Overused hooks in the niche everyone's already doing
- Aesthetic directions that don't fit the brand
- Competitor names to avoid naming directly

## 8. Brand and tone

- Tone (e.g., "warm + direct; never preachy; occasional dark humor")
- Visual direction (e.g., "natural light, handheld phone footage feel; avoid over-polished")
- Voice: first-person founder? User testimonial? Faceless voiceover?

## 9. CTA variants

3–5 call-to-action phrasings, rotated across the batch:
- "Link in bio — first week free"
- "Comment HABIT for the link"
- "Bio → 7 days free, cancel anytime"

## 10. Technical / account constraints

- Which accounts belong to this app (per `accounts.yaml`)
- Posting caps (usually 2–4/day max on TikTok, 1–2/day on IG)
- Language per account (TR-only, EN-only, or mixed)
- Timezone of primary audience (affects scheduling)
```

---

## Update cadence

Regenerate the brief:
- **Weekly** — routine refresh based on last week's performance.
- **After any viral hit** — update "top-performing hooks" immediately; the next batch should build on what worked.
- **After a dud week** — full re-research of competitors and pain points; something shifted.
- **On pivot** — full rewrite.

## Diff protocol

Never silently overwrite a brief. Produce a diff against the previous version and show the user:
- Added angles
- Removed angles (with reason)
- Changed tone/positioning
- New pain points discovered

User approves the diff before it's written to disk. Commit the brief to git after approval — the commit history is the app's growth story.
