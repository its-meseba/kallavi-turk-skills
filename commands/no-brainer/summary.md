---
name: no-brainer:summary
description: Boil down any input into a 3-point executive summary (Problem, Solution, Impact). Use when the user shares something verbose — a Linear issue, meeting notes, Slack thread, document — and wants the core takeaway distilled. Trigger on "summarize this", "break this down", "tldr", "what's the point", or any wall of text needing clarity.
argument-hint: "[paste content or describe the situation]"
---
<objective>
Generate a concise executive summary from the provided input. Present it directly — no Linear updates.
</objective>

<context>
Input: $ARGUMENTS (if empty, ask "What do you want me to summarize?")
</context>

<process>
1. **Read the input carefully.** Understand the full picture before summarizing.

2. **Identify the macro.** Ask yourself:
   - "If I had 10 seconds to explain this to a CEO, what would I say?" → Problem
   - "What are we doing about it?" → Solution
   - "Why should anyone care?" → Impact

3. **Write the summary** in this exact format:

```markdown
# Executive Summary

1. **Problem:** [One sentence — what's broken or missing]
2. **Solution:** [One sentence — the approach or path forward]
3. **Impact:** [One sentence — what changes when this is done]

**Context**

[One paragraph max. Supplementary only — the 3 points above must stand on their own.]

---
```

Formatting rules:
- `# Executive Summary` is always an H1 header
- Problem, Solution, Impact are a numbered ordered list (1. 2. 3.) with bold labels
- No divider before Context — it flows naturally after the 3 points
- Divider (`---`) goes AFTER Context, before any remaining content below
- Context section is optional — only include when genuinely useful. If no context needed, skip it entirely (no divider either)

4. **Present the summary** directly to the user.

## Quality Checks
- Each point is ONE sentence. No compound sentences with semicolons. No "and also."
- Problem states what's broken — not symptoms, not history
- Solution states the approach — not implementation details, not a task list
- Impact states what changes — in measurable or observable terms
</process>
