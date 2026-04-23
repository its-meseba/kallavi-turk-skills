# Reading Lens Chapter-Voice Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update the reading-lens SKILL.md to produce per-chapter pre-read briefs and post-read syntheses in author voice, grounded in close-reading extraction, dispatched via parallel subagents for setup.

**Architecture:** Single-file edit against `SKILL.md`. Two new prose sections added (Writing Voice, Close-Reading Extraction Discipline). Two templates rewritten (Pre-read Brief, Post-read Synthesis). Setup workflow steps 11–12 converted to parallel subagent dispatch. Book Overview template gains a `language:` frontmatter field. Quality Rules tightened. Changes land in `.claude-shared` source of truth, synced to `its-meseba/meseba-skills` via `sync-skills.sh`.

**Tech Stack:** Markdown (SKILL.md), Bash (sync script), Claude Code `Task` tool primitive for parallel subagent dispatch.

**Spec:** `/Users/mehmetsemihbabacan/.claude-shared/skills/reading-lens/docs/specs/2026-04-23-chapter-voice-design.md`

---

## File Structure

**Files modified by this plan:**
- `/Users/mehmetsemihbabacan/.claude-shared/skills/reading-lens/SKILL.md` — the single target file. All edits here.

**Files intentionally NOT modified (per spec §3):**
- `scripts/parse_epub.py`
- `config.yaml`
- All existing `.md` files in vault (existing chapter files — users can opt in to regeneration per chapter)

**No new files created** by this plan. Validation steps regenerate existing chapter files in place as part of testing.

**Git commits land in** `/Users/mehmetsemihbabacan/.claude-shared/skills/reading-lens/` via `sync-skills.sh` which fans out to `its-meseba/meseba-skills`.

---

## Task 1: Add "Writing Voice" section to SKILL.md

**Files:**
- Modify: `/Users/mehmetsemihbabacan/.claude-shared/skills/reading-lens/SKILL.md`

**Rationale:** The spec §4 defines the author-voice principle. SKILL.md currently has no dedicated section for writing voice — it's implicit in the templates. Making it explicit and placing it before the Templates section gives generators (main agent and subagents) a single reference point.

- [ ] **Step 1: Find the insertion point**

Open `/Users/mehmetsemihbabacan/.claude-shared/skills/reading-lens/SKILL.md`. Locate the heading `## Templates` (currently line 195, but search by heading text to be robust against drift).

- [ ] **Step 2: Insert the Writing Voice section immediately before `## Templates`**

Insert the following block on its own, with one blank line before and after:

````markdown
## Writing Voice

Every section of every brief and synthesis is written as the author speaking directly to the reader. First person throughout. Warm. Flowing. Complexity where earned, not performative.

- **Pre-read framing** — the author is about to walk the reader into the chapter: *"Before you dive in, here's what I'm doing in this chapter…"*
- **Post-read framing** — the author is reflecting with the reader: *"Now that you've made it through, here's what I hoped landed, and here's where I'd give ground to a sharp critic."*

First-person pronouns. Contractions are fine. No em-dash pileups (max one per paragraph; prefer sentence breaks). Plain English when plain English lands harder. Complexity only when the idea earns it.

### Author-character channeling

Each book has a distinct voice register. Fitzpatrick reads different from Kahneman reads different from Taleb. The generator identifies the register during the close-reading pass (see next section) and channels it through every section. Examples of what the register looks like in practice:

| Author | Register to channel |
|---|---|
| Rob Fitzpatrick (*The Mom Test*) | Self-effacing, colloquial ("cool", "awesome", "doomed", "gold dust"), anecdote-driven |
| Daniel Kahneman (*Thinking, Fast and Slow*) | Precise, measured, academic, "my colleague Amos and I" |
| Nassim Taleb (*Antifragile*) | Polemical, erudite, multilingual vocabulary, sardonic asides |
| Atul Gawande (*The Checklist Manifesto*) | Warm, physician-reflective, patient case studies |

The generator must not impose a single house style. Each book should feel genuinely different.

### One explicit voice break

In the post-read synthesis, the **Contrarian Take** section briefly leaves author voice for a critic, then returns. Frame it as:

> *"A sharp reader will push back here, and they'd be right about X —"*

then the specific pushback, concrete and biting. Then back to the author, graciously:

> *"I'd give ground on that. This is where my argument stretches further than my evidence can carry…"*

Every other section stays in author voice.
````

- [ ] **Step 3: Verify markdown is syntactically valid**

Run: `python3 -c "import markdown; markdown.markdown(open('/Users/mehmetsemihbabacan/.claude-shared/skills/reading-lens/SKILL.md').read())" 2>&1 | head -3`

If `markdown` is unavailable, fall back to a visual check: `grep -n '^## ' /Users/mehmetsemihbabacan/.claude-shared/skills/reading-lens/SKILL.md | head -30` — confirm the new `## Writing Voice` appears exactly once, immediately before `## Templates`.

Expected: no errors. The heading list should now show `## Writing Voice` followed by `## Templates`.

- [ ] **Step 4: Commit**

