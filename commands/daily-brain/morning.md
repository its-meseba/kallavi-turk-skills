---
name: daily-brain:morning
description: Morning kickoff — today's agenda from goals, plan state, and habits
---
<objective>
Start the day with a focused briefing. Reads this week's goals, checks MiniDecade plan state for today's cadence day, pulls HabitAdd status, and creates today's daily note with the day summary line.

Best used first thing in the morning or at the start of a work session.
</objective>

<context>
Vault: `/Users/mehmetsemihbabacan/dev/brain/`
Daily note: `Daily Tracking/MM-YYYY/Week N/Daily/YYYY-MM-DD.md`
Goals: `Daily Tracking/MM-YYYY/Week N/Goals.md`
MiniDecade plans: `Work/Mine/MiniDecade/[Field]/0. Plan.md`
HabitAdd config: `Work/Mine/MiniDecade/0. What is MiniDecade/Tools/.habitadd-config.json`
HabitAdd API ref: `/Users/mehmetsemihbabacan/.claude/skills/mini-decade/references/habitadd-api.md`

Weekly cadence: Mon Plan, Tue-Thu Build, Fri Ship, Sat-Sun Reflect
</context>

<process>
1. **Get current date and day of week**

2. **Determine cadence phase:**
   - Monday → "📋 Plan Day — set objectives and prioritize"
   - Tuesday-Thursday → "🔨 Build Day — deep work on this week's objectives"
   - Friday → "🚀 Ship Day — finish and ship an artifact"
   - Saturday-Sunday → "🪞 Reflect Day — review the week and recharge"

3. **Read this week's Goals.md** — show incomplete goals grouped by field

4. **Read active MiniDecade Plan.md files:**
   - Extract this week's objective per field
   - Check for approaching milestones (within 2 weeks)
   - Note any stale fields (no activity in 2+ weeks)

5. **If HabitAdd config exists:**
   - Read API key
   - Call `agentGetHabits` to get all active habits
   - Call `agentGetEntries` for yesterday to show streak context
   - Show today's habits to complete

6. **Create today's daily note** if it doesn't exist:
   ```markdown
   > **Today:** [Cadence phase] — [Top 1-2 priorities from goals]

   ## 📚 Learnings

   ## 📋 Feedback

   ## 💡 Discoveries

   ## 💥 Failures

   ## 💭 Ideas

   ## 🎯 Goals

   ## 🔧 Work Notes
   ```

7. **Output morning briefing:**
   ```
   ☀️ Good morning! It's [Day], [Date] — [Cadence Phase]

   📋 Today's Focus:
   - [Top priority from goals]
   - [Second priority]

   🎯 This Week's Objectives:
   [Field]: [Objective] — [Status]

   ⚠️ Heads Up:
   - [Approaching milestone]
   - [Stale field warning]

   ✅ Habits to Complete Today:
   - [ ] [Habit 1]
   - [ ] [Habit 2]
   ```

8. **Open the daily note in Obsidian:**
   ```bash
   obsidian-cli open "Daily Tracking/MM-YYYY/Week N/Daily/YYYY-MM-DD"
   ```
</process>
