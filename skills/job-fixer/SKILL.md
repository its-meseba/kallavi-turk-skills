---
name: job-fixer
description: >
  A comprehensive job application assistant that turbocharges your job search using your CV,
  GitHub, LinkedIn, or any other profile source you share. Use this skill whenever a user
  wants to find jobs, tailor their CV to a specific role, write a cover letter, answer job
  application questions, address selection criteria, or improve their chances for a specific
  position. Triggers on: "find jobs for me", "help me apply", "tailor my CV", "write a cover
  letter", "answer these job questions", "what jobs match my background", "fix my resume for
  this role", "I uploaded my CV", "here is my GitHub", "what should I change in my CV",
  "selection criteria", "how do I answer this application question". Even if the user just
  drops a CV file, shares a link, or pastes a job URL — trigger this skill immediately if
  there's any hint of job searching, applying, or application improvement intent.
---

# Job Fixer

A runtime-adaptive job application assistant. No hardcoded profiles — the user provides their
info in the chat (documents, links, pasted text) and this skill does the rest.

---

## Core Principles

- **Never hallucinate.** Only use information explicitly provided by the user or found via web search.
- **Never invent experience.** CV suggestions reframe and reorder what exists — never fabricate.
- **Always be specific.** Generic output is useless. Every deliverable must reference the actual job and the actual candidate.
- **Respect the user's voice.** Suggested edits should sound like the user, not a template.
- **Honest gap analysis.** If the user doesn't match a requirement, say so — then suggest how to address it.

---

## Phase 0: Build the User Profile

At the start of each session, collect what the user has shared. Accept any combination of:

| Source | How to Handle |
|---|---|
| Uploaded CV/resume (PDF, DOCX, TXT) | Extract and parse all sections |
| GitHub link | Web-fetch the profile page; note pinned repos, languages, bio |
| LinkedIn URL | Web-fetch the public profile if accessible |
| Pasted text | Accept and parse inline |
| Portfolio / personal site | Web-fetch and extract relevant content |
| Any other document | Read and incorporate |

**If no profile is provided yet**, ask:
> "To get started, please share your CV (upload a file or paste the text), and optionally your GitHub or LinkedIn link. The more you share, the better I can tailor everything."

Once profile info is received, silently extract a structured profile:
```
name, current_role, target_roles, skills (technical + soft), experience_entries,
education, projects, publications, links, languages, certifications
```

Do NOT display the raw extracted profile unless the user asks. Just proceed.

---

## Phase 1: Understand the Request

After (or alongside) profile collection, identify what the user needs:

| User Intent | Go To |
|---|---|
| "Find jobs for me" | → Phase 2: Job Discovery |
| "I have a job / here's a URL / here's a screenshot" | → Phase 3: Job Analysis |
| "Tailor my CV for this role" | → Phase 4: CV Suggestions |
| "Write me a cover letter" | → Phase 5: Cover Letter |
| "Answer these questions / selection criteria" | → Phase 6: Application Q&A |
| Multiple at once | Handle them in order: 3 → 4 → 5 → 6 |

---

## Phase 2: Job Discovery

Search for jobs matching the user's background and stated goals.

### Search Strategy

Use `web_search` with targeted queries:
```
"[target role] job opening [year]"
"[key skill] engineer/analyst/developer jobs [location if given]"
"[industry] [role] [country] site:linkedin.com OR site:greenhouse.io OR site:lever.co"
```

For each result:
- Fetch the job listing page to get the full description
- Score it: **High / Medium / Low** match based on skill overlap, seniority fit, and topic alignment
- Note the application link

### Output Format

Present as a Markdown table:

| Role | Company | Match | Key Requirements | Link |
|---|---|---|---|---|
| ... | ... | 🟢 High | ... | [Apply](...) |

Then ask: *"Which of these would you like to pursue? I can analyze the full job description, suggest CV changes, write a cover letter, or answer application questions."*

---

## Phase 3: Job Analysis

When the user provides a job (URL, screenshot, pasted text):

1. **Fetch the full posting** — use `web_fetch` on the URL, or read the screenshot/text
2. **Extract structured requirements**:
   - Required skills (hard requirements)
   - Preferred skills (nice-to-haves)
   - Responsibilities
   - Selection criteria / competency questions (if listed)
   - Application format (what they ask for)

3. **Run a Gap Analysis** against the user's profile:

```
✅ Strong match: [skill/experience they clearly have]
⚠️  Partial match: [skill they have but could frame better]
❌ Gap: [requirement they don't have — honest assessment]
```

