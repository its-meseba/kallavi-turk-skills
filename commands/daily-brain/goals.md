---
name: daily-brain:goals
description: Set or review weekly goals mapped to MiniDecade fields
argument-hint: "[--set|--review]"
---
<objective>
Set weekly goals or review current goals. Every goal maps to a MiniDecade field. Reads each field's Plan.md to extract this week's objectives and compiles them into the weekly Goals.md.

Use at the start of the week (Monday) to plan, or anytime to check progress.
</objective>

<context>
Goals file: `Daily Tracking/MM-YYYY/Week N/Goals.md`
MiniDecade plans: `Work/Mine/MiniDecade/[Field]/0. Plan.md`

Goals.md format:
```markdown
# Weekly Goals — Week N (MM-YYYY)

## Fields Active This Week
- [[AI Engineering]] | [[Context Engineering]] | ...

## 🎯 AI Engineering
- [ ] [Goal from Plan.md weekly objective]
- [ ] [Additional goal]

## 🎯 Context Engineering
- [ ] [Goal from Plan.md weekly objective]

## 🎯 Personal Growth
- [ ] [Goal]

---
*Updated: YYYY-MM-DD HH:MM*
```
</context>

<process>
**If `--set` or no Goals.md exists for this week:**

1. **Get current date** and calculate MM-YYYY + Week N

2. **Read each MiniDecade field's Plan.md:**
   - Find current week's objective in the weekly objectives table
   - Extract any upcoming milestones due this week/next

3. **For each active field**, compile goals:
   - Primary goal from Plan.md weekly objective
   - Ask user if they want to add extra goals for any field

4. **Write Goals.md** to `Daily Tracking/MM-YYYY/Week N/Goals.md`

5. **Show summary** with field links and goal counts

**If `--review` or Goals.md already exists:**

1. **Read current Goals.md**

2. **Read this week's daily entries** to check what was actually done:
   - Scan for `[Field Name]` tagged entries
   - Match against goals

3. **Show progress report:**
   ```
   | Field | Goals | Done | Progress |
   |-------|-------|------|----------|
   | AI Engineering | 3 | 2 | 🟡 67% |
   ```

4. **Suggest adjustments** if behind schedule

5. **Route:** If it's Friday+, suggest `/mini-decade:review [field]` for full review
</process>