```bash
cd /Users/mehmetsemihbabacan/.claude-shared
git add skills/reading-lens/SKILL.md
git commit -m "reading-lens: add Writing Voice section

Codifies the author-voice-throughout principle, author-character
channeling with per-book register examples, and the explicit
voice-break rule for the Contrarian Take section.

Implements spec §4."
```

(If `.claude-shared` is not itself a git repo, skip this commit — the sync-skills.sh task at the end of this plan handles the canonical commit.)

---

## Task 2: Add "Close-Reading Extraction Discipline" section to SKILL.md

**Files:**
- Modify: `/Users/mehmetsemihbabacan/.claude-shared/skills/reading-lens/SKILL.md`

**Rationale:** Spec §7 requires a mandatory extraction pass before any brief/synthesis generation. Currently the skill has no such requirement — the generator goes straight from "load chapter text" to "fill template," producing shallow output. This section codifies the extraction as a workflow-level hard discipline.

- [ ] **Step 1: Find the insertion point**

Locate the `## Writing Voice` section added in Task 1. The new section goes immediately after it, before `## Templates`.

- [ ] **Step 2: Insert the Close-Reading Extraction Discipline section**

Insert the following block with one blank line before and after:

````markdown
## Close-Reading Extraction Discipline

**Required workflow step.** Before filling any pre-read or post-read template, the generator runs an internal extraction pass against the chapter text. The extraction output stays internal — it is the scratchpad the generator reasons over, and it does not appear in the chapter file.

Each bullet, term, and per-lens paragraph in the final output must be traceable to extracted material.

### The extraction pass (per chapter)

1. **Thesis** — the one sentence from the chapter that, reduced to ~25 words, survives. Verbatim or close paraphrase.
2. **Anchor phrases** — 8–12 verbatim phrases, metaphors, vivid images, canonical examples. The specific words the author uses ("bulldozer", "toothbrush", "fragile", "gold dust", "earlyvangelist", etc.). Every Watch-For bullet must attach to one.
3. **Defined terms** — 4–8 terms the author actively defines in the chapter, along with the author's own working definition (not a paraphrase). Pulled from the text, not invented.
4. **Author-voice register** — 2–3 sentences characterizing the author's voice in this chapter. Colloquial / academic / polemical / warm / etc. Specific turns of phrase. This register drives every section's voice.
5. **Structural role** — 1–2 sentences on what this chapter does in the book's argument. Example: *"It's the 'why rigor matters' beat before the rules in Ch 4."*

### Enforcement rule

**Do not proceed to template filling until extraction is complete.** Each bullet, term, and per-lens paragraph in the output must be traceable to an extracted item. If a Watch-For bullet has no anchor, if a Key Term has no source in the text, or if a per-lens paragraph has no extracted insight to ground on, return to the extraction pass before writing.

### Where extraction runs

- **`/reading-lens:brief N`** — the main agent runs extraction + generation for the single chapter.
- **`/reading-lens:synthesize N`** — same.
- **`/reading-lens:setup`** — each subagent runs extraction + generation for its assigned chapter batch. The book-level author-voice register (identified during `0. General.md` generation) is passed in as seed context; subagents refine it per chapter.
````

- [ ] **Step 3: Verify**

`grep -n '^## ' /Users/mehmetsemihbabacan/.claude-shared/skills/reading-lens/SKILL.md` — confirm the order is `## Writing Voice`, `## Close-Reading Extraction Discipline`, `## Templates`.

- [ ] **Step 4: Commit**

```bash
cd /Users/mehmetsemihbabacan/.claude-shared
git add skills/reading-lens/SKILL.md
git commit -m "reading-lens: add Close-Reading Extraction Discipline

Mandatory extraction pass (thesis, anchor phrases, defined terms,
voice register, structural role) before any template filling. Hard
enforcement rule. Applies to :brief, :synthesize, and :setup (each
subagent).

Implements spec §7."
```

---

## Task 3: Rewrite the Pre-read Brief template

**Files:**
- Modify: `/Users/mehmetsemihbabacan/.claude-shared/skills/reading-lens/SKILL.md`

**Rationale:** Spec §5 specifies a new template shape: 1-line author-voice thesis, 1–2 paragraph opener, phrase-anchored Watch For, author-voice Key Terms, checkbox Questions to Hold (philosophical, not action-oriented), full per-lens paragraphs. The current template is too terse and doesn't encode the voice/depth expectations.

- [ ] **Step 1: Locate the current Pre-read Brief template**

Search for the heading `### Pre-read Brief — fills \`## Pre-read brief\`` inside SKILL.md. The template runs from that heading until the next `### Post-read Synthesis` heading (which starts the next template section).

- [ ] **Step 2: Replace the entire Pre-read Brief template section**

Replace the block (heading through end of the code fence) with the following:

````markdown
### Pre-read Brief — fills `## Pre-read brief`

**Voice:** First person. The author is about to walk the reader into the chapter. See the *Writing Voice* section above. Channel the author-voice register extracted in close-reading step 4.

**Notation:** `[...]` marks a placeholder filled during generation. Placeholder descriptions are plain text — rendered output is plain prose, *not* italic, unless `*…*` is shown literally.

