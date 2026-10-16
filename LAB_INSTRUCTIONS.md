# Lab: Coding Correctly with AI Agents

**Audience:** undergraduate and master's students
**Tool:** Claude Code (VS Code extension)
**Estimated time:** 4 to 5 hours (undergraduate core); add 3 to 4 hours for the master's extensions
**Submission:** your own repository (fork) containing your code, `CLAUDE.md`, `.claude/`, and the files in `docs/`

---

## Why this lab exists

Software teams now routinely delegate programming work to AI coding agents.
Employers increasingly expect graduates to arrive already able to work this
way. Being "AI native" does **not** mean typing a request and accepting
whatever comes back. It means you can:

1. **Specify** precisely what you want, including the cases that matter.
2. **Plan** with the agent before it changes anything.
3. **Delegate** well-scoped work.
4. **Verify** the result independently, with tests and your own reasoning.
5. **Review** the change as a professional reviewer would, and reject what is wrong.
6. **Own** the result: you are accountable for every line you commit, whoever typed it.

This lab practises each of those skills on a small, realistic codebase. You
will see the agent do impressive work, and you will also catch it being
wrong. Both experiences are the point.

> **The rule for the whole lab:** never accept a change you cannot explain.
> At assessment you may be asked to explain any line in your submission
> **without** the agent's help.

---

## Learning outcomes

By the end of this lab you should be able to:

- **LO1** Explain what a coding agent is, how its work loop operates, and where its errors come from.
- **LO2** Configure an agent for a project using `CLAUDE.md`, a skill (`SKILL.md`), and a subagent.
- **LO3** Write a task specification with testable acceptance criteria and use it to drive the agent.
- **LO4** Use plan-first and test-first workflows to keep the agent's work correct.
- **LO5** Review agent-generated code systematically and identify defects such as invented dependencies, silent failures and tautological tests.
- **LO6** Apply safe practice: permissions, secrets, personal data, and honest disclosure of AI use.
- **LO7 (master's)** Evaluate agent-assisted development critically, using evidence you collect yourself.

---

## Prerequisites (check honestly before you start)

You will supervise an agent, and you cannot supervise work you cannot read.
Before starting, you should be able to:

- [ ] Read a short Python function and say what it returns for a given input.
- [ ] Use Git from the terminal: `clone`, `status`, `add`, `commit`, `push`, `diff`.
- [ ] Run a test suite with `pytest` and read a failing test's output.
- [ ] Explain why `0.1 + 0.2 == 0.3` is `False` in Python. (Hint: look up floating point.)

If any box is unticked, spend 30 minutes on it first. The lab will still
"work" without these skills, but you will be accepting code you cannot judge,
which defeats its purpose.

---

## Repository map

```
.
├── LAB_INSTRUCTIONS.md        <- you are here
├── RUBRIC.md                  <- how your work is marked
├── check_setup.py             <- Step 0 setup check
├── sales_toolkit/             <- the practice codebase (Python)
│   ├── invoices.py
│   └── __main__.py            <- command-line interface
├── tests/test_invoices.py
├── data/sample_sales.csv
├── exercises/review_agent_output/currency.py   <- Step 9
└── templates/                 <- starting points you will copy and edit
    ├── AI_USE_LOG.md
    ├── TASK_SPEC.md
    ├── REVIEW_CHECKLIST.md
    ├── CLAUDE.md.template
    ├── SKILL.md.template
    └── code-reviewer.md.template
```

---

# Part A: Foundations

## Step 0: Get the code and set up your log (20 minutes)

1. **Fork** this repository to your own GitHub account, then clone your fork:

   ```bash
   git clone git@github.com:<your-username>/CodingAgents.git
   cd CodingAgents
   ```

2. Create a virtual environment and install the test tool:

   ```bash
   python -m venv .venv
   # Windows (PowerShell):  .venv\Scripts\Activate.ps1
   # Linux / macOS:          source .venv/bin/activate
   python -m pip install -r requirements.txt
   ```

3. Run the setup check, the tests, and the program:

   ```bash
   python check_setup.py
   python -m pytest -q
   python -m sales_toolkit invoice data/sample_sales.csv
   ```

   You should see `7 passed` and an invoice breakdown in KES.

4. Create your log and your documents folder:

   ```bash
   mkdir docs
   cp templates/AI_USE_LOG.md docs/AI_USE_LOG.md
   ```

   (On Windows PowerShell, `cp` and `mkdir` also work.)

5. **Before you use any AI**, read `sales_toolkit/invoices.py` yourself for
   ten minutes. Note in your log the four business rules and anything you do
   not understand. You will compare this with what the agent tells you in
   Step 3.

6. Commit: `git add docs && git commit -m "Start AI use log"`.

> **Windows users:** the repository includes a `.gitattributes` file that
> keeps Unix (LF) line endings. If Git warns about line endings, that is
> expected and harmless.

---

## Step 1: Install Claude Code and choose a safe mode (20 minutes)

1. You need VS Code and an account that includes Claude Code: a paid Claude
   subscription (Pro, Max, Team or Enterprise) or a Claude Console account.
   If you do not have access, speak to your lecturer **before** the lab.
2. In VS Code, open the Extensions view (`Ctrl+Shift+X` on Windows/Linux,
   `Cmd+Shift+X` on macOS), search for **Claude Code** (publisher:
   Anthropic), and click **Install**.
3. Open the `CodingAgents` folder in VS Code (**File → Open Folder**), then
   open any file. Click the **Spark icon** in the top-right of the editor to
   open the Claude panel, and sign in when prompted.
4. At the bottom of the prompt box is the **permission mode** indicator.
   Click it and select **Manual**. In Manual mode the agent must ask before
   editing files or running most commands, and it shows you each proposed
   edit as a side-by-side diff.

   **Use Manual mode for this entire lab unless a step says otherwise.**
   Faster modes exist; you will earn the right to use them by first learning
   to review every change.

5. Type `hello, what can you do in this folder?` and send it. Record in your
   log which model is shown at the bottom of the prompt box.

Official documentation: <https://code.claude.com/docs/en/vscode-extension>

---

## Step 2: Understand what you are working with (15 minutes, reading)

A **coding agent** is a language model connected to tools. It works in a loop:

```
 your request
      │
      ▼
 ┌─────────────┐   reads files, searches code,   ┌─────────────┐
 │    THINK    │ ─────────────────────────────▶  │     ACT     │
 │ (the model) │ ◀─────────────────────────────  │ (the tools) │
 └─────────────┘   sees results, test output,    └─────────────┘
      │            error messages
      ▼
 a result for you to review
```

Three consequences matter for everything that follows:

- **It is fluent, not infallible.** The model produces the most plausible
  continuation of its context. Plausible and correct usually coincide, but
  not always. Its mistakes look exactly as confident as its successes.
- **It only knows what is in its context.** It does not remember your last
  session unless you write things down (Step 4). It does not know your
  client's business rules unless you state them.
- **It optimises for what you ask.** Ask it to "make the tests pass" and it
  may edit the tests. Ask precisely, and state what must not change.

**Your role** is therefore not "prompt writer". You are the specifier,
supervisor, reviewer and owner. The workflow you will practise:

```
Explore ──▶ Specify ──▶ Plan ──▶ Test first ──▶ Implement ──▶ Review ──▶ Commit
   ▲                                                            │
   └──────────────────── reject and revise ◀────────────────────┘
```

Write two or three sentences in your log: in your own words, why can a
passing test suite still hide a wrong answer?

---

# Part B: The core workflow

## Step 3: Explore before you change anything (25 minutes)

Use the agent to understand the codebase, then check what it tells you.

1. Ask:

   ```
   Explain this project to me. What does sales_toolkit do, what are the
   business rules in invoices.py, and how are the tests organised?
   Do not change any files.
   ```

2. Ask a follow-up of your own about something you did not understand in Step 0.
3. **Verify three specific claims** the agent made, by reading the code or
   running it. For example, if it says "VAT is charged after the discount",
   find the exact line that does this.
4. In your log, record each of the three claims and whether it was **true,
   false, or partly true**, with the line number that proves it.

> **Hint (read only after trying):** compare what the docstring *says* about
> VAT with what `invoice_total` *does*. Did the agent notice the difference?
> Agents often summarise documentation instead of reading code closely.

---

## Step 4: Give the agent project memory with CLAUDE.md (25 minutes)

`CLAUDE.md` is a Markdown file in the project root that the agent reads at
the start of **every** session. It holds the standing rules you would
otherwise repeat in every request.

1. In the Claude panel, type `/init` and send it. The agent analyses the
   project and drafts a `CLAUDE.md`. Accept the file.
2. Open `templates/CLAUDE.md.template` alongside it. **Edit the generated
   file yourself** so that it contains at least:
   - the commands to run the tests and the CLI;
   - the four business rules, copied accurately from the docstring;
   - "use Decimal for money, never float";
   - "never edit or delete an existing test to make it pass".
3. Keep it short (under 50 lines). Everything in it is loaded every time,
   so padding costs attention. Delete anything vague, such as "write good code".
4. Start a **new conversation** (the `+` button or a new tab), then ask:
   `What rules must you follow in this project?` Check that the answer
   reflects your file.
5. Commit: `git add CLAUDE.md && git commit -m "Add project instructions for the agent"`.

In your log, note one thing `/init` got wrong or left out, and why you
think it missed it.

---

## Step 5: Fix a reported bug, test first (40 minutes)

The client's accountant sends this message:

> "An order of 10 items at KES 100 each, with a 10% discount, came out as a
> total of KES 1,060.00. By our calculation it should be KES 1,044.00.
> Please fix this urgently."

**Do the following in order. Do not ask the agent to fix it yet.**

1. **Work it out by hand** in your log, using the four business rules.
   Is the accountant right? Which rule does the code break?
2. **Write a failing test yourself**, without the agent. Add to
   `tests/test_invoices.py`:

   ```python
   def test_vat_is_charged_on_the_discounted_subtotal():
       breakdown = invoice_total([item(10, "100.00")], discount_percent=10)
       assert breakdown["discounted_subtotal"] == Decimal("900.00")
       assert breakdown["vat"] == Decimal(...)    # fill in from your hand calculation
       assert breakdown["total"] == Decimal(...)  # fill in from your hand calculation
   ```

3. Run `python -m pytest -q`. **Confirm the new test fails** and that the
   failure message shows the wrong value. A test that has never failed has
   not proved anything.
4. Commit the failing test: `git commit -am "Add failing test for VAT after discount"`.
5. Now ask the agent:

   ```
   The test test_vat_is_charged_on_the_discounted_subtotal fails.
   Find the cause and fix the code so that it obeys business rule 3.
   Do not modify any test. Run the full test suite when you are done.
   ```

6. In Manual mode, read the proposed diff **before** accepting. It should be
   a very small change. If the agent proposes to edit a test, reject that
   edit and tell it why.
7. Run the tests yourself. Then run the CLI with a 10% discount:

   ```bash
   python -m sales_toolkit invoice data/sample_sales.csv --discount 10
   ```

   The total should now be **KES 19,167.29 or KES 19,167.30**. Note which
   one you get. (The one-cent difference is not a mistake in these
   instructions; it is investigated in Master's extension M1. Undergraduates:
   write one sentence in your log suggesting why two answers are possible.)
8. Commit with a message that explains the fix, then write your log entry.

---

## Step 6: Write a specification before asking for a feature (40 minutes)

The client now asks:

> "We would like to see how much we sold in each category, with the biggest
> category first, and what share of the sales each category is."

This is vague. An agent given only this sentence will make dozens of
decisions for you. Your job is to make those decisions yourself.

1. Copy the template: `cp templates/TASK_SPEC.md docs/TASK_SPEC.md`.
2. Complete **every** section. At minimum, decide and write down:
   - whether amounts are before or after discount and VAT;
   - how the share is shown (for example `37.80%`) and how it is rounded;
   - what happens when two categories have the same amount;
   - what happens with an empty file;
   - the command the user will type (for example
     `python -m sales_toolkit report data/sample_sales.csv`) and its exact output format.
3. Compute **two worked examples by hand**, one of which is the provided
   `data/sample_sales.csv`. (Check: the Stationery total is KES 6,940.00.)
4. List anything still ambiguous under **Open questions** and decide each one.
5. **Optional but recommended:** ask the agent to critique your specification
   without writing code:

   ```
   Read docs/TASK_SPEC.md. Do not write any code. List every ambiguity,
   missing edge case or contradiction you can find.
   ```

   Accept only the suggestions you agree with, and update the specification.
6. Commit the specification.

---

## Step 7: Plan before code (25 minutes)

1. In the prompt box, type:

   ```
   /plan Implement the feature described in docs/TASK_SPEC.md.
   ```

   (Alternatively, switch the permission mode to **Plan**.) In Plan mode the
   agent describes what it intends to do and waits for your approval. VS Code
   opens the plan as a Markdown document.
2. **Critique the plan.** Add inline comments to the plan document for
   anything you disagree with. Check in particular:
   - Does it modify only the files your specification allows?
   - Does it write tests before or alongside the code?
   - Does it handle every worked example and edge case in your specification?
   - Does it add any dependency?
3. You must request **at least one change** to the plan, even if small, and
   record in your log what you changed and why. If the plan is genuinely
   perfect, ask for the tests to be written first as a separate step.
4. Do not approve the plan yet. Continue to Step 8.

---

## Step 8: Implement test-first and review every change (50 minutes)

1. Tell the agent to proceed **in two stages**:

   ```
   Stage 1 only: write the tests for the report feature from the worked
   examples in docs/TASK_SPEC.md. Do not write the implementation yet.
   Run the tests and confirm they fail for the right reason.
   ```

2. Review the new tests against your specification **line by line**.
   Check that each expected value matches your hand calculation and was
   not computed by calling the code under test. Correct anything wrong.
3. Then:

   ```
   Stage 2: implement the feature so that these tests pass, following the
   approved plan. Do not modify the tests.
   ```

4. Review each proposed edit using `templates/REVIEW_CHECKLIST.md`. Use the
   **Accept this change** and **Reject this change** buttons to review one
   change at a time.
5. **Reject or revise at least one change**, and explain why in your log.
   Typical good reasons: unclear name, duplicated logic, use of `float`, an
   error that is silently ignored, or a change outside the agreed files.
6. Run the full test suite and the new command yourself. Compare the output
   with your specification, character by character.
7. Commit in **small, meaningful commits** (for example, tests first, then
   implementation). Write your log entry.

> **If things go wrong:** hover over an earlier message in the conversation
> to find the rewind button. **Rewind code to here** reverts the agent's
> file edits to that point. This is useful, but Git is still your real
> safety net: commit often.

---

## Step 9: Catch the agent being wrong (40 minutes)

Open `exercises/review_agent_output/currency.py`. Treat it as a pull request
an agent produced when asked to "add KES/USD currency conversion". It looks
professional. It contains **at least seven** defects, ranging from wrong
arithmetic to security problems.

1. **Without using the agent**, review the file with
   `templates/REVIEW_CHECKLIST.md`. Write each defect you find in
   `docs/REVIEW_currency.md` using this format:

   | # | Line(s) | Defect | Why it matters | How to fix it |
   |---|---------|--------|----------------|---------------|

2. Only then, ask the agent to review the same file. Compare its findings
   with yours. Record in the file: which defects it found that you missed,
   which you found that it missed, and whether it reported anything that was
   **not** actually a defect.

> **Think about:** one of these defects could cause harm far beyond this
> project if a student ran `pip install` on the advice of the code. Which
> one, and why? Search for the term "package hallucination".

---

# Part C: Make the agent work your way

## Step 10: Write a skill (30 minutes)

`CLAUDE.md` is always loaded. A **skill** is loaded only when relevant, so
it can hold a detailed procedure without cluttering every session.

1. Create the folder and copy the template:

   ```bash
   mkdir -p .claude/skills/add-tests
   cp templates/SKILL.md.template .claude/skills/add-tests/SKILL.md
   ```

   (On Windows PowerShell: `mkdir .claude\skills\add-tests` then `cp` as above.)
2. Read the template and improve it. Make at least two changes of your own
   based on what you learnt in Steps 5 and 8.
3. Start a new conversation and invoke it explicitly:

   ```
   /add-tests apply_discount in sales_toolkit/invoices.py
   ```

4. Check: did the agent follow every step of your skill? Did it compute
   expected values by hand? Did it avoid changing `sales_toolkit/`?
5. Start another new conversation and ask, **without** the slash command:
   `Can you add tests for the money() function?` Did the agent load the
   skill on its own? If not, improve the `description` line (it decides
   when the skill is used) and try again.
6. Commit the skill and any tests you accepted.

Documentation: <https://code.claude.com/docs/en/skills>

---

## Step 11: Create a reviewer subagent (30 minutes)

A **subagent** is a specialised assistant with its own instructions and its
own, separate context. A read-only reviewer is a classic example: it can
look at your code but cannot change it.

1. Create it:

   ```bash
   mkdir -p .claude/agents
   cp templates/code-reviewer.md.template .claude/agents/code-reviewer.md
   ```

2. Read it. Note that `tools: Read, Glob, Grep` means it cannot edit files.
   Improve the instructions with one rule specific to this project.
3. Start a new conversation and ask:

   ```
   Use the code-reviewer subagent to review the report feature I added in Step 8.
   ```

4. Compare the reviewer's findings with your own review from Step 8.
   Did it find anything you missed? Did it raise anything that was wrong?
   Act on findings you agree with; record the others with your reason for
   disagreeing.
5. Commit the subagent file.

Documentation: <https://code.claude.com/docs/en/sub-agents>

---

## Step 12: Work safely and responsibly (20 minutes)

Answer each question in your log in two or three sentences.

1. **Permissions.** Why did this lab require Manual mode? Describe one
   situation in which a faster mode would be reasonable, and one in which
   it would be dangerous.
2. **Secrets.** Where should an API key for a real currency service live,
   so that neither the agent nor Git ever stores it in code? (Hint: environment
   variables and `.gitignore`.)
3. **Personal data.** Suppose the sales file contained customer names and
   phone numbers. Under the Kenya Data Protection Act, 2019, what should you
   consider before letting a cloud-hosted agent read that file? What could
   you do instead (for example, synthetic or anonymised data)?
4. **Dependencies.** What will you check before installing any package an
   agent recommends?
5. **Disclosure.** Your institution's academic integrity policy applies to
   AI-assisted work. How does your AI use log satisfy it?

---

## Step 13: Submit (15 minutes)

1. Make sure your repository contains:
   - your fixed code and new feature, with all tests passing;
   - `CLAUDE.md`, `.claude/skills/add-tests/SKILL.md`, `.claude/agents/code-reviewer.md`;
   - `docs/AI_USE_LOG.md` (one entry per step), `docs/TASK_SPEC.md`, `docs/REVIEW_currency.md`.
2. Run `python -m pytest -q` one final time and paste the result at the end
   of your log.
3. Add a short **reflection** (300 to 400 words for undergraduates) at the
   end of your log:
   - Where did the agent save you the most time?
   - Where would you have shipped a defect if you had trusted it?
   - Which of the six skills (specify, plan, delegate, verify, review, own)
     do you most need to practise, and how will you practise it?
4. Push to your fork and submit the repository link as instructed by your lecturer.

---

# Master's extensions

Complete **all four**. Write your answers in `docs/MASTERS.md`.

### M1: Specification ambiguity (rounding)

In Step 5 the total could be KES 19,167.29 or KES 19,167.30. Explain
precisely where the one cent comes from. Which reading of the business rules
is better for the client, and why? Write the additional business rule that
removes the ambiguity, add it to `CLAUDE.md`, and add a test that pins the
behaviour. Then discuss: who should resolve this kind of ambiguity, the
developer, the agent or the client, and what happens in practice when an
agent resolves it silently?

### M2: A small controlled comparison

Choose a small new feature (for example, rejecting rows with a negative
quantity, with a clear error message). Implement it **twice** on two
separate branches:

- **Branch A:** a single one-sentence request, Edit automatically mode, no plan.
- **Branch B:** the full workflow from Steps 6 to 8.

For each, record: time taken, number of agent turns, number of defects you
found afterwards (using the same review checklist), and lines changed.
Present the results in a table and discuss them. Be explicit about the
threats to validity: one person, one task, an order effect (you learnt from
the first attempt), and model non-determinism. What would a more rigorous
study need?

### M3: Evaluate your skill

Write five different prompts that **should** trigger your `add-tests` skill
and five that **should not**. Run each in a fresh conversation and record
whether the skill was used. Report the results as a small confusion matrix,
revise the `description`, and repeat. What does this tell you about relying
on automatic invocation?

### M4: Critical essay (800 to 1,000 words)

In a 2026 interview with *The Economist*, Andrew Ng argued that the real
problem for young workers is that universities are too slow to teach the
skills employers want now
(<https://www.youtube.com/watch?v=J-sMqnzHwI0>). Using that argument, your
evidence from this lab, and at least three scholarly or industry sources,
answer: **What should an "AI-native" computing graduate be able to do, and
what must a university still teach that an agent cannot substitute for?**
Take a position, and address the strongest counter-argument to it.

---

## Getting help

- Claude Code in VS Code: <https://code.claude.com/docs/en/vscode-extension>
- Project memory (`CLAUDE.md`): <https://code.claude.com/docs/en/memory>
- Best practices: <https://code.claude.com/docs/en/best-practices>
- Ask the agent itself how a feature works, then **verify** the answer in the documentation.
