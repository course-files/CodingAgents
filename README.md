# CodingAgents

A standalone, hands-on lab that teaches undergraduate and master's students
to **code correctly and responsibly with AI coding agents**: to specify, plan,
delegate, verify, review and own the work, rather than accept whatever an
agent produces.

## Choose your track

Both tracks use the same codebase, the same exercises and the same marking
rubric. Pick the one that matches the tool you can use.

| | [GitHub Copilot track](github-copilot/) | [Claude Code track](claude-code/) |
|---|---|---|
| **Cost to you** | Free for verified students (GitHub Student Developer Pack) | Paid: from USD 20 per month (see [costs](claude-code/COSTS_AND_ACCESS.md)) |
| **Usage** | Limited monthly AI credits; model chosen automatically | Plan usage limits; you can choose the model |
| **Who should choose it** | **Most students** | Students who already have, or choose to buy, Claude access |
| **Start here** | [github-copilot/LAB_INSTRUCTIONS.md](github-copilot/LAB_INSTRUCTIONS.md) | [claude-code/LAB_INSTRUCTIONS.md](claude-code/LAB_INSTRUCTIONS.md) |

**Not sure? Choose the GitHub Copilot track.** The tool you choose does not
affect your mark.

Before you begin, read **[AGENT_FILES_GUIDE.md](AGENT_FILES_GUIDE.md)**. It
explains how coding agents work, the workflow you will follow, the key
configuration files for both tools, and whether those files are public.

## What you will practise

| Part | Steps | Skills |
|------|-------|--------|
| A. Foundations | 0–2 | Setup, safe permissions, how an agent works, the key files |
| B. Core workflow | 3–10 | Exploring and verifying, project instructions, test-first bug fixing, specification, planning, change review, context management, catching agent errors |
| C. Making the agent yours | 11–14 | Skills (`SKILL.md`), a read-only reviewer subagent, safety, data protection, cost, public versus private files, disclosure |
| Master's extensions | M1–M4 | Specification ambiguity, a controlled comparison, skill evaluation, critical essay |

## Repository layout

```
AGENT_FILES_GUIDE.md   how agents work and the files that control them (both tracks)
github-copilot/        complete lab for GitHub Copilot (free for students)
claude-code/           complete lab for Claude Code (paid)
```

Each track folder is self-contained: open **only that folder** in VS Code.

## Requirements

- Python 3.10 or newer, Git, VS Code
- One of: GitHub Copilot (free with the GitHub Student Developer Pack), or a
  Claude account that includes Claude Code

## Licence

GNU General Public License v3.0. See [LICENSE](LICENSE).
