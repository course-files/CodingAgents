# Claude Code track

This folder contains the complete lab for students using **Claude Code** in
VS Code.

> **Claude Code is a paid tool.** Read **[COSTS_AND_ACCESS.md](COSTS_AND_ACCESS.md)**
> before you start. If you do not have access, use the free
> **[GitHub Copilot track](../github-copilot/)** instead; it is marked the same way.

## Start here

1. Read [COSTS_AND_ACCESS.md](COSTS_AND_ACCESS.md).
2. Follow **[LAB_INSTRUCTIONS.md](LAB_INSTRUCTIONS.md)** step by step.
3. Check how you will be marked in [RUBRIC.md](RUBRIC.md).

In VS Code, open **this folder** (`claude-code/`), not the repository root.

## Part D: calling a model from your own code

In Part D your program calls a frontier AI model through its API. Use the
free **Google Gemini API** (age 18 and over), or the paid **Anthropic Claude
API**. This is separate from your coding agent. A Claude Pro subscription covers Claude Code but **not** API usage; see [COSTS_AND_ACCESS.md](COSTS_AND_ACCESS.md).

## Files you will create

| File | Purpose | Step |
|------|---------|------|
| `CLAUDE.md` | Project instructions, loaded in every session | 4 |
| `.claude/skills/add-tests/SKILL.md` | A skill, loaded when relevant or with `/add-tests` | 11 |
| `.claude/agents/code-reviewer.md` | A read-only reviewer subagent | 12 |
| `.env` (never committed) | Your model API key and settings for Part D | 16 |
| `sales_toolkit/ai/order_parser.py` | The AI feature you build in Part D | 21 |
| `tests/test_order_parser.py` | Tests for the AI feature, using a fake model | 21 |
| `evals/` cases | Your evaluation and hold-out cases | 20 |
| `docs/` | Your AI use log, specifications, plan, reviews and evaluation report | throughout |

The general guide [../AGENT_FILES_GUIDE.md](../AGENT_FILES_GUIDE.md) explains
how agents work, what each file does, and whether these files are public.