```markdown
> **[Author-voice one-line thesis — their own framing, not a
> summary of what the chapter covers]**

[Paragraph 1: 2–3 sentences. Author's voice. A personal opener —
"here's where I'm about to take you." Introduces the chapter's
concerns in the author's register.]

[Paragraph 2: 2–4 sentences. More explanatory. Gives the reader
enough context to understand what they're about to encounter.
Places the chapter in the book's arc — e.g., "I made the
asymmetric-risk argument back in Chapter 3 — this chapter builds
on that by showing you the three species of bad data I keep
seeing…"]

**Watch for**
- [Phrase-anchored bullet, 1–3 sentences, author voice. Cites a
  specific word, metaphor, anecdote, or moment from the chapter.
  Example: "When I drop the bulldozer metaphor in a bit, I mean
  something very specific — the founder who asks 'do you think
  this is a good idea?' and treats the nod they get as data."]
- [3–5 bullets total. Each grounded in an extracted anchor phrase
  from close-reading step 2.]

**Key terms**
- **Term** — Author-voice definition, 1–2 sentences. The author's
  own working vocabulary. No academic paraphrase. Sourced from
  close-reading step 3.
- [3–6 term→definition pairs total.]

**Questions to hold**
- [ ] [Open philosophical question the chapter raises, framed as
  the author asking the reader to wrestle with it. Not a personal-
  action question — the chapter's unresolved tensions.]
- [ ] [3–5 questions total.]

**Per-lens angles**

*{Role 1}.* [3–5 sentences of flowing author prose, directly
addressed to this lens. Names what the chapter asks of this role
specifically. Depth enough that the reader recognizes themselves
in it. Not a bullet disguised as a paragraph.]

*{Role 2}.* [Same depth, for this lens.]

*{Role N}.* [Same depth, for this lens. Always include every
configured lens as a separate paragraph — never collapse two
lenses into one entry.]
```

**Flexibility rules:**
- If the chapter is structurally a **comparison** (two patterns, two failure modes, before/after dialogue), render Watch For or Key Terms as a 2-column markdown table instead of a bulleted list.
- If the chapter describes a **sequential process**, Watch For may become a numbered list.
- **Per-lens angles never collapse** — always one paragraph per configured lens in the declared order, even if lenses share overlap.
- **Inline wikilinks allowed** when the chapter references an earlier chapter explicitly: `[[3. Talking to customers is hard|Chapter 3]]`.
````

- [ ] **Step 3: Verify**

`grep -n '^### ' /Users/mehmetsemihbabacan/.claude-shared/skills/reading-lens/SKILL.md | grep -A1 -B1 'Pre-read Brief'` — confirm the heading still exists exactly once.

- [ ] **Step 4: Commit**

```bash
cd /Users/mehmetsemihbabacan/.claude-shared
git add skills/reading-lens/SKILL.md
git commit -m "reading-lens: rewrite Pre-read Brief template

Author voice throughout. New 2-paragraph opener after the
one-liner. Phrase-anchored Watch For. Full 3-5 sentence paragraph
per lens. Flexibility rules for tables and wikilinks.

Implements spec §5."
```

---

## Task 4: Rewrite the Post-read Synthesis template

**Files:**
- Modify: `/Users/mehmetsemihbabacan/.claude-shared/skills/reading-lens/SKILL.md`

**Rationale:** Spec §6 specifies the new synthesis shape: author-voice core idea, 1–2 paragraph reflection, substantial Key Takeaways ending with mental-model naming, full per-lens takeaway paragraphs, Contrarian Take with explicit voice-break pattern, author-voice Connections, unchanged Flashcards.

- [ ] **Step 1: Locate the current Post-read Synthesis template**

Search for the heading `### Post-read Synthesis — fills \`## Post-read synthesis\`` inside SKILL.md. The template runs from there until the next `##` or `---` separator.

- [ ] **Step 2: Replace the entire Post-read Synthesis template section**

Replace with:

````markdown
### Post-read Synthesis — fills `## Post-read synthesis`

**Voice:** First person. The author is reflecting with the reader after the chapter. Channel the author-voice register. The Contrarian Take section is the one explicit voice-break — see *Writing Voice* above.

