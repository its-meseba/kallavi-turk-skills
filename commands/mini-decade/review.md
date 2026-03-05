---
name: mini-decade:review
description: Weekly or quarterly review of MiniDecade progress
argument-hint: "[field name] [--weekly|--quarterly]"
---
<objective>
Review progress for a MiniDecade field. Auto-detects whether to do a weekly or quarterly review based on the current date, but can be overridden with flags.

Weekly review: Compares planned vs actual, extracts lessons from daily-brain entries, suggests next week adjustments.
Quarterly review: Aggregates all weekly reviews, assesses against quarterly goals, proposes next quarter.
</objective>

<context>
Field name: $ARGUMENTS (ask if not provided)
Flags: `--weekly` or `--quarterly` to force review type

Vault paths:
- Plan: `Work/Mine/MiniDecade/[Field]/0. Plan.md`
- Progress: `Work/Mine/MiniDecade/[Field]/Progress/`
- Daily entries: `Daily Tracking/MM-YYYY/Week N/Daily/`
- Goals: `Daily Tracking/MM-YYYY/Week N/Goals.md`

Auto-detection: If current week is 12 (or last week of quarter), default to quarterly. Otherwise weekly.
Get real date with `date` command — never guess.
</context>

<process>
**Weekly Review:**
1. Get current date and calculate week number
2. Read field's Plan.md — find this week's objectives
3. Read daily-brain entries for this week tagged with `[Field Name]`:
   ```bash
   # Search entries for field tags
   obsidian-cli search-content "[Field Name]"
   ```
   Also read daily files directly from `Daily Tracking/MM-YYYY/Week N/Daily/`
4. Generate review:
   - Planned vs actual objectives (table)
   - Lessons learned (from daily entries)
   - Artifacts shipped
   - Blockers identified
5. Save to `Progress/YYYY-MM-DD.md`
6. Update Plan.md: mark weekly objective status (⬜→✅ or 🟡)
7. Suggest adjustments for next week
8. If HabitAdd config exists, pull this week's habit completion data via agentGetEntries

**Quarterly Review:**
1. Read all `Progress/*.md` files for this quarter
2. Read Plan.md quarterly goals and capstone
3. Assess:
   - Was capstone shipped? (Evidence Log check)
   - Skills gap closure (compare Skills Map current vs target)
   - Milestones hit/missed
   - Evidence Log entry count
4. Draft review section and append to Plan.md's Quarterly Reviews
5. If HabitAdd config exists, pull 90-day analytics via agentGetAnalytics
6. Suggest: `/mini-decade:plan [field] --next-quarter` to draft next quarter
</process>