4. Ask the user which materials they want: CV suggestions, cover letter, Q&A answers, or all three.

---

## Phase 4: CV Suggestions

**Rules:**
- NEVER create a new CV from scratch
- ONLY suggest modifications to the existing CV
- Suggestions must be based on the actual job requirements vs. actual user experience
- Do not invent achievements, numbers, or projects

### Output Format

Present as a structured diff-style suggestion:

```markdown
## CV Suggestions for [Job Title] at [Company]

### Summary / Objective (if applicable)
**Current:** [existing text or "none"]
**Suggested:** [rewritten version targeting this role]
**Why:** [1-sentence rationale]

### Experience: [Most Relevant Entry]
**Current bullet:** [existing text]
**Suggested bullet:** [reframed version]
**Why:** [maps to requirement X in the JD]

### Skills Section
**Add to front:** [keywords from JD that user has but hasn't listed]
**Reorder:** [most relevant skills first for this role]

### What to Deprioritize
- [Irrelevant section or bullet — suggest moving to end or removing]

### Honest Gap Note
- ❌ [Missing requirement]: You don't have X. Consider [course / project / honest acknowledgment].
```

Keep suggestions minimal and impactful — 5–10 targeted changes, not a full rewrite.

---

## Phase 5: Cover Letter

Write a tailored cover letter based on the actual job and actual user profile.

**Structure:**
1. **Opening hook** — Reference something specific about the company/role (not "I am writing to apply for...")
2. **Why you / Why them** — 1–2 paragraphs connecting the user's strongest relevant experience to the role's key needs
3. **One concrete story** — A specific achievement or project that proves fit
4. **Vision / alignment** — Why this role, this company, now
5. **Close** — Confident and brief. Clear call to action.

**Length:** 300–400 words for industry. 400–550 for research/senior roles.

**Tone:** Professional but human. Avoid:
- "I am a highly motivated self-starter"
- "To Whom It May Concern"
- Restating the CV verbatim
- Vague claims with no evidence

Output as a clean Markdown block, ready to copy.

---

## Phase 6: Application Q&A and Selection Criteria

When the user provides job application questions (pasted, screenshotted, or from a fetched URL):

### For Standard Questions (Why this company? Tell us about a challenge, etc.)

Answer each question drawing from the user's actual profile:
- Specific, grounded in real experience
- 100–200 words per answer unless specified
- STAR format for behavioral questions (Situation → Task → Action → Result)
- Never fabricate

### For Selection Criteria (Common in government, academic, and Australian/UK roles)

Read the detailed guide: `references/selection-criteria-guide.md`

**Systematic approach:**
1. Parse each criterion (what competency is really being tested)
2. Find the best matching example from the user's experience
3. Write a STAR-format response for each criterion
4. Flag criteria where the user has weak evidence — suggest what to say honestly

Output as a numbered Markdown list matching the original questions.

---

## Phase 7: Quality Gate

Before delivering any output, check:

- [ ] Is every claim traceable to the user's provided profile or the job posting?
- [ ] Does the output mention something *specific* to this job and this candidate?
- [ ] Is the tone professional but not robotic?
- [ ] Are there any red flags (generic openers, invented experience, buzzword soup)?
- [ ] For CV suggestions: are these genuinely improvements, not just padding?

Fix anything that fails before outputting.

---

## Handling Partial Information

| Situation | Response |
|---|---|
| User gives job but no CV | Ask for CV before generating CV suggestions or cover letter |
| User gives CV but no job | Offer job discovery (Phase 2) or ask them to paste/link a job |
| Screenshot of job application | Treat screenshot as input — extract text visually and proceed |
| Job URL that fails to load | Ask user to paste the job description text directly |
| GitHub/LinkedIn that's private | Ask user to paste the relevant sections |

---

## Output Format Summary

| Material | Format |
|---|---|
| Job search results | Markdown table with match scores |
| Gap analysis | ✅/⚠️/❌ bullet list |
| CV suggestions | Diff-style Markdown (current → suggested + why) |
| Cover letter | Clean Markdown block |
| Application Q&A | Numbered Markdown list |
| Selection criteria | STAR-format Markdown per criterion |

---

## Reference Files

- `references/selection-criteria-guide.md` — Systematic approach to selection criteria (STAR method, government/academic formats, framing weak evidence)
- `references/cover-letter-guide.md` — Principles, tone, anti-patterns, and examples for writing excellent cover letters