```markdown
> **[Author-voice one-line core idea — the sentence they'd want
> to survive this chapter]**

[Paragraph 1: 2–3 sentences in author voice. Reflecting on what
was just read together. Example: "Now that you've made it through,
here's what I most hoped landed, and here's why I built the
chapter the way I did."]

[Paragraph 2 (optional, chapter-dependent): 2–3 sentences. Where
the chapter fits in the book's running argument now that it has
done its work.]

**Key takeaways**
- [Substantial bullet, 1–2 sentences per bullet, author voice.
  4–6 total. No clipped labels — each bullet reads as a complete
  thought.]
- [Final bullet names the mental model the chapter builds, as a
  takeaway sentence. Example: "The model I hope you walk away
  with: false positives are asymmetric bets against your own
  runway."]

**Per-lens takeaways**

*{Role 1}.* [3–5 sentences of flowing author prose, directly
addressed to this lens. Monday-morning specific — what changes
in their week because of this chapter. Never a single sentence.]

*{Role 2}.* [Same depth.]

*{Role N}.* [Same depth, one paragraph per configured lens.]

**Contrarian take**

[2–3 paragraphs. Voice break: the critic speaks first.

"A sharp reader will push back here, and they'd be right about X —"
then the specific pushback, concrete and biting. Name the actual
claim that overreaches, not a vague "some might disagree."

Then back to author voice, graciously: "I'd give ground on that.
This is where my argument stretches further than my evidence can
carry…" and a short concession of where the critique lands.]

**Actionable experiments**
- [Concrete experiment a builder could run this quarter, 1–2
  sentences, author voice. 2–3 total. Scaled to a small team's
  reality.]

**Connections**
- **[Other book / framework]** — [1-sentence link in author
  voice. Example: "*Lean Startup* (Ries) — he wrote the
  learning-loop theory; I'm writing the script for what to say
  inside the loop."]
- [3–5 connections total.]

**Flashcards**
- **Q:** [Sharp question that tests the chapter's core move]
  **A:** [Under 30 words.]
- [3–5 pairs total.]
```
````

- [ ] **Step 3: Verify**

`grep -n '^### Post-read Synthesis' /Users/mehmetsemihbabacan/.claude-shared/skills/reading-lens/SKILL.md` — confirm the heading appears exactly once.

- [ ] **Step 4: Commit**

```bash
cd /Users/mehmetsemihbabacan/.claude-shared
git add skills/reading-lens/SKILL.md
git commit -m "reading-lens: rewrite Post-read Synthesis template

Author voice throughout. 1-2 paragraph reflection after core
idea. Mental-model naming in final Key Takeaway. Full per-lens
paragraphs. Explicit voice-break pattern for Contrarian Take.
Author-voice Connections.

Implements spec §6."
```

---

## Task 5: Convert setup workflow steps 11–12 to parallel subagent dispatch

**Files:**
- Modify: `/Users/mehmetsemihbabacan/.claude-shared/skills/reading-lens/SKILL.md`

**Rationale:** Spec §8 replaces the serial per-chapter generation in the main agent with a parallel subagent fan-out. For a 32-chapter book this yields ~4–8× speedup and keeps the main agent's context clean.

- [ ] **Step 1: Locate the current steps 11 and 12**

Inside `### /reading-lens:setup <epub-path>`, find the two workflow steps that begin:
- "11. **Generate pre-read briefs for every chapter.**"
- "12. **Generate post-read syntheses for every chapter.**"

These bullets were written for serial generation in the main agent.

- [ ] **Step 2: Replace steps 11 and 12 with a single consolidated parallel-dispatch step**

Replace both steps with the following block (renumbered so step 11 becomes the new combined step and step 12 is dropped; the subsequent step 13 becomes 12):

````markdown
11. **Generate pre-read briefs AND post-read syntheses for all chapters — in parallel via subagents.** Use Claude Code's `Task` tool to dispatch multiple subagents concurrently. For a book of N chapters, batch the chapters across 4–8 subagents (e.g., 32 chapters → 8 subagents handling 4 chapters each; 16 chapters → 4 subagents handling 4 chapters each; <8 chapters → one subagent). Each subagent receives, in its prompt:

    - Its assigned chapters' titles, numbers, and full text (inline, pulled from the cached EPUB JSON)
    - The book's extracted author-voice register from step 8
    - The book's thesis and the frozen lens list from step 6
    - The full **Pre-read Brief** and **Post-read Synthesis** templates from the Templates section above
    - The **Close-Reading Extraction Discipline** instructions
    - A direct write mandate — each subagent writes the completed brief and synthesis straight into the corresponding chapter file using the Edit tool

    The orchestrator (main agent) issues all subagent `Task` calls in a **single message** to trigger concurrent execution. See `superpowers:dispatching-parallel-agents` for the fan-out pattern.

    Each subagent, for each assigned chapter:
    1. Runs the close-reading extraction pass (thesis, anchor phrases, defined terms, voice register refinement, structural role)
    2. Fills the Pre-read Brief template
    3. Fills the Post-read Synthesis template, prepending the `> [!info] Generated at setup — no reader notes yet` callout
    4. Updates the chapter file's frontmatter: `brief_generated: <ISO-date>`, `synthesis_generated: <ISO-date>`, `synthesis_has_notes: false`, `status: synthesized`
    5. Returns a short status line: chapter number, success/failure, any warnings

    After all subagents return, the orchestrator verifies every chapter file has both sections filled and reports aggregate completion.
````

The subsequent numbered step (currently step 13, "Report") stays as-is but becomes step 12.

- [ ] **Step 3: Renumber any subsequent steps**

If there are steps after the old 12 (e.g., a step 13 reporting to user), decrement by 1. `grep -n '^[0-9]\+\. ' /Users/mehmetsemihbabacan/.claude-shared/skills/reading-lens/SKILL.md | head -20` — verify the numbering is sequential.

- [ ] **Step 4: Verify the `superpowers:dispatching-parallel-agents` skill reference is resolvable**

