# GitHub Copilot track (free for students)

This folder contains the complete lab for students using **GitHub Copilot** in
VS Code. Verified students can use Copilot free of charge through the
**GitHub Student Developer Pack** (the Copilot Student plan).

> **Apply at least a week before the lab.** Student verification and
> activation can take several days. See Step 1.1 of the instructions.

## Start here

1. Apply for and activate Copilot Student:
   <https://github.com/settings/education/benefits>
2. Follow **[LAB_INSTRUCTIONS.md](LAB_INSTRUCTIONS.md)** step by step.
3. Check how you will be marked in [RUBRIC.md](RUBRIC.md).

In VS Code, open **this folder** (`github-copilot/`), not the repository root.

## What "free" means here

The Copilot Student plan includes unlimited code completions and a **limited
monthly allowance of AI credits** for chat and agent work, with the model
chosen automatically. Agent tasks use credits faster than simple questions.
Step 1.4 explains how to make the allowance last. **Do not buy credits for
this lab**; if you run out, tell your lecturer.

## Part D: calling a model from your own code

In Part D your program calls a frontier AI model through its API. Use the
free **Google Gemini API** (age 18 and over), or the paid **Anthropic Claude
API**. This is separate from your coding agent, and Gemini calls do not use your Copilot credits.

## Files you will create

| File | Purpose | Step |
|------|---------|------|
| `.github/copilot-instructions.md` (or `AGENTS.md`) | Project instructions, loaded in every request | 4 |
| `.github/skills/add-tests/SKILL.md` | A skill, loaded when relevant or with `/add-tests` | 11 |
| `.github/agents/code-reviewer.agent.md` | A read-only reviewer agent | 12 |
| `.env` (never committed) | Your model API key and settings for Part D | 16 |
| `sales_toolkit/ai/order_parser.py` | The AI feature you build in Part D | 21 |
| `tests/test_order_parser.py` | Tests for the AI feature, using a fake model | 21 |
| `evals/` cases | Your evaluation and hold-out cases | 20 |
| `docs/` | Your AI use log, specifications, plan, reviews and evaluation report | throughout |

The general guide [../AGENT_FILES_GUIDE.md](../AGENT_FILES_GUIDE.md) explains
how agents work, what each file does, and whether these files are public.
