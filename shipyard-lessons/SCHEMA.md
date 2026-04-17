# Lesson File Schema

Every file in `lessons/` is a markdown document with YAML frontmatter and a fixed set of sections. Tooling depends on the structure — don't deviate.

## Filename

```
L-<PLATFORM>-<NUMBER>-<kebab-title>.md
```

Example: `L-IOS-001-register-extension-bundle-ids-early.md`

## Required frontmatter

```yaml
---
id: L-IOS-001
title: Short imperative sentence — what the reader should do
severity: critical | high | medium | low
category: architecture | platform | sdk | process | product | localization | performance | security | deployment | design
platforms: [ios-swiftui]            # any of: ios-swiftui, android-kotlin, flutter, react-native-expo, cross-platform
tags: [screen-time, extensions]     # free-form, lowercase-kebab
polarity: require | avoid           # require: pattern must be present. avoid: mistake must be absent
applies_when: "FamilyControls present in project.yml"   # one-line precondition
source_project: runlock
learned_at: 2026-04-17
last_verified: 2026-04-17
supersedes: []
superseded_by: null
---
```

## Required sections

### `## Mistake` (polarity=avoid) OR `## Pattern` (polarity=require)
One short paragraph (≤4 sentences). Plain language. No preamble.

### `## Why it matters`
One short paragraph. Link cause to consequence.

### `## Detect`
How to check if this lesson applies to a project. Either:
- **Checklist** — `- [ ] manual step` items a human can verify in minutes, OR
- **Shell block** — fenced ```shell block labeled `detect:` that exits 0 if the pattern is PRESENT, non-zero if ABSENT.

The `/shipyard:update-learned-lessons` command runs the `detect:` block to classify the project state.

Example:
```shell
# detect: exits 0 if AnalyticsRouter exists, 1 if missing
test -f "$(find . -name 'AnalyticsRouter.*' | head -1)"
```

### `## Fix`
Ordered steps to apply the pattern (or remove the mistake). Use numbered list. Can optionally include a ```shell block labeled `fix:` that the command offers to run.

### `## Worked example`
2-5 lines pointing at real code/commits from the source project. Include file paths and commit hashes where possible. This is what makes the lesson concrete.

## Optional sections

### `## Anti-patterns`
Bullet list of variations that look correct but aren't.

### `## Related`
Bullet list of other lesson IDs: `- L-CRS-005 — AnalyticsRouter fan-out`

### `## Retired`
Present only if `superseded_by` is set. One paragraph: why this was retired, what replaced it.

## Conventions

- **Tone**: imperative, terse, engineering-grade. "Do X" not "You might consider X."
- **No hedging**: if you're not sure, the lesson isn't ready.
- **One mistake per file**: don't bundle unrelated observations.
- **Cite the source**: every lesson frontmatter names its `source_project`. No anonymous lessons.