Run: `ls /Users/mehmetsemihbabacan/.claude-work/plugins/cache/claude-plugins-official/superpowers/ 2>/dev/null && echo "superpowers plugin available"`

Expected: the plugin path resolves. If not, the skill reference is still valid as long as superpowers is installed at invocation time — confirm by checking that `superpowers:dispatching-parallel-agents` appears in the available skills list during a live session.

- [ ] **Step 5: Commit**

```bash
cd /Users/mehmetsemihbabacan/.claude-shared
git add skills/reading-lens/SKILL.md
git commit -m "reading-lens: parallel subagent dispatch for setup

Replaces serial per-chapter generation with a single parallel
Task-tool fan-out. 4-8 subagents handle chapter batches
concurrently. Each subagent runs close-reading extraction +
generation + direct file write. Main agent orchestrates and
verifies.

Implements spec §8."
```

---

## Task 6: Add `language:` field to the Book Overview frontmatter template

**Files:**
- Modify: `/Users/mehmetsemihbabacan/.claude-shared/skills/reading-lens/SKILL.md`

**Rationale:** Spec §9 adds per-book language support. The book's language is stored in `0. General.md` frontmatter so `:brief` and `:synthesize` commands can read it without the user re-specifying.

- [ ] **Step 1: Locate the Book Overview template**

Find the heading `### Book Overview — content for \`0. General.md\``. Inside, find the YAML frontmatter block that starts with `---` and contains `type: book`, `title: "{title}"`, etc.

- [ ] **Step 2: Add the `language` field to the frontmatter template**

In the YAML frontmatter block, after the existing `chapters: {N}` line and before the `lenses:` line, add:

```yaml
language: {ISO 639-1 code, default: en}
```

So the relevant portion of the frontmatter becomes:

```yaml
---
type: book
title: "{title}"
author: "{author}"
source_epub: "{absolute-epub-path}"
status: reading
started: {YYYY-MM-DD}
chapters: {N}
language: {ISO 639-1 code, default: en}
lenses:
  - role: "{Role 1}"
    interests: "{interests}"
  - role: "{Role 2}"
    interests: "{interests}"
tags: [book, reading-lens]
---
```

- [ ] **Step 3: Add language-detection logic to the setup workflow**

Find step 6 of `/reading-lens:setup` ("Resolve lenses"). After it, and before step 7 ("Create folder + cache"), insert a new step:

````markdown
7. **Detect language for this book.** Check the user's setup invocation message for a language directive (e.g., "do it in Turkish", "yap bunu Türkçe", "auf Deutsch"). If detected, set `language: <code>` for this book (e.g., `tr`, `de`). Default: `en`. Confirm the detected language back to the user before proceeding: *"I'll generate this book's analysis in {Turkish}. Confirm?"* Wait for confirmation, then continue.
````

Renumber subsequent steps (old step 7 becomes 8, etc.) so the numbering stays sequential through the end of the `:setup` workflow.

- [ ] **Step 4: Update the per-command workflows to honor the language field**

In `/reading-lens:brief <N>` workflow, add a new step between step 1 and step 2:

````markdown
2. **Read language from `0. General.md` frontmatter.** Generate output in that language. Preserve author-voice register across translation.
````

Renumber subsequent steps.

Do the same for `/reading-lens:synthesize <N>` — add an equivalent step reading the language field.

For `/reading-lens:overview-redo`, add a step:

````markdown
2. **Detect language override.** If the user's invocation includes a new language directive, update the `language:` field in frontmatter. Otherwise preserve the existing value.
````

- [ ] **Step 5: Verify**

`grep -n 'language:' /Users/mehmetsemihbabacan/.claude-shared/skills/reading-lens/SKILL.md` — confirm the field appears in the frontmatter template and is referenced in the per-command workflows.

- [ ] **Step 6: Commit**

```bash
cd /Users/mehmetsemihbabacan/.claude-shared
git add skills/reading-lens/SKILL.md
git commit -m "reading-lens: add per-book language support

language: ISO 639-1 field in 0. General.md frontmatter. Default
en. Setup workflow detects language from invocation message and
confirms with user. :brief, :synthesize, :overview-redo read the
field and generate in that language while preserving author-voice
register.

Implements spec §9."
```

---

## Task 7: Tighten Quality Rules

**Files:**
- Modify: `/Users/mehmetsemihbabacan/.claude-shared/skills/reading-lens/SKILL.md`

**Rationale:** Spec §11 calls for tighter Quality Rules to prevent the specific failure modes observed on *The Mom Test* setup: collapsed per-lens angles, unanchored Watch-For bullets, generic paraphrase instead of author voice.

- [ ] **Step 1: Locate the Quality Rules section**

Find the heading `## Quality Rules` (or `## Quality` if the exact heading differs).

- [ ] **Step 2: Replace the entire Quality Rules section with**

````markdown
## Quality Rules

These rules are not optional. They convert the reading-lens output from a competent book summarizer into a genuinely useful reading companion. Enforce them on every generation.

### Voice and flow

