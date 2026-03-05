---
name: mini-decade:new-field
description: Create a new MiniDecade mastery field with plan, resources, and goals
argument-hint: "[field name]"
---
<objective>
Create a new MiniDecade mastery field from scratch. Interviews the user about their background, goals, and time commitment, then creates the full folder structure, Plan.md, initial resources, and weekly goals.

**After this command:** Run `/daily-brain:goals` to set this week's goals for the new field.
</objective>

<context>
Field name: $ARGUMENTS (optional — ask if not provided)

Vault base: `/Users/mehmetsemihbabacan/dev/brain/Work/Mine/MiniDecade/`

Existing fields (check before creating duplicates):
AI Engineering, Context Engineering, Backend Engineering, SaaS Product, Entrepreneurship, Languages, Personal Growth
</context>

<process>
1. **If no field name provided**, ask the user what they want to learn/master

2. **Interview** (one question at a time):
   - Current experience level in this field
   - Hours per week they can dedicate
   - What "mastery" looks like to them (3-year target)
   - What they want to ship by end of this quarter (12-week capstone)

3. **Create folder structure:**
   ```bash
   FIELD_PATH="/Users/mehmetsemihbabacan/dev/brain/Work/Mine/MiniDecade/[Field Name]"
   mkdir -p "$FIELD_PATH/Resources" "$FIELD_PATH/Progress" "$FIELD_PATH/Artifacts" "$FIELD_PATH/Tools"
   ```

4. **Generate `0. Plan.md`** using the MiniDecade plan template:
   - Declaration from interview answers
   - Current Quarter section with 12 weekly objectives
   - Initial Skills Map (current vs target level)
   - First milestones
   - Empty Evidence Log and Resources Queue

5. **Research initial resources** using WebSearch:
   - Find 5-10 relevant books, courses, articles, videos
   - Prefer free/open resources first
   - Save each to `Resources/[Resource Name].md` with structured format
   - Populate Resources Queue in Plan.md

6. **Create HabitAdd habits** if config exists:
   - Read API key from `.habitadd-config.json`
   - Create 1-2 daily habits for the new field via agentCreateHabit

7. **Output:** Confirm field created, show Plan.md summary, suggest `/daily-brain:goals` to set weekly goals
</process>
