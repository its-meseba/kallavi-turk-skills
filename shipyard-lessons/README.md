# Shipyard — Learned Lessons Library

A continuously-growing library of mobile app engineering lessons, extracted from every shipped project and applied to every new one.

## Location

```
~/.claude-shared/shipyard-lessons/
├── README.md           ← you are here
├── SCHEMA.md           ← lesson file format spec
├── INDEX.md            ← master table of all lessons (scannable)
├── lessons/            ← one markdown file per lesson (details + detect/fix)
└── templates/
    └── lesson.md       ← copy this for new lessons
```

## How this is used

Two slash commands from the `shipyard` skill operate on this library:

| Command | Direction | Purpose |
|---|---|---|
| `/shipyard:learn-lessons` | project → library | Analyze the current project, extract new lessons, append to library + write project-local `docs/LESSONS-LEARNED.md` |
| `/shipyard:update-learned-lessons` | library → project | Scan current project against every applicable lesson, report gaps, apply fixes |

## Lesson ID scheme

`L-<PLATFORM>-<NUMBER>` — stable, never renumbered, only retired.

| Prefix | Scope |
|---|---|
| `L-IOS-*` | iOS (SwiftUI) specific |
| `L-AND-*` | Android (Kotlin/Compose) specific |
| `L-FLU-*` | Flutter specific |
| `L-RNE-*` | React Native (Expo) specific |
| `L-CRS-*` | Cross-platform (applies to 2+ platforms) |
| `L-PRC-*` | Process (git, plans, reviews — platform-agnostic) |

## Severity

- **critical** — blocks shipping (crash, TestFlight reject, Play Store reject)
- **high** — breaks core UX / correctness (widget shows zeros, analytics drift)
- **medium** — quality / maintainability (design token drift, inconsistent naming)
- **low** — polish / nice-to-have

## Categories

`architecture` · `platform` · `sdk` · `process` · `product` · `localization` · `performance` · `security` · `deployment` · `design`

## Contribution flow

New lessons enter the library via `/shipyard:learn-lessons` running against a completed feature or project. The command prompts before promoting a project-specific observation to the shared library — only **generalizable** lessons are kept. Project-only observations stay in `docs/LESSONS-LEARNED.md`.

Lessons are never deleted. If superseded, set `superseded_by: <new-id>` in frontmatter and add a `## Retired` section explaining why.