- **Author voice throughout.** First person. Channel the author-voice register identified in close-reading step 4. See the *Writing Voice* section.
- **Flow over friction.** Sentences must read aloud smoothly. No em-dash pileups (max one per paragraph). No noun-stacked Latinate phrases when plain English does the job. Contractions are fine. Complexity only when the idea earns it.
- **No generic MBA platitudes.** Every takeaway must be specific enough that a reader who skipped the chapter could still lose an argument with one who read it. Bad: "focus on customers." Good: "Ries argues the unit of progress is the validated learning cycle — not revenue, users, or ship velocity."

### Grounding

- **Every Watch-For bullet must cite a specific phrase, metaphor, anecdote, or moment from the chapter text.** No unanchored observations. If there's no anchor, cut the bullet.
- **Every Key Term must come from the author's own vocabulary.** Pulled from the chapter text (close-reading step 3), not invented.
- **The close-reading extraction pass is mandatory.** Do not proceed to template filling without it.

### Per-lens rigor

- **Per-lens angles never collapse.** Every configured lens gets its own paragraph (3–5 sentences) in the declared lens order. Never combine two lenses into one line.
- **Lens paragraphs must be role-specific.** If a PM paragraph would read identically as a CEO paragraph, both are wrong. Rewrite until they diverge.
- **Monday-morning specificity in post-read takeaways.** A PM should be able to name one thing that changes in their week because of the chapter. Same for CEO and Entrepreneur.

### Contrarian rigor

- **Contrarian takes must bite.** "Some readers might disagree" is not a contrarian take. Name the specific claim and say why it overreaches, ignores something, or is wrong.
- **The voice-break pattern is required.** The critic speaks first, then the author graciously concedes. See *Writing Voice → One explicit voice break*.

### Other

- **Actionable experiments must fit a small startup.** Not "hire a data science team" — "add an event to track X in the existing analytics for Y feature, run for 2 weeks, compare to the Z cohort."
- **Never fabricate.** If the chapter text is thin or the topic is outside your confidence, say so in-line rather than inventing.
- **Respect the user's notes.** Never modify `## ✍️ My notes`. When generating a notes-aware synthesis upgrade, read the user's content and weave it in — their framing is data.
- **Never delete files. Ever. When in doubt, ask.**
- **Ask before overwriting.** Every regeneration is a deliberate choice, confirmed by the user.
````

- [ ] **Step 3: Verify**

`grep -n '^### ' /Users/mehmetsemihbabacan/.claude-shared/skills/reading-lens/SKILL.md | grep -B1 -A10 'Quality Rules'` — confirm the subsections are present: Voice and flow, Grounding, Per-lens rigor, Contrarian rigor, Other.

- [ ] **Step 4: Commit**

```bash
cd /Users/mehmetsemihbabacan/.claude-shared
git add skills/reading-lens/SKILL.md
git commit -m "reading-lens: tighten Quality Rules

Adds grounding rules (every Watch-For cites a phrase, every Key
Term from author's vocabulary). Per-lens rigor (never collapse,
role-specific divergence, Monday-morning specificity). Contrarian
rigor (must bite, voice-break required). Voice and flow rules
(no em-dash pileups, no platitudes).

Implements spec §11."
```

---

## Task 8: End-to-end consistency pass

**Files:**
- Modify (if drift found): `/Users/mehmetsemihbabacan/.claude-shared/skills/reading-lens/SKILL.md`

**Rationale:** Seven preceding edits can introduce inconsistencies. This task is a full read-through to catch cross-reference drift (e.g., the Writing Voice section references the Close-Reading section; verify the referenced heading exists).

- [ ] **Step 1: Read the entire SKILL.md top to bottom**

Command: `cat /Users/mehmetsemihbabacan/.claude-shared/skills/reading-lens/SKILL.md | less` (or use the Read tool for chunks if piping).

Check:
- All `## ` and `### ` headings match the order declared in the Templates section above (Book Overview → Chapter Stub → Pre-read Brief → Post-read Synthesis)
- Writing Voice and Close-Reading Extraction Discipline sections both exist, in order, before Templates
- Setup workflow step numbers are sequential, no gaps or duplicates
- Per-command workflows (`:brief`, `:synthesize`, `:overview-redo`) all reference the `language:` field
- Every `see *X*` cross-reference in prose points to an existing heading
- No `*[...]*` italic placeholder patterns remain in either template (they should be plain `[...]`)

- [ ] **Step 2: Fix any drift found**

For any issue found in step 1, edit the relevant section in place.

- [ ] **Step 3: Verify the file parses as valid markdown**

`python3 -c "import sys; content = open('/Users/mehmetsemihbabacan/.claude-shared/skills/reading-lens/SKILL.md').read(); print('headings:', content.count('## '), 'code fences:', content.count('\`\`\`'))"`

