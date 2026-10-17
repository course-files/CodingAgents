# Claude Code: costs and access

**Read this before you pay for anything.** Prices were checked on
17 October 2026 at <https://claude.com/pricing> and can change. Always confirm
the current price on that page.

## Do I have to pay?

**Yes.** Claude Code is **not** included in Claude's free plan. It is included
in every paid plan.

| Plan | Price (USD) | Includes Claude Code | Notes |
|------|-------------|:--------------------:|-------|
| Free | 0 | No | Chat only |
| Pro | 20 per month billed monthly, or 17 per month billed annually (200 up front) | Yes | Enough for this lab |
| Max | From 100 per month | Yes | Higher usage limits; not needed for this lab |
| Team | From 20 per seat per month (annual billing) | Yes | Bought by an organisation |
| Enterprise | Contact sales | Yes | Bought by an organisation |
| Education | Bought by a university | Yes | Not available to buy as an individual |

There is **no individual student discount** at the time of writing. Claude for
Education is a university-wide plan; it is free to students only if their
university has bought it.

You can also use Claude Code with a **Claude Console** account, which is billed
by usage (pay as you go) rather than by subscription. This suits occasional use
but makes the cost harder to predict.

## Part D: the Claude API is billed separately

Part D asks your own program to call a model through its API. **A Claude Pro
subscription does not include API usage**; the API is billed separately, per
token, through a Claude Console account at <https://platform.claude.com>.

You do not have to pay for this. The free Google Gemini API works for every
step of Part D, and the lab is designed for it. If you choose the Claude API:

- Add a small amount of credit and **set a monthly spend limit** in the
  Console before creating a key.
- Use the smallest model, `claude-haiku-5-5`. At the time of writing it is
  priced from USD 0.10 per million input tokens and USD 0.50 per million
  output tokens; check <https://platform.claude.com/docs/en/about-claude/models/overview>
  for current prices. Part D sends a few hundred short requests, so the cost
  should be small, but the spend limit is your safety net.

## If you decide to pay

- **Choose monthly billing** if you only need Claude Code for this course. You
  can cancel before the next billing date.
- **Pay in US dollars.** Your bank may add a foreign-currency fee; check the
  exchange rate and fees before you subscribe.
- **Usage limits apply** even on paid plans and reset over time. Follow the
  context-management advice in Step 9 to make your allowance last.
- **Never share an account** or its login with classmates. It breaches the
  terms of use and exposes your personal data.

## If you do not want to pay

Use the **[GitHub Copilot track](../github-copilot/)**. It teaches the same
skills, uses the same codebase and exercises, and is marked with the same
rubric. Most students in this course are expected to use it, because Copilot
is free for verified students through the GitHub Student Developer Pack.

Choosing the free track does **not** reduce your mark. The lab assesses how
well you specify, verify and review work, not which tool you used.

## Sources

- Claude plans and pricing: <https://claude.com/pricing>
- Claude Code in VS Code (account requirements): <https://code.claude.com/docs/en/vscode-extension>
- API billing is separate from paid plans: <https://support.claude.com/en/articles/9876003-i-have-a-paid-claude-subscription-pro-max-team-or-enterprise-plans-why-do-i-have-to-pay-separately-to-use-the-claude-api-and-console>
- Claude models and API prices: <https://platform.claude.com/docs/en/about-claude/models/overview>
