---
name: mini-decade:habits
description: Sync HabitAdd habits with MiniDecade plans — create, log, and pull analytics
argument-hint: "[field name] [--create|--log|--analytics]"
---
<objective>
Bridge between MiniDecade plans and HabitAdd habit tracking. Creates habits from plan objectives, logs completions, and pulls analytics for reviews.

Requires HabitAdd API config at:
`/Users/mehmetsemihbabacan/dev/brain/Work/Mine/MiniDecade/0. What is MiniDecade/Tools/.habitadd-config.json`

API reference: `/Users/mehmetsemihbabacan/.claude/skills/mini-decade/references/habitadd-api.md`
</objective>

<context>
Field name: $ARGUMENTS (optional — operates on all fields if omitted)
Flags:
- `--create` — Create new habits from plan objectives
- `--log` — Log today's habit completions
- `--analytics` — Pull completion analytics for reviews

API base: `https://us-central1-habits-x.cloudfunctions.net/`
</context>

<process>
1. **Read HabitAdd config** — get API key. If not found, tell user to set it up and exit.

2. **Read API reference** from `/Users/mehmetsemihbabacan/.claude/skills/mini-decade/references/habitadd-api.md`

3. **If `--create`:**
   a. Read field's Plan.md — extract current week's objectives
   b. Get existing habits via `agentGetHabits`
   c. Identify objectives that don't have matching habits
   d. For each new habit, call `agentCreateHabit` with:
      - Name format: `[Objective] ([Field Name])`
      - Type: check (for most) or number (for measurable goals)
      - Color: field-specific color
      - Frequency: daily
   e. Report created habits

4. **If `--log`:**
   a. Get all habits via `agentGetHabits`
   b. Show today's habits and ask which ones to mark complete
   c. Call `agentLogEntry` for each with today's date
   d. Report logged entries

5. **If `--analytics` (or no flag):**
   a. Get all habits via `agentGetHabits`
   b. For each field-related habit, call `agentGetAnalytics` with days=30
   c. Build analytics summary:
      - Current streaks
      - Completion rates
      - Trends (improving/declining)
   d. If field specified, include in next weekly review

6. **Output:** Summary table of habits with streaks and completion rates
</process>
