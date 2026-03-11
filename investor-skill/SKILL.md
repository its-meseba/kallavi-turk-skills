---
name: investor-skill
description: Multi-agent investment advisor system. Use when the user asks to analyze their investment portfolio, update market data, generate financial guidance reports, or asks ad-hoc investment questions based on their portfolio.
---

# Investment Advisor Multi-Agent System Skill

This skill allows Claude to operate the Investment Advisor Multi-Agent System, enabling personalized financial advisory, portfolio management, and interactive inference.

## Phase 1: Setup & Validation

Before executing any workflows, ensure the environment is correctly set up:

1.  **Environment Variables:** Verify that a `.env` file exists with the necessary parameters (e.g., Gemini API keys, SMTP credentials).
2.  **Portfolio Security:** **NEVER** push the user's actual portfolio (`scripts/portfolio/current_portfolio.json`) to version control. The portfolio is secret.
3.  **Temporary Portfolio:** If a portfolio does not exist, you MUST instruct the user to use the interactive tool `python scripts/manage_portfolio.py` to create or populate their `scripts/portfolio/current_portfolio.json` before running the analysis. This file acts as a temporary document locally.

## Phase 2: Workflows

### Periodicity (Scheduled Runs)
This skill should be run **periodically every 72 hours** to generate fresh advice.
If the system supports scheduled background execution, configure it to trigger the "Full Analysis Pipeline" every 72 hours automatically.

Use the following commands to fulfill user requests based on their intent:

### 1. Portfolio Setup and Management

When the user wants to add/remove assets, view changes, or initialize their portfolio:

```bash
python scripts/manage_portfolio.py
```
This launches an interactive CLI. Guide the user to use this tool to manage their assets securely.

### 2. Full Analysis Pipeline

When the user asks for comprehensive market research and portfolio advice (runs the full pipeline of Research -> Discussion -> Decider):

```bash
python scripts/main.py
```

### 3. Ad-hoc Inference

When the user asks specific financial questions about their portfolio or the market:

```bash
python scripts/inference.py --question "YOUR_QUESTION_HERE"
```
Replace `YOUR_QUESTION_HERE` with the user's actual specific question.

## Reference Management

For deeper technical understanding of the system's architecture, file structure, or advanced CLI arguments, consult the following local files:

-   [`README.md`](../README.md): Contains system architecture, setup instructions, and CLI usage.
-   [`app_state.txt`](references/app_state.txt): Contains the project state report, including agent taxonomy and data flow.
-   [`Investment Analyst App Definition.txt`](references/Investment Analyst App Definition.txt): Original requirement specifications.
-   [`Investment Analyst App Structure.txt`](references/Investment Analyst App Structure.txt): Additional design definitions.
