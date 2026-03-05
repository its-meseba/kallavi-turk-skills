---
name: daily-brain:log
description: Quick structured entry to today's daily brain note
argument-hint: "[what happened]"
---
<objective>
Log a structured entry to today's daily brain note. Auto-detects the category, adds timestamp, tags with MiniDecade field, and appends to the correct section.

This is the fastest path to capturing something — just tell me what happened and I handle the rest.
</objective>

<context>
Entry text: $ARGUMENTS (if empty, ask "What do you want to log?")

Vault path: `/Users/mehmetsemihbabacan/dev/brain/`
Daily note: `Daily Tracking/MM-YYYY/Week N/Daily/YYYY-MM-DD.md`

Category detection (from the entry text):
- "learned", "realized", "understood", "TIL", "figured out" → 📚 Learnings
- "feedback", "review", "told me", "suggested", "in the meeting" → 📋 Feedback
- "found", "discovered", "came across", "interesting" → 💡 Discoveries
- "failed", "broke", "mistake", "bug", "wrong" → 💥 Failures
- "idea", "what if", "could we", "maybe" → 💭 Ideas
- "goal", "want to", "plan to", "aim", "target" → 🎯 Goals
- "worked on", "built", "shipped", "implemented", "fixed" → 🔧 Work Notes

Field detection: Match keywords against known MiniDecade fields.
</context>

<process>
1. **Get current date and time:**
   ```bash
   date "+%Y-%m-%d"
   date "+%H:%M"
   date "+%d"  # for week calculation
   date "+%m-%Y"  # for folder
   ```

2. **Calculate folder path:**
   - MM-YYYY from date
   - Week N from day of month (1-7=Week 1, 8-14=Week 2, etc.)
   - Full path: `Daily Tracking/MM-YYYY/Week N/Daily/YYYY-MM-DD.md`

3. **Auto-detect category** from entry text using the detection table

4. **Auto-detect MiniDecade field** from keywords (AI, backend, Go, Swift, etc.)

5. **Format entry:**
   ```
   HH:MM — [Entry text][Context if provided][Takeaway/so-what]
   ```
   Add `[Field Name]` tag if field detected.

6. **Check if daily note exists:**
   - If exists, read it and append under the correct category section
   - If not, create it with the day summary line and category sections

7. **Append entry** using obsidian-cli or direct file operations:
   ```bash
   obsidian-cli open "Daily Tracking/MM-YYYY/Week N/Daily/YYYY-MM-DD" --append "content"
   ```
   Fallback to direct file write if obsidian-cli fails.

8. **Output:** Confirm entry logged with category and field tag shown
</process>
