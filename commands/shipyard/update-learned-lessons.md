---
name: shipyard:update-learned-lessons
description: Scan the current mobile app project against every applicable lesson in `~/.claude-shared/shipyard-lessons/` and apply the fixes where gaps are detected. Platform-aware — only runs lessons tagged for the detected platform (iOS/Android/Flutter/RN Expo) plus cross-platform lessons. Produces a gap report and offers to auto-apply fixes.
---

<objective>
Proactively enforce every learned lesson from every past project on the current one. The command:
1. Detects the project platform.
2. Loads every applicable lesson from the shared library.
3. Runs each lesson's `Detect` check against the current codebase.
4. Classifies each as ✅ applied / ⚠️ gap / ❓ indeterminate / ➖ not applicable.
5. Presents gaps grouped by severity.
6. Offers to apply `Fix` steps — automated where a `# fix:` shell block exists, manual-guided otherwise.
7. Updates project-local `docs/LESSONS-LEARNED.md` with the applied lessons.

This command is **defensive** — it stops the current project from repeating past mistakes.
</objective>

<library_location>
- Library root: `~/.claude-shared/shipyard-lessons/`
- Index: `~/.claude-shared/shipyard-lessons/INDEX.md`
- Lesson files: `~/.claude-shared/shipyard-lessons/lessons/*.md`
</library_location>

<process>

### 1. Detect platform

Same logic as `shipyard:learn-lessons`:

| Signal | Platform tag |
|---|---|
| `project.yml` / `*.xcodeproj` | `ios-swiftui` |
| `build.gradle.kts` / `build.gradle` | `android-kotlin` |
| `pubspec.yaml` | `flutter` |
| `package.json` + `app.json` | `react-native-expo` |

Save as `$PLATFORM`.

### 2. Load applicable lessons

Read `~/.claude-shared/shipyard-lessons/INDEX.md`. Filter lessons where the `Platforms` column matches `$PLATFORM` OR is `all` / `cross-platform`. Also include `L-PRC-*` (process lessons, platform-agnostic).

For each applicable lesson, read the full file from `lessons/<id>-*.md` and parse:
- Frontmatter: `id`, `severity`, `polarity`, `applies_when`
- `## Detect` block — either shell code or checklist
- `## Fix` block — ordered steps + optional shell code

Skip any lesson where `applies_when` clearly doesn't hold (e.g., "project uses Firebase" when the project has no Firebase imports).

### 3. Run every Detect check

For each lesson:

1. If `## Detect` contains a shell block starting with `# detect:`, run it via `mcp__plugin_context-mode_context-mode__ctx_execute(language: "shell", ...)`.
2. Classify by exit code:
   - `0` = pattern is PRESENT (for `require` polarity, this means ✅ applied; for `avoid` polarity, this means ⚠️ mistake present — gap).
   - `non-zero` = pattern is ABSENT (for `require` polarity, this means ⚠️ gap; for `avoid` polarity, this means ✅ mistake absent — good).
3. If the `Detect` block is a manual checklist (no shell), mark as ❓ indeterminate and include the checklist in the report for the human to verify.
4. If `applies_when` cannot be satisfied (e.g., Firebase lesson on non-Firebase project), mark ➖ not applicable.

Store one row per lesson with: id, severity, status, evidence (exit code or stderr output).

### 4. Present the gap report

Format as a compact table, grouped by severity:

```
🛡  shipyard:update-learned-lessons — <project-name> (<platform>)

Scanned: <N> applicable lessons from ~/.claude-shared/shipyard-lessons/
Applied: <X> ✅   Gaps: <Y> ⚠️   Indeterminate: <Z> ❓   Not applicable: <W> ➖

CRITICAL gaps (<count>)
─────────────────────────────────────────────────────────────
⚠️  L-IOS-001  Register every extension bundle ID in week 1
    Evidence: RunlockShieldAction has no entitlements file
    Fix: see lessons/L-IOS-001-register-extension-bundle-ids-early.md#fix

HIGH gaps (<count>)
─────────────────────────────────────────────────────────────
⚠️  L-CRS-005  Route all analytics through a single AnalyticsRouter
    Evidence: 3 direct PostHogSDK.shared.capture calls found
              - Views/Dashboard/DashboardView.swift:142
              - Views/Paywall/PaywallView.swift:88
              - ViewModels/OnboardingViewModel.swift:203
    Fix (automated available): run fix block? [y/N]

MEDIUM / LOW gaps omitted by default — pass --all to show.

Indeterminate (manual check needed, <count>)
─────────────────────────────────────────────────────────────
❓ L-CRS-007  Share loop needs all four pieces
    Manual checklist — see lessons/L-CRS-007-virality-needs-all-four-pieces.md#detect
```

### 5. Offer to apply fixes

For each gap, ask the user which to apply:

1. **Batch mode**: "Apply all CRITICAL + HIGH fixes? [y/N]" — default no.
2. **Per-lesson**: loop through gaps in severity order, ask y/n per lesson.
3. For lessons with a `# fix:` shell block: run it with user confirmation.
4. For lessons without: print the ordered steps and pause for the user to confirm they've completed them.
5. After each applied fix, re-run that lesson's `Detect` to verify it now passes. If it still fails, flag for human attention.

**Never apply a fix without user confirmation** — fixes may touch many files, entitlements, or external dashboards.

### 6. Update project-local document

If `docs/LESSONS-LEARNED.md` doesn't exist, suggest running `/shipyard:learn-lessons` first.

If it exists, append an `## Update log` section (or add to existing one):

```markdown
## Update log

### 2026-05-01 — /shipyard:update-learned-lessons
Scanned 22 applicable lessons. Gaps found: 3. Applied: 2.

| ID | Action | Verified |
|---|---|---|
| L-IOS-001 | manual fix applied (registered bundle IDs) | ✅ |
| L-CRS-005 | automated fix (refactored 3 call sites) | ✅ |
| L-CRS-007 | deferred (landing page not yet needed) | ⏭ |
```

### 7. Commit

If fixes were applied, propose a commit:

```
chore: apply shipyard lessons L-IOS-001, L-CRS-005

- Registered extension bundle IDs in ASC
- Routed 3 direct analytics calls through AnalyticsRouter

Ref: ~/.claude-shared/shipyard-lessons/
```

Do NOT commit automatically — confirm with the user first.

### 8. Report summary

End with:

```
🛡  Update complete
   Applied: <N> fixes
   Deferred: <M> gaps (see docs/LESSONS-LEARNED.md update log)
   Re-run after significant changes to catch new gaps.
```

</process>

<flags>
- `--all`        include MEDIUM and LOW severity in the report (default: critical + high only).
- `--dry-run`    detect and report only, never apply.
- `--only <id>`  run a single lesson by ID.
- `--category <name>`  filter lessons by category (sdk, architecture, process, …).
- `--auto`       apply CRITICAL + HIGH automated fixes without per-lesson confirmation. Use with caution.
</flags>

<rules>
- **Platform filter is mandatory**. Never run an Android-tagged lesson on an iOS project.
- **Shell detect blocks must exit cleanly.** If a detect script errors, mark the lesson `❓ indeterminate` and do not auto-apply its fix.
- **Never modify lessons in the shared library** from this command — that's `shipyard:learn-lessons`' job.
- **Never apply a fix whose detect verification still fails after application** — flag for human review instead.
- **Respect `applies_when`** — skip lessons whose precondition isn't met.
- **Hooks / CI scripts** added by a fix must be reversible — suggest them in a PR rather than applying directly when they touch `.github/`, `Fastfile`, or `settings.json`.
</rules>

<triggers>
Invoke when the user says:
- "update learned lessons"
- "apply lessons to this project"
- "check this project against lessons"
- "what lessons am I violating"
- "/shipyard:update-learned-lessons"
- After `/shipyard:init` on a new project (proactive suggestion).
</triggers>
