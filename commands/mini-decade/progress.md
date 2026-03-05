---
name: mini-decade:progress
description: Cross-field dashboard showing all MiniDecade fields and what to work on next
---
<objective>
Show a dashboard view of all MiniDecade fields with current status, then suggest what the user should work on next based on plan state, cadence day, and stale fields.
</objective>

<context>
Vault base: `/Users/mehmetsemihbabacan/dev/brain/Work/Mine/MiniDecade/`
Get real date with `date` command.
Weekly cadence: Mon Plan, Tue-Thu Build, Fri Ship, Sat-Sun Reflect
</context>

<process>
1. **Get current date and day of week**

2. **List all field directories** under MiniDecade (skip "0. What is MiniDecade")

3. **For each field**, read `0. Plan.md` and extract:
   - Field type (Primary/Secondary)
   - Current quarter focus
   - This week's objective and status
   - Next upcoming milestone
   - Last Evidence Log entry date (staleness check)
   - Overall weekly objectives completion rate

4. **Build dashboard table:**
   ```
   | Field | Type | This Week | Status | Next Milestone | Last Activity |
   |-------|------|-----------|--------|---------------|--------------|
   ```

5. **Suggestions based on current state:**
   - **Day-appropriate action:** "It's Monday — time to plan this week's objectives"
   - **Stale fields:** "You haven't logged anything for [Field] in 2+ weeks"
   - **Approaching milestones:** "Your [Milestone] is due in N weeks"
   - **Missing artifacts:** "Friday is ship day — what did you build this week?"
   - **Resource completion:** "You finished [Resource] — update your skills map"

6. **If HabitAdd config exists**, pull today's habit completion status via agentGetHabits + agentGetEntries

7. **Route to next action:**
   - Suggest specific `/mini-decade:` commands based on what's most impactful
   - E.g., "Run `/mini-decade:review Backend Engineering` — it's been 3 weeks since last review"
</process>