Expected: code-fence count is even (every opened fence is closed). Heading count should match a hand count (there are at least 12 `## ` sections: Why This Exists, Model & Thinking, Sub-commands, Configuration, Vault Structure, Lens Selection Flow, Update-Don't-Delete Safety, Workflow, Writing Voice, Close-Reading Extraction Discipline, Templates, Quality Rules, What This Skill Is NOT, Help Output).

- [ ] **Step 4: Commit (only if drift was fixed)**

```bash
cd /Users/mehmetsemihbabacan/.claude-shared
git add skills/reading-lens/SKILL.md
git commit -m "reading-lens: consistency pass fixes

End-to-end read-through caught cross-reference drift and
placeholder-italic leftovers. Fixed inline."
```

If no drift was found, skip the commit.

---

## Task 9: Sync to meseba-skills repo

**Files:**
- No file edits. Runs `sync-skills.sh`.

**Rationale:** The canonical git commit lives in `its-meseba/meseba-skills` per the `SYNC_CUSTOM_SKILLS` rule. Up to this point all commits have been local to `.claude-shared` (if at all). This task pushes to the shared repo.

- [ ] **Step 1: Run sync-skills.sh**

```bash
bash /Users/mehmetsemihbabacan/.claude-shared/scripts/sync-skills.sh
```

Expected output tail:
```
[main <hash>] sync: update custom skills YYYY-MM-DD
 N files changed, …
To github.com:its-meseba/meseba-skills.git
   <old>..<new>  main -> main
Skills synced successfully!
```

If the output says "No changes to sync," either (a) all Task 1–8 edits were in a `.claude-shared` path not covered by the sync script, or (b) the sync script was already run after Task 8. Check by diffing: `diff -r /Users/mehmetsemihbabacan/.claude-shared/skills/reading-lens/ /tmp/meseba-skills-sync/skills/reading-lens/ 2>&1 | head -20`. If no diff, the sync succeeded.

- [ ] **Step 2: Verify the commit landed on GitHub**

```bash
gh api repos/its-meseba/meseba-skills/commits --jq '.[0].commit.message' 2>&1 | head -3
```

Expected: the most recent commit message matches `sync: update custom skills YYYY-MM-DD`.

- [ ] **Step 3: No local commit needed for this task**

The sync script handles the commit and push. Skip a separate `git commit` here.

---

## Task 10: Validation — re-run `/reading-lens:brief 3` on The Mom Test

**Files:**
- Regenerates: `/Users/mehmetsemihbabacan/dev/brain/Reads/The Mom Test (Rob Fitzpatrick)/3. Talking to customers is hard.md`

**Rationale:** Spec §12 calls for a quality gate against the reference screenshot. Chapter 3 is a good test case: medium length, contains vivid metaphors (bulldozer, toothbrush, Habit anecdote, textbook-vs-checkbook), has all three lens angles applicable.

- [ ] **Step 1: Invoke the skill**

In a Claude Code session with reading-lens installed:

```
/reading-lens:brief 3
```

- [ ] **Step 2: Review the regenerated Pre-read brief section of chapter 3**

Open `/Users/mehmetsemihbabacan/dev/brain/Reads/The Mom Test (Rob Fitzpatrick)/3. Talking to customers is hard.md` and review the `## Pre-read brief` section against this checklist:

```
- [ ] One-liner is in Fitzpatrick's voice, paraphrasing his own thesis
- [ ] Opens with 1-2 paragraphs of flowing author-voice prose (not italicized placeholder text)
- [ ] Watch For has 3-5 bullets, each anchored to a specific phrase or metaphor from ch 3 text (e.g., "bulldozer", "toothbrush", "Habit", "textbook and checkbook")
- [ ] Key Terms are in Fitzpatrick's working vocabulary, 1-2 sentence definitions
- [ ] Questions to Hold are open philosophical questions with `- [ ]` checkboxes (not personal-action questions)
- [ ] Per-lens angles has three separate paragraphs, each 3-5 sentences, directly addressed to PM / CEO / Entrepreneur
- [ ] No em-dash pileups, no clipped labels, no generic MBA platitudes
- [ ] Contains inline wikilinks to other chapters if Fitzpatrick's text references them explicitly
```

- [ ] **Step 3: Record findings**

If any checkbox fails, note the specific shortfall in a new file at `/Users/mehmetsemihbabacan/.claude-shared/skills/reading-lens/docs/plans/2026-04-23-validation-notes.md` (create if not present). The findings drive follow-up refinement, not immediate fixes — this is a calibration check.

- [ ] **Step 4: No commit for this task**

Regenerated chapter files live in the user's vault, not the skill repo. No skill-repo commit.

---

## Task 11: Validation — re-run `/reading-lens:synthesize 3` on The Mom Test

**Files:**
- Regenerates the `## Post-read synthesis` section of: `/Users/mehmetsemihbabacan/dev/brain/Reads/The Mom Test (Rob Fitzpatrick)/3. Talking to customers is hard.md`

**Rationale:** Validates the post-read template against the reference quality bar.

- [ ] **Step 1: Invoke the skill**

```
/reading-lens:synthesize 3
```

Since `synthesis_has_notes: false` and there are no reader notes, the skill runs the standard overwrite flow (not the notes-aware upgrade).

- [ ] **Step 2: Review the regenerated Post-read synthesis section against this checklist**

```
- [ ] Core idea one-liner is in Fitzpatrick's voice
- [ ] Opens with 1-2 paragraphs of author-voice reflection (not a book-review summary)
- [ ] Key takeaways are 4-6 substantial bullets (1-2 sentences each)
- [ ] Final Key takeaway names the mental model the chapter builds
- [ ] Per-lens takeaways has three separate 3-5 sentence paragraphs with Monday-morning specificity
- [ ] Contrarian Take has the explicit voice-break pattern (critic speaks, then author concedes)
- [ ] Actionable experiments are 2-3 concrete bullets, scaled to a small team
- [ ] Connections has 3-5 links in author voice (not dry "see also")
- [ ] Flashcards has 3-5 Q/A pairs under 30 words each
- [ ] No em-dash pileups, no collapsed per-lens lines, no generic contrarian hedging
```

- [ ] **Step 3: Record findings**

Append to `/Users/mehmetsemihbabacan/.claude-shared/skills/reading-lens/docs/plans/2026-04-23-validation-notes.md`.

- [ ] **Step 4: No commit**

---

## Task 12: Validation — parallel-dispatch setup on a short book

**Files:**
- Regenerates: a book folder under `/Users/mehmetsemihbabacan/dev/brain/Reads/` for a test EPUB (or the user's choice of short EPUB).

**Rationale:** Spec §12 calls for a ≥3× speedup vs. serial. This task times setup against the new parallel workflow.

- [ ] **Step 1: Prepare a short test EPUB**

Locate an existing EPUB with ≤15 chapters, or use a public-domain short book (e.g., a free Project Gutenberg EPUB). Place at a known path, e.g., `/tmp/test-book.epub`.

If no suitable test EPUB is available, skip to Task 13 and note this as deferred.

- [ ] **Step 2: Time the setup**

```bash
time /reading-lens:setup /tmp/test-book.epub
```

Record elapsed wall-clock time in `2026-04-23-validation-notes.md`.

- [ ] **Step 3: Compare against expected**

Expected: for a 10–15 chapter book, total setup time under 10 minutes with parallel dispatch, versus ~30+ minutes serial. Exact target depends on chapter size. If the measured time is more than 2× the expected, investigate subagent dispatch fan-out and document in validation notes.

- [ ] **Step 4: No commit**

---

## Task 13: Validation — Turkish language override smoke test

**Files:**
- Regenerates: a book folder under `/Users/mehmetsemihbabacan/dev/brain/Reads/` for a test EPUB, in Turkish.

**Rationale:** Spec §9 language support needs validation.

- [ ] **Step 1: Invoke setup with Turkish directive**

In a Claude Code session:

```
/reading-lens:setup /tmp/test-book.epub

do it in Turkish
```

- [ ] **Step 2: Verify `0. General.md` frontmatter**

Open the new book's `0. General.md`. Confirm the YAML frontmatter contains `language: tr`.

- [ ] **Step 3: Verify a chapter's content is in Turkish**

Open any chapter file (e.g., chapter 1). Confirm:
- The pre-read brief is in Turkish
- The post-read synthesis is in Turkish
- The author's voice register is preserved (not generic Turkish — specific turns of phrase the author would use)

- [ ] **Step 4: Verify per-command consistency**

Invoke `/reading-lens:brief 2` on the same book. Verify the regenerated content stays in Turkish without the user re-specifying.

- [ ] **Step 5: Record findings**

Append to validation notes. Any shortfall (e.g., mixed-language output, dropped register) is a defect to be addressed in a follow-up plan.

- [ ] **Step 6: No commit**

---

## Self-Review

After writing the plan, I ran a self-review against the spec:

**Spec coverage check:**
- §4 (Writing voice) → Task 1 ✓
- §5 (Pre-read brief structure) → Task 3 ✓
- §6 (Post-read synthesis structure) → Task 4 ✓
- §7 (Close-reading extraction discipline) → Task 2 ✓
- §8 (Execution model) → Task 5 ✓
- §9 (Language support) → Task 6 ✓
- §10 (Linking mechanism) → covered inside Tasks 3 and 4 (inline wikilinks rule in Pre-read Brief flexibility; author-voiced Connections + mental-model naming in Post-read Synthesis) ✓
- §11 (Migration / SKILL.md sections to modify) → Tasks 1–7 cover each bullet ✓
- §12 (Testing/validation) → Tasks 10–13 ✓
- §13 (Deferred) → intentionally not implemented ✓

**Placeholder scan:** no "TBD", "TODO", or "implement later" strings. Every task has exact content. ✓

**Type/name consistency:** the templates in Tasks 3 and 4 both reference the close-reading extraction step numbers defined in Task 2 (thesis, anchor phrases, defined terms, voice register, structural role). The per-lens angles use `{Role 1} / {Role 2} / {Role N}` placeholder notation consistently with the Book Overview frontmatter in Task 6. ✓

**Scope check:** single-skill single-file edit plus a sync push. Appropriately scoped for one plan. ✓

---

## Execution choice

Plan complete.

**Two execution options:**

**1. Subagent-Driven (recommended)** — dispatch a fresh subagent per task, review between tasks, fast iteration. Uses `superpowers:subagent-driven-development`.

**2. Inline Execution** — execute tasks in this session using `superpowers:executing-plans`, batch execution with checkpoints.

Which approach?
