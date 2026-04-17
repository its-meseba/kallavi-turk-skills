---
name: shipyard:learn-lessons
description: Analyze the current mobile app project end-to-end (git history, plans, architecture, SDK integrations, localization, extensions) and extract learned lessons. Writes a project-local `docs/LESSONS-LEARNED.md` with systematic tables AND promotes new, generalizable lessons to the shared `~/.claude-shared/shipyard-lessons/` library. Use at any project milestone, after shipping a feature, or as a retrospective.
---

<objective>
Produce two outputs from a thorough analysis of the current project:

1. **Project-local** `docs/LESSONS-LEARNED.md` — a systematic, table-formatted document that a future reader (human or AI) can scan to understand what worked, what broke, and what this project's author would do differently next time.

2. **Library contributions** — for every lesson that is generalizable (not project-specific), a new file in `~/.claude-shared/shipyard-lessons/lessons/` with the schema defined in `SCHEMA.md`, plus an updated row in `INDEX.md`.

The goal is that every project you ship makes the next one easier.
</objective>

<library_location>
- Library root: `~/.claude-shared/shipyard-lessons/`
- Schema: `~/.claude-shared/shipyard-lessons/SCHEMA.md` — read this before adding lessons.
- Master index: `~/.claude-shared/shipyard-lessons/INDEX.md` — update after adding lessons.
- Template: `~/.claude-shared/shipyard-lessons/templates/lesson.md`.
</library_location>

<process>

### 1. Detect the project platform

Use the same detection logic as the shipyard SKILL.md:

| Signal | Platform |
|---|---|
| `project.yml` / `*.xcodeproj` | iOS (SwiftUI) → `ios-swiftui` |
| `build.gradle.kts` / `build.gradle` | Android (Kotlin/Compose) → `android-kotlin` |
| `pubspec.yaml` | Flutter → `flutter` |
| `package.json` + `app.json`/`app.config.js` | React Native (Expo) → `react-native-expo` |

Save the detected platform as `$PLATFORM` — every lesson you write will tag its `platforms:` field with it (plus `cross-platform` if the lesson applies broadly).

### 2. Gather project intelligence

Use `mcp__plugin_context-mode_context-mode__ctx_batch_execute` to avoid context flood. Collect in parallel:

```shell
# Commit archaeology
git log --all --oneline --reverse
git log --all --pretty=format:'%h|%s|%ad' --date=short
git log --all --pretty=format:'%s' -n 500 | sort | uniq -c | sort -rn | head -30   # top commit subjects
git log --all --oneline | grep -iE 'fix:|revert|ship-wreck|hotfix'                   # bug signal

# Plan / architecture / product docs
find docs -name '*.md' | head -50
find . -maxdepth 2 -name 'CLAUDE*.md' -o -name 'ARCHITECTURE*.md' -o -name 'PRODUCT*.md'

# SDK fingerprints (platform-adapted)
# iOS: grep -r "import Adapty\|import PostHog\|import Firebase" Runlock* || true
# Android: grep -r "com.posthog\|com.adapty\|firebase" app/build.gradle*
# Flutter: grep -E "posthog|adapty|firebase" pubspec.yaml
# RN: jq '.dependencies' package.json

# Localization surface
find . -name '*.xcstrings' -o -name 'strings.xml' -o -name 'intl_*.arb' -o -name 'app_*.arb'

# Extensions / native targets (iOS-specific)
grep -E '^\s+[A-Z][A-Za-z0-9]+:$' project.yml 2>/dev/null

# Memory records that inform lessons
ls ~/.claude-personal/projects/$(pwd | sed 's|/|-|g')/memory/ 2>/dev/null
```

Use `ctx_batch_execute` queries like:
- "architecture pattern service layer"
- "SDK integrations and initialization order"
- "ship-wreck reviews and bug fixes"
- "localization gaps and usage"
- "onboarding pivots and variants"
- "performance or crash incidents"

### 3. Extract lessons systematically

For each of these 10 dimensions, ask two questions — "what pattern emerged?" and "what mistake did we make?":

1. **Architecture** — module shape, DI, shared code, file organization.
2. **Platform** — OS-specific frameworks (HealthKit, Screen Time, WorkManager, etc.).
3. **SDK** — third-party init order, API key handling, analytics fan-out.
4. **Process** — git hygiene, plans, reviews, feature cadence.
5. **Product** — onboarding, paywall, virality, user positioning.
6. **Localization** — catalog choice, ViewModel strings, per-locale copy.
7. **Performance** — build time, runtime, memory, battery.
8. **Security** — secrets, entitlements, auth, PII.
9. **Deployment** — TestFlight/Play Store friction, CI/CD, provisioning.
10. **Design** — tokens, theming, accessibility.

Use `fix:` / `revert:` / `refactor:` commits as primary evidence. Every such commit is a candidate lesson — it documents a mistake that required a fix.

### 4. Classify each lesson

