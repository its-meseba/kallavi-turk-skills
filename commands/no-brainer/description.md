---
name: no-brainer:description
description: Generate an executive summary and update a Linear issue description with it. Use when starting a task — takes the issue content, distills it to Problem/Solution/Impact, and prepends it to the Linear issue description. Trigger when user says "update this issue", "add summary to issue", shares a Linear issue and wants it clarified, or is about to start working on an issue and wants the description cleaned up.
argument-hint: "[paste issue content or Linear issue ID/URL]"
---
<objective>
Generate a concise executive summary from the provided input and update the Linear issue description — prepending the summary at the top with a divider separating it from existing content.
</objective>

<context>
Input: $ARGUMENTS (if empty, ask "Which issue? Paste the content or share the Linear issue ID/URL.")
</context>

<process>
1. **Parse the input.** Determine if the user provided:
   - Raw text/content → use it directly for summarization
   - A Linear issue ID or URL → fetch the issue via Linear MCP tools first

2. **Read the input carefully.** Understand the full picture before summarizing.

3. **Identify the macro.** Ask yourself:
   - "If I had 10 seconds to explain this to a CEO, what would I say?" → Problem
   - "What are we doing about it?" → Solution
   - "Why should anyone care?" → Impact

4. **Write the summary** in this exact format:

```
**Executive Summary**

**Problem:** [One sentence — what's broken or missing]

**Solution:** [One sentence — the approach or path forward]

**Impact:** [One sentence — what changes when this is done]
```

5. **Decide on Context.** If there's genuinely useful background (links, prior decisions, constraints), add:

```
---

**Context**

[One paragraph max. Supplementary only — the 3 points above must stand on their own.]
```

6. **Present the summary** to the user for confirmation before updating.

7. **Update the Linear issue:**
   - Fetch the current issue description via Linear MCP (`get_issue`)
   - Prepend the executive summary at the top
   - Add a `---` horizontal rule divider between the summary and the existing description
   - Update the issue via Linear MCP (`save_issue`)
   - Confirm the update: "Updated [ISSUE-ID]: [issue title]"

## Quality Checks
- Each point is ONE sentence. No compound sentences with semicolons. No "and also."
- Problem states what's broken — not symptoms, not history
- Solution states the approach — not implementation details, not a task list
- Impact states what changes — in measurable or observable terms
- Context is optional and max one paragraph
- Always show the summary before updating — never update blind
</process>
