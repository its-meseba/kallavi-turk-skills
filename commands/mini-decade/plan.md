---
name: mini-decade:plan
description: Write or update a MiniDecade field's quarterly plan
argument-hint: "[field name] [--next-quarter]"
---
<objective>
Write or update the quarterly plan for a specific MiniDecade field. Can update the current quarter's weekly objectives or draft the next quarter's plan.

Use this at the start of a new quarter, when priorities shift, or when the user wants to restructure their approach.
</objective>

<context>
Field name: $ARGUMENTS (ask if not provided, or list fields and let user choose)
Flag `--next-quarter`: Draft next quarter's plan instead of updating current

Vault base: `/Users/mehmetsemihbabacan/dev/brain/Work/Mine/MiniDecade/`
Plan path: `[Field Name]/0. Plan.md`

**Always read the current Plan.md before making any changes.**
</context>

<process>
1. **Resolve field** — if no argument, list existing fields and ask user to pick one

2. **Read current Plan.md** — understand current state, progress, Skills Map

3. **If `--next-quarter`:**
   a. Read all Progress/ files from the current quarter
   b. Assess: Was capstone shipped? Skills gap closed? Milestones hit?
   c. Draft quarterly review section
   d. Propose next quarter: new focus, new capstone, 12 weekly objectives
   e. **Get user confirmation before writing**
   f. Update Plan.md with new quarter section

4. **If updating current quarter:**
   a. Show current weekly objectives table with status
   b. Ask what needs updating: objectives, milestones, skills map, or all
   c. Make targeted updates preserving existing progress
   d. Adjust upcoming weeks if behind/ahead of schedule

5. **After updating**, suggest:
   - `/mini-decade:research [field]` if Resources Queue is thin
   - `/mini-decade:habits [field]` to sync habit tracking
   - `/daily-brain:goals` to refresh weekly goals

6. **Confirm before major changes** — quarterly rewrites, dropping milestones, or restructuring objectives require user approval
</process>
