# Reviewing an agent's change

Use this checklist every time you accept a change from a coding agent.
If you cannot tick an item, do not accept the change yet.

## Understand it
- [ ] I can explain, in my own words, what every changed line does.
- [ ] I know why each file was touched. No file changed that should not have.
- [ ] The change does what the specification asked, and nothing extra.

## Verify it
- [ ] I ran the tests myself and saw them pass (not only the agent's report).
- [ ] At least one expected value in the tests was worked out by hand.
- [ ] No existing test was weakened, skipped or deleted.
- [ ] I tried one input the agent did not mention (an edge case).

## Check for common agent mistakes
- [ ] No invented functions, parameters or packages (check that each import exists).
- [ ] No silently swallowed errors (`except Exception: pass` or returning 0 / None).
- [ ] No hard-coded values presented as "current" or "live" data.
- [ ] Money uses `Decimal` and `money()`; no `float` or `round()`.
- [ ] No secrets, tokens or personal data in code, logs or prompts.
- [ ] Tests do not compute their expected value with the code under test.

## Record it
- [ ] I wrote an entry in docs/AI_USE_LOG.md.
- [ ] The commit message explains what changed and why.