| Column | Values |
|---|---|
| Polarity | `require` (pattern to apply) or `avoid` (mistake to prevent) |
| Severity | `critical`, `high`, `medium`, `low` |
| Scope | `project-specific` (stays in `docs/LESSONS-LEARNED.md` only) or `generalizable` (also promoted to library) |

A lesson is **generalizable** if it would apply to at least one other project of the same platform — i.e., you can strip out project-specific names and it still makes sense.

### 5. Write the project-local document

Location: `docs/LESSONS-LEARNED.md` (create the directory if it doesn't exist).

Required structure:

```markdown
# <Project Name> — Lessons Learned

**Project:** <name>
**Platform:** <ios-swiftui | android-kotlin | flutter | react-native-expo>
**Build window:** <first-commit-date> → <last-commit-date>
**Stats:** <N> commits, <M> plan documents, <K> ship-wreck reviews.

---

## Summary table

| # | ID | Severity | Category | Polarity | Title | Library? |
|---|---|---|---|---|---|---|
| 1 | L-IOS-001 | critical | deployment | require | <title> | ✅ promoted |
| 2 | (local)   | medium   | product    | avoid   | <title> | — |

(One row per lesson. "Library?" shows whether it was promoted to `~/.claude-shared/shipyard-lessons/` or stays project-local.)

---

## Category tables

One table per category. Rows include: Mistake/Pattern, Why it matters (one line), Worked example (commit hash + file), Fix (one line).

---

## Metrics snapshot

Table: commit counts by type, plan count, locale count, SDKs integrated, targets, etc. — calibration data for future projects.

---

## The top N takeaways

Ranked list of the 5-10 highest-leverage lessons from this project specifically.
```

### 6. Promote generalizable lessons to the library

For each lesson marked `generalizable`:

1. Read `~/.claude-shared/shipyard-lessons/SCHEMA.md` and `templates/lesson.md`.
2. Assign the next available ID:
   - iOS-specific → `L-IOS-<next>`
   - Android-specific → `L-AND-<next>`
   - Flutter-specific → `L-FLU-<next>`
   - RN/Expo-specific → `L-RNE-<next>`
   - Cross-platform → `L-CRS-<next>`
   - Process → `L-PRC-<next>`
   Read `INDEX.md` to find the current max, add 1. IDs are never reused.
3. Create `lessons/<id>-<kebab-title>.md` with:
   - Full frontmatter (see SCHEMA.md).
   - `## Pattern` or `## Mistake` section.
   - `## Why it matters`.
   - `## Detect` — **must** include either a shell block labeled `# detect:` or a manual checklist. This is how `/shipyard:update-learned-lessons` checks future projects.
   - `## Fix` — ordered steps. Optionally include a `# fix:` shell block.
   - `## Worked example` — commit hashes + file paths from the source project.
   - `## Related` — IDs of adjacent lessons.
4. Append a row to `INDEX.md` — keep the table sorted by ID.
5. Update `INDEX.md` totals and source-projects table.

### 7. Before promoting, dedupe against existing library

Before assigning a new ID, read `INDEX.md` and scan every existing lesson that matches the same platform and category. If the candidate is substantially the same as an existing lesson:
- Do **not** create a duplicate.
- Instead, update the existing lesson's `last_verified` date and add this project to a `## Also observed in` section in the lesson file.
- Record the match in the project-local summary table as "reinforces L-XXX-NNN".

### 8. Commit

Create one commit per output:

```
docs: learned-lessons for <project>
```

and (if any library additions):

```
docs(shipyard-lessons): add L-XXX-NNN, L-XXX-NNN from <project>
```

The library commit lives in `~/.claude-shared/` — remind the user to run `bash ~/.claude-shared/scripts/sync-skills.sh` if they keep the lessons in the sync repo.

### 9. Report

End with a compact summary:

```
📚 Lessons extracted from <project>
   Project-local doc: docs/LESSONS-LEARNED.md
   New library lessons: L-IOS-008, L-CRS-011  (2)
   Reinforced existing: L-IOS-003, L-CRS-005  (2)
   Top 3 takeaways:
     1. <title>
     2. <title>
     3. <title>
```

</process>

<rules>
- **Never invent lessons that aren't supported by the project's git history.** Every lesson cites a commit, a file, or a memory record.
- **Project-local lessons are allowed** and often more valuable than promoted ones — don't force-generalize.
- **Never edit existing library lessons** except to update `last_verified` or append to `Also observed in`. Creating a superseding lesson is preferred.
- **Respect polarity**: a lesson is `require` OR `avoid` — if it's both, split into two lessons.
- **Filenames are kebab-case, imperative**: `register-extension-bundle-ids-early.md`, not `extensionBundleIds.md`.
</rules>

<triggers>
Invoke when the user says:
- "learn lessons from this project"
- "what have we learned from <project>"
- "do a retrospective"
- "analyze this project" (in a retrospective / post-mortem context)
- "/shipyard:learn-lessons"
</triggers>
