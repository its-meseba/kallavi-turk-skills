# meseba-skills

A personal library of [Claude Code](https://claude.com/claude-code) skills, commands, and rules, synced from my local setup.

This repo is **fully open source under MIT** — clone any skill, adapt it to your workflow, ship your own thing. If something here helps you, a `@its-meseba` tag or star is appreciated, but not required.

---

## What's in here

| Folder | Purpose |
|---|---|
| [`skills/`](skills/) | Agent Skills — self-contained instruction bundles loaded into Claude Code on demand |
| [`commands/`](commands/) | Slash-command sub-skills (e.g. `/daily-brain:log`, `/intel:gather`) |
| [`rules/`](rules/) | Global rules loaded into every session (coding style, git workflow, etc.) |
| [`shipyard-lessons/`](shipyard-lessons/) | Lesson library consumed by the `shipyard` skill |

### Skills currently in the repo

```
skills/
├── app-growth-pipeline           # Promote subscription mobile apps on TikTok/IG
├── daily-brain                   # Second-brain logging into Obsidian
├── frame-forge                   # Automated story-chain images for reels
├── image-gen                     # Batch image generation (Gemini / Replicate)
├── intel                         # Competitive-intelligence dossier builder
├── ios-monetization-expert       # Indie iOS monetization advisor
├── linkedin-newsletter-generation # Long-form LinkedIn post generator
├── little-paws                   # Illustrated children's-story generator
├── mini-decade                   # Decade-scale mastery tracking in Obsidian
├── no-brainer                    # Executive summary generator
├── obsidian-cli                  # Obsidian vault operations via CLI
├── obsidian-markdown             # Obsidian-flavored markdown helpers
├── qgit                          # One-shot `git add + commit + push`
├── reading-lens                  # Active-reading scaffolding for nonfiction EPUBs
├── replicate                     # Replicate API model runner
├── ship-wreck-check              # Brutal final-quality review
├── shipyard                      # Mobile app dev automation
├── skill-creator                 # Skill authoring / editing toolkit
└── spending-tracker              # Personal spending tracker
```

Each skill is self-contained — it has its own `SKILL.md` with YAML frontmatter, plus optional `scripts/`, `references/`, and `assets/`.

---

## Install a skill in Claude Code

Claude Code loads skills from `~/.claude/skills/` (or any other `.claude/skills/` folder in scope). Two install paths:

### Option A — Clone the whole repo (fastest)

```bash
# Clone into your user-scope skills folder
git clone https://github.com/its-meseba/meseba-skills.git ~/.claude/meseba-skills

# Symlink the skills you want into Claude Code's skills path
mkdir -p ~/.claude/skills
ln -s ~/.claude/meseba-skills/skills/reading-lens ~/.claude/skills/reading-lens
ln -s ~/.claude/meseba-skills/skills/daily-brain  ~/.claude/skills/daily-brain
# …repeat for each skill you want
```

Pull updates later with `git -C ~/.claude/meseba-skills pull`.

### Option B — Copy a single skill

If you only want one, copy just that folder:

```bash
# One-shot single-skill install
git clone --depth 1 https://github.com/its-meseba/meseba-skills.git /tmp/meseba-skills
cp -r /tmp/meseba-skills/skills/reading-lens ~/.claude/skills/
rm -rf /tmp/meseba-skills
```

### Option C — Project-scope (shared with your team)

To make a skill available inside one project repo (and check it into version control):

```bash
mkdir -p <your-project>/.claude/skills
cp -r /path/to/meseba-skills/skills/reading-lens <your-project>/.claude/skills/
git -C <your-project> add .claude/skills
```

### Verify the install

Restart Claude Code, then in any session:

```
/help
```

Your installed skill should appear in the available-skills list, triggerable by its description or by `/<skill-name>`.

---

## Slash commands

Skills in [`commands/`](commands/) expose sub-commands, e.g.:

```
/daily-brain:log       # quick structured entry into today's daily note
/intel:gather          # deep-research dossier on a tracked entity
/mini-decade:progress  # cross-field mastery dashboard
/shipyard:learn-lessons
```

Install the same way — clone `commands/<name>/` into `~/.claude/commands/<name>/`.

---

## Global rules

The [`rules/`](rules/) folder contains short guidance files (coding style, git workflow, testing, security, etc.) that I load into every session via `@path/to/rule.md` references inside `CLAUDE.md`.

To reuse: copy [`rules/`](rules/) to `~/.claude/rules/` and reference the files from your own `CLAUDE.md`.

---

## Compatibility

These skills are authored for **Claude Code** (CLI + IDE). The Agent Skills format is an [open standard](https://docs.anthropic.com/en/docs/agents/agent-skills), so most skills also work in:

- **Claude.ai** — paste `SKILL.md` as a custom instruction
- **Claude API** — use the Skills feature on the Messages API
- **Other Agent Skills-compatible runtimes**

Skills with platform-specific side-effects (e.g. Obsidian vault paths, Replicate API keys) need the matching tool or env var set.

---

## Contributing

PRs welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). New skill? Open a PR with a `SKILL.md`, short description, and a usage example. Fix in an existing skill? Send a patch.

---

## License

MIT — see [LICENSE](LICENSE). Use these skills freely, commercially or personally. No permission needed. If any of this genuinely helps your work, a `@its-meseba` tag is a kind gesture, not a requirement.

---

## Author

**Semih Babacan** — [@its-meseba](https://github.com/its-meseba)
