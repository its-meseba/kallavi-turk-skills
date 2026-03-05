---
name: mini-decade:research
description: Find and save resources for a MiniDecade field
argument-hint: "[field name] [topic]"
---
<objective>
Research resources (books, courses, articles, videos, tools) for a MiniDecade field and save structured notes to the vault. Updates the Resources Queue in Plan.md.
</objective>

<context>
Field name: first argument (ask if not provided)
Topic: second argument (optional — defaults to current quarter's focus from Plan.md)

Vault paths:
- Resources: `Work/Mine/MiniDecade/[Field]/Resources/`
- Plan: `Work/Mine/MiniDecade/[Field]/0. Plan.md` (Resources Queue section)
</context>

<process>
1. **Resolve field and topic** — read Plan.md to get current quarter focus if no topic given

2. **Search for resources** using WebSearch:
   - Search for books, courses, articles, YouTube videos related to the topic
   - Prefer free/open resources first
   - Find 5-10 relevant results

3. **For each resource**, create `Resources/[Resource Name].md`:
   ```markdown
   # [Resource Title]

   **Author/Source:** [Name]
   **URL:** [Link]
   **Type:** Book / Course / Article / Video / Tool
   **Relevance:** [Why this matters for the field]
   **Key Topics:** [Comma-separated list]
   **Estimated Time:** [Hours to complete]
   **Priority:** High / Med / Low
   **Status:** ⬜ Not started

   ## Notes
   [Empty — user fills in as they consume the resource]
   ```

4. **Update Resources Queue** in Plan.md — add new entries with priority

5. **Output:** Summary of resources found with relevance explanations
</process>
