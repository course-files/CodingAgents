# CodingAgents

A standalone, hands-on lab that teaches undergraduate and master's students
to **code correctly with AI coding agents**: to specify, plan, delegate,
verify, review and own the work, rather than accept whatever an agent
produces.

The lab uses [Claude Code](https://code.claude.com/docs/en/vscode-extension)
in VS Code and a small Python invoicing codebase (`sales_toolkit`) with a
real bug, a vague feature request, and an "agent-written" file full of
plausible defects.

## Start here

👉 **[LAB_INSTRUCTIONS.md](LAB_INSTRUCTIONS.md)** (step-by-step)
👉 **[RUBRIC.md](RUBRIC.md)** (how the work is marked)

## What students practise

| Part | Steps | Skills |
|------|-------|--------|
| A. Foundations | 0–2 | Setup, safe permission mode, how an agent works |
| B. Core workflow | 3–9 | Explore, project memory (`CLAUDE.md`), test-first bug fixing, specification, planning, change review, catching agent errors |
| C. Making the agent yours | 10–13 | Skills (`SKILL.md`), a read-only reviewer subagent, safety, data protection, disclosure |
| Master's extensions | M1–M4 | Specification ambiguity, a controlled comparison, skill evaluation, critical essay |

## Requirements

- Python 3.10 or newer, Git, VS Code
- A Claude account that includes Claude Code (a paid Claude subscription or a Claude Console account)

Check your machine with:

```bash
python -m pip install -r requirements.txt
python check_setup.py
python -m pytest -q
```

## Repository layout

```
sales_toolkit/                  practice codebase
tests/                          starter tests (all pass; that does not mean the code is correct)
data/sample_sales.csv           sample data
exercises/review_agent_output/  agent-style code to review in Step 9 (do not use it)
templates/                      CLAUDE.md, SKILL.md, subagent, specification, log and checklist templates
```

## Licence

GNU General Public License v3.0. See [LICENSE](LICENSE).
