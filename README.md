# CodingAgents

A hands-on lab that teaches undergraduate and master's students the two
skills employers now expect of every new software engineer:

1. **Writing software with an AI coding agent**: specifying, planning,
   delegating, verifying, reviewing and owning the work, rather than
   accepting whatever the agent produces.
2. **Writing software that calls a frontier AI model** through its API:
   keeping the model's role narrow, validating what it returns, defending
   against prompt injection, and measuring quality with a proper evaluation.

The lab is self-contained and self-explanatory, so that students can work
through it alone and return to it after they graduate.

## Choose your track

Both tracks use the same codebase, the same exercises and the same marking
rubric. Pick the one that matches the coding agent you can use.

| | [GitHub Copilot track](github-copilot/) | [Claude Code track](claude-code/) |
|---|---|---|
| **Coding agent** | GitHub Copilot in VS Code | Claude Code in VS Code |
| **Cost to you** | Free for verified students (GitHub Student Developer Pack) | Paid: from USD 20 per month (see [costs](claude-code/COSTS_AND_ACCESS.md)) |
| **Usage** | Limited monthly AI credits; model chosen automatically | Plan usage limits; you can choose the model |
| **Who should choose it** | **Most students** | Students who already have, or choose to buy, Claude access |
| **Start here** | [github-copilot/LAB_INSTRUCTIONS.md](github-copilot/LAB_INSTRUCTIONS.md) | [claude-code/LAB_INSTRUCTIONS.md](claude-code/LAB_INSTRUCTIONS.md) |

**Not sure? Choose the GitHub Copilot track.** The tool you choose does not
affect your mark.

In Part D, your program calls a model API. That choice is separate from the
coding agent: the free **Google Gemini API** (age 18 and over) works on both
tracks, and the paid **Anthropic Claude API** is an option on both. An
offline mode is included for students who cannot use either.

Before you begin, read **[AGENT_FILES_GUIDE.md](AGENT_FILES_GUIDE.md)**. It
explains how coding agents work, the workflow you will follow, the key
configuration files for both tools, and whether those files are public.

## What you will practise

| Part | Steps | Skills |
|------|-------|--------|
| A. Foundations | 0 to 2 | Setup, safe permissions, how an agent works, the key files |
| B. Core workflow | 3 to 10 | Exploring and verifying, project instructions, test-first bug fixing, specification, planning, change review, context management, catching agent errors |
| C. Making the agent yours | 11 to 14 | Skills (`SKILL.md`), a read-only reviewer subagent, safety, data protection, cost, public versus private files, disclosure |
| D. Building with a frontier model | 15 to 25 | Model APIs, keys and secrets, a first network call, the adapter pattern, specifying an AI feature, evaluation sets and error analysis, prompt injection, failure handling, personal data, cost |
| Master's extensions | M1 to M6 | Specification ambiguity, a controlled comparison, skill evaluation, critical essay, model comparison, structured output |

Plan for about five lab sessions. The instructions mark safe stopping points
and explain how to pause and resume.

## Repository layout

```
AGENT_FILES_GUIDE.md   how agents and model APIs work, and the files that control them
github-copilot/        complete lab for GitHub Copilot (free for students)
claude-code/           complete lab for Claude Code (paid)
```

Each track folder is self-contained: open **only that folder** in VS Code.

## Requirements

- Python 3.10 or newer, Git, VS Code
- One coding agent: GitHub Copilot (free with the GitHub Student Developer
  Pack) or Claude Code (a paid Claude plan)
- For Part D: a free Google AI Studio account (age 18 and over), or a Claude
  Console account with credit, or the offline mode

## Licence

GNU General Public License v3.0. See [LICENSE](LICENSE).
