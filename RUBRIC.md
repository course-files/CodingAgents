# Marking rubric

The lab is marked out of **100** for undergraduates. Master's students are
marked out of **100** on a different weighting that includes the extensions.

The marking rewards **evidence of judgement**, not the amount of code the
agent produced. A student who catches and records an agent's mistake earns
more than one whose log claims that everything worked first time.

## Criteria

| # | Criterion | Evidence | UG weight | Master's weight |
|---|-----------|----------|:---------:|:---------------:|
| C1 | Bug fix done test-first (Step 5) | Failing test committed **before** the fix; hand calculation in log; tests unchanged by the fix | 15 | 10 |
| C2 | Specification quality (Step 6) | `docs/TASK_SPEC.md` complete, testable, with hand-worked examples and resolved open questions | 15 | 10 |
| C3 | Plan and review (Steps 7 and 8) | At least one plan change and one rejected or revised edit, each with a reason; small commits | 15 | 10 |
| C4 | Defect review (Step 9) | Number and accuracy of defects in `docs/REVIEW_currency.md`; comparison with the agent's review | 15 | 10 |
| C5 | Agent configuration (Steps 4, 10, 11) | Concise, accurate `CLAUDE.md`; improved skill and subagent; evidence they were tested | 15 | 10 |
| C6 | AI use log and reflection (Steps 3, 12, 13) | Honest, specific entries; verified claims from Step 3; thoughtful answers on safety and disclosure | 15 | 10 |
| C7 | Oral check (in class, 5 minutes) | Explains a randomly chosen part of their submission **without** the agent | 10 | 10 |
| M1–M4 | Master's extensions | See below | – | 30 |
| | **Total** | | **100** | **100** |

## Performance levels (apply to each criterion)

| Level | Share of criterion marks | Description |
|-------|:------------------------:|-------------|
| Excellent | 85–100% | Complete, precise and verified. Shows independent judgement: disagrees with the agent where it is wrong and explains why. |
| Good | 70–84% | Complete and mostly precise. Minor gaps in verification or reasoning. |
| Satisfactory | 50–69% | Required artefacts present, but checks are shallow or reasons generic ("it looked fine"). |
| Weak | 1–49% | Incomplete, or evidence that agent output was accepted without review. |
| Missing | 0% | Not submitted. |

## Specific guidance for markers

- **C1:** use `git log` to confirm the failing test commit precedes the fix.
  A fix that edits the provided tests scores at most "Weak".
- **C4:** an undergraduate who correctly identifies five defects with sound
  reasoning reaches "Good"; seven or more with fixes reaches "Excellent".
  Master's students are expected to identify all defects and classify them
  (correctness, reliability, security, testing).
- **C6:** a log that records no problems at all, across every step, should be
  treated with caution and probed in the oral check.
- **C7:** choose a line or function in the student's new feature and ask:
  "What does this do, why is it here, and what would break if it were
  removed?" A student who cannot answer cannot score above "Satisfactory"
  on C7, and the marker should review C3 and C5 again.

## Master's extensions (30 marks)

| Extension | Marks | Excellent work |
|-----------|:-----:|----------------|
| M1 Rounding ambiguity | 6 | Locates the cent precisely, proposes a defensible rule, pins it with a test, and discusses who should decide |
| M2 Controlled comparison | 8 | Clean data from both branches; honest discussion of validity threats; sensible design for a stronger study |
| M3 Skill evaluation | 6 | Ten well-chosen prompts, confusion matrix before and after revision, sound conclusion about automatic invocation |
| M4 Critical essay | 10 | Clear position, evidence from the lab, at least three credible sources, and a fair treatment of the strongest counter-argument |
