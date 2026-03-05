---
name: daily-brain:review
description: Weekly or monthly summary of daily brain entries
argument-hint: "[--week|--month] [MM-YYYY]"
---
<objective>
Generate a summary of daily brain entries over a period. Weekly review covers the current week, monthly review aggregates across all weeks in a month.

Extracts patterns, themes, and actionable insights from logged entries.
</objective>

<context>
Flags:
- `--week` (default): Review current week's entries
- `--month`: Review all entries for a month
- `MM-YYYY`: Specific month to review (defaults to current)

Vault paths:
- Daily entries: `Daily Tracking/MM-YYYY/Week N/Daily/*.md`
- Goals: `Daily Tracking/MM-YYYY/Week N/Goals.md`
</context>

<process>
**Weekly Review:**

1. **Get current date**, calculate MM-YYYY and Week N

2. **Read all daily files** from `Daily Tracking/MM-YYYY/Week N/Daily/`

3. **Read Goals.md** for this week

4. **Analyze entries by category:**
   - Count entries per category (Learnings, Feedback, etc.)
   - Extract themes and patterns
   - Identify most active MiniDecade fields

5. **Generate summary:**
   ```markdown
   ## Week N Review (MM-YYYY)

   **Entries logged:** X across Y days
   **Most active field:** [Field Name] (N entries)

   ### 📊 By Category
   | Category | Count | Key Themes |
   |----------|-------|------------|

   ### 🎯 Goals Progress
   [From Goals.md — completed vs planned]

   ### 💡 Key Insights
   - [Pattern or recurring theme]
   - [Connection between entries]

   ### ⚡ Action Items
   - [Suggested follow-ups based on entries]
   ```

6. **Output directly** — don't save to vault (the mini-decade review saves the formal record)

**Monthly Review:**

1. **Read all weeks** for the specified month
2. **Aggregate across weeks:**
   - Total entries by category
   - Field activity distribution
   - Goals completion rate across weeks
   - Themes that persisted across weeks
3. **Generate monthly summary** with trends and recommendations
4. **Suggest:** `/mini-decade:review [field] --quarterly` if end of quarter
</process>
