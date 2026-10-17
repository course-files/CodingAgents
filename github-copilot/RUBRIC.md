# Marking rubric

This rubric is identical for the Claude Code and GitHub Copilot tracks, and
for the free and paid model APIs. The tools a student chose do not affect
the mark.

The marking rewards **evidence of judgement**, not the amount of code the
agent or the model produced. A student who catches and records a mistake
earns more than one whose log claims that everything worked first time.

## Criteria

| # | Criterion | Evidence | UG weight | Master's weight |
|---|-----------|----------|:---------:|:---------------:|
| C1 | Bug fix done test-first (Step 5) | Failing test committed **before** the fix; hand calculation in log; tests unchanged by the fix | 10 | 7 |
| C2 | Specification quality (Step 6) | `docs/TASK_SPEC.md` complete, testable, with hand-worked examples and resolved open questions | 10 | 7 |
| C3 | Plan, review and context (Steps 7 to 9) | Committed plan with at least one requested change; at least one rejected or revised edit with a reason; feature branch and small commits; a sound personal rule for managing context | 10 | 7 |
| C4 | Defect review (Step 10) | Number and accuracy of defects in `docs/REVIEW_currency.md`; comparison with the agent's review | 10 | 7 |
| C5 | Agent configuration (Steps 4, 11, 12, 18) | Concise, accurate project instruction file including AI rules; improved skill and subagent; evidence they were tested | 10 | 7 |
| C6 | AI use log and reflections (Steps 2, 3, 13, 14, 25) | Honest, specific entries; verified claims; thoughtful answers on safety, cost, public versus private files, and disclosure | 10 | 7 |
| C7 | API integration and safety (Steps 16, 17, 21, 23, 24) | Key kept out of the repository and its history; model limited to identifying products and quantities; all model output validated; tests use a fake client; injection test with a compromised model; helpful failure messages | 15 | 10 |
| C8 | Evaluation and error analysis (Steps 19, 20, 22, 24) | Specification with a clear division of responsibility; at least eight hand-labelled cases and a hold-out set; one change per iteration; failures grouped by cause; honest hold-out result; cost estimate | 15 | 10 |
| C9 | Oral check (in class, 5 to 10 minutes) | Explains a randomly chosen part of their submission **without** the agent | 10 | 8 |
| M1 to M6 | Master's extensions | See below | not applicable | 30 |
| | **Total** | | **100** | **100** |

## Performance levels (apply to each criterion)

| Level | Share of criterion marks | Description |
|-------|:------------------------:|-------------|
| Excellent | 85 to 100% | Complete, precise and verified. Shows independent judgement: disagrees with the agent or the model where it is wrong and explains why. |
| Good | 70 to 84% | Complete and mostly precise. Minor gaps in verification or reasoning. |
| Satisfactory | 50 to 69% | Required artefacts present, but checks are shallow or reasons generic ("it looked fine"). |
| Weak | 1 to 49% | Incomplete, or evidence that agent or model output was accepted without review. |
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
- **C7:** an API key found anywhere in the repository or its history caps C7
  at "Weak", even if the key has since been revoked. Check that prices come
  from `data/catalogue.csv` and that a requested discount is never applied
  automatically.
- **C8:** do **not** mark the accuracy figure itself. Mark the process: were
  expected answers written by hand, was one thing changed at a time, were
  failures analysed by cause, and was the hold-out result reported honestly?
  A student who reports a lower hold-out score and explains it should score
  higher than one who reports a suspiciously perfect result without analysis.
- **Students without API access** (under 18, or unable to create an
  account) complete Part D with the offline `keyword` provider and the
  lecturer's demonstration. Mark C7 and C8 on the same process criteria; do
  not penalise the absence of live results.
- **C9:** choose a line or function in the student's work and ask: "What
  does this do, why is it here, and what would break if it were removed?"
  Good choices include a validation rule in `parse_order` or a rule in
  `SYSTEM_PROMPT`. A student who cannot answer cannot score above
  "Satisfactory" on C9, and the marker should review C3, C5 and C7 again.

## Master's extensions (30 marks)

| Extension | Marks | Excellent work |
|-----------|:-----:|----------------|
| M1 Rounding ambiguity | 4 | Locates the cent precisely, proposes a defensible rule, pins it with a test, and discusses who should decide |
| M2 Controlled comparison | 5 | Clean data from both branches; honest discussion of validity threats; sensible design for a stronger study |
| M3 Skill evaluation | 4 | Ten well-chosen prompts, confusion matrix before and after revision, sound conclusion about automatic invocation |
| M4 Critical essay | 7 | Clear position, evidence from the lab, at least three credible sources, and a fair treatment of the strongest counter-argument |
| M5 Model comparison | 5 | Repeated runs, variation reported, cost and latency compared, a recommendation whose confidence matches the sample size |
| M6 Structured output | 5 | Working optional mode, before and after measurements, and a reasoned view on provider lock-in |

## Note for the GitHub Copilot track

Students on the Copilot Student plan have a limited monthly allowance of AI
credits for the coding agent. A student who runs out of credits and records
this honestly in the log must not be penalised for agent steps they could
not complete, provided they completed every step that does not require the
agent (hand calculations, the failing test, the specification, the manual
defect review, the evaluation cases and Step 13). Calls to the Gemini API in
Part D do not use Copilot credits. Reported credit usage is useful evidence
for discussion, not a marking criterion.
