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

```
**Executive Summary**

**Problem:** [One sentence — what's broken or missing]

**Solution:** [One sentence — the approach or path forward]

**Impact:** [One sentence — what changes when this is done]
```

4. **Decide on Context.** If there's genuinely useful background (links, prior decisions, constraints), add:

```
---

**Context**

[One paragraph max. Supplementary only — the 3 points above must stand on their own.]
```

If no useful context, skip it entirely.

5. **Present the summary** directly to the user.

## Quality Checks
- Each point is ONE sentence. No compound sentences with semicolons. No "and also."
- Problem states what's broken — not symptoms, not history
- Solution states the approach — not implementation details, not a task list
- Impact states what changes — in measurable or observable terms
- Context is optional and max one paragraph
</process>
