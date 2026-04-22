# Contributing to meseba-skills

Thanks for considering a contribution. This is a personal skills library that I open source because it might help others build their own — PRs that sharpen existing skills or add well-scoped new ones are welcome.

## Philosophy

All skills here follow the [Anthropic Agent Skills](https://docs.anthropic.com/en/docs/agents/agent-skills) open standard so they work across Claude Code, Claude.ai, and the Claude API. Skills should be:

- **Actionable** — clear step-by-step instructions an agent can follow
- **Self-contained** — a `SKILL.md` plus optional `scripts/`, `references/`, and `assets/`
- **Standards-compliant** — follow the Agent Skills frontmatter spec
- **Tested** — validated against real user queries before submission

## Add a new skill

### 1. Fork and branch

```bash
# Fork its-meseba/meseba-skills on GitHub, then:
git clone https://github.com/YOUR-USERNAME/meseba-skills.git
cd meseba-skills
git checkout -b add-skill-<your-skill-name>
```

### 2. Create the skill folder

```bash
mkdir skills/your-skill-name
```

**Folder naming:**
- kebab-case, lowercase, no spaces
- descriptive and concise (2–4 words)
- must match the `name:` field in the SKILL.md frontmatter
- must NOT start with `claude` or `anthropic`

### 3. Write `SKILL.md`

Every skill must have a `SKILL.md` file (exact casing) with YAML frontmatter followed by instructions:

```yaml
---
name: your-skill-name
description: What this skill does and when to trigger it. Include trigger phrases users are likely to say. Keep under 1024 characters, no XML tags.
metadata:
  author: your-github-username
  version: 1.0.0
  tags:
    - tag-1
    - tag-2
---
```

**Frontmatter rules:**
- `name` matches folder name exactly (kebab-case)
- `description` covers both WHAT the skill does and WHEN it should trigger
- `description` is under 1024 chars and contains no `<` / `>` / XML
- `name` does not start with `claude` or `anthropic`

**Body content should include:**
1. **Overview** — what the skill does, why it exists
2. **Prerequisites** — required tools, API keys, env vars
3. **Workflow** — numbered, specific steps
4. **Example queries** — 3–5 user queries with expected behavior
5. **Error handling** — common failure modes and recovery

Write for specificity. "Call API endpoint `/v1/stocks/{ticker}`" beats "get the data." Avoid vague verbs like "validate properly."

### 4. Optional subdirectories

```
skills/your-skill-name/
├── SKILL.md          # Required
├── scripts/          # Optional: executable code
├── references/       # Optional: detailed docs, API guides
└── assets/           # Optional: templates, configs, sample data
```

**Do NOT** place a `README.md` inside the skill folder. Use `SKILL.md` as the single entry point.

### 5. Test locally in Claude Code

```bash
# Symlink into your user-scope skills dir
ln -s $(pwd)/skills/your-skill-name ~/.claude/skills/your-skill-name
```

Restart Claude Code and test with at least 3 different user queries, including edge cases and at least one failure mode.

### 6. Validation checklist

Before submitting:

- [ ] File is exactly named `SKILL.md` (case-sensitive)
- [ ] Folder is kebab-case and matches the frontmatter `name`
- [ ] Frontmatter has `---` delimiters at start and end
- [ ] `name` and `description` are present and valid
- [ ] Description covers WHAT and WHEN
- [ ] Description is under 1024 chars with no XML tags
- [ ] `name` doesn't start with `claude` or `anthropic`
- [ ] Instructions are specific and actionable
- [ ] 3+ example queries documented
- [ ] Error handling is present
- [ ] No `README.md` inside the skill folder
- [ ] Tested against 3+ real user queries

### 7. Open the PR

```bash
git add skills/your-skill-name/
git commit -m "Add <your-skill-name>: <short description>"
git push origin add-skill-<your-skill-name>
```

Then open a pull request against `its-meseba/meseba-skills` with:
- What the skill does
- How you tested it
- Any external dependencies (API keys, tools, MCP servers)

## Standards at a glance

### Required structure

```
skills/your-skill-name/
├── SKILL.md          # Required
├── scripts/          # Optional
├── references/       # Optional
└── assets/           # Optional
```

### Frontmatter

```yaml
---
name: skill-name              # kebab-case, matches folder name
description: What and when    # < 1024 chars, no XML tags
metadata:
  author: github-username
  version: 1.0.0
  tags: [tag1, tag2]
---
```

### Instruction quality bar

- **Specific** — concrete commands, file paths, API endpoints
- **Numbered** — workflows as ordered lists
- **Exemplified** — 3+ user query examples with expected behaviors
- **Defensive** — explicit error handling and recovery steps

## Style

### Markdown

- Standard CommonMark
- Clear H2/H3 sectioning
- Code blocks with language tags (` ```python `, ` ```bash `, ` ```yaml `)
- Numbered lists for workflows, bullets for requirements

### Code in `scripts/`

- **Python** — PEP 8, type hints, docstrings
- **Bash** — `#!/bin/bash`, `set -e`, comments at choice points
- **Node/JS** — standard JS conventions, ESLint-compatible

## Code of conduct

Be respectful, constructive, and focused on the work. Harassment or discrimination isn't tolerated — report concerns via a GitHub issue.

## Review process

PRs are reviewed against:
- Agent Skills standard compliance
- Clarity of instructions
- Error handling
- Evidence of testing
- Code quality in any `scripts/`

Expect a 1–3 day review cycle on most PRs.

## Resources

- **Agent Skills docs** — https://docs.anthropic.com/en/docs/agents/agent-skills
- **Claude Code** — https://claude.com/claude-code
- **This repo** — https://github.com/its-meseba/meseba-skills

## License

By contributing, you agree your contributions will be released under the MIT License (same as the repo).

---

Thanks — and if something here leads you to build your own skills library, tag `@its-meseba` so I can see what you made.
