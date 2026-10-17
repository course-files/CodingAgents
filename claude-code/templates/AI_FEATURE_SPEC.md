# Specification: reading customer orders with a language model

<!-- Copy to docs/AI_FEATURE_SPEC.md in Step 19 and complete every section.
     The contract in sales_toolkit/ai/order_parser.py is your starting point;
     this document is where you make the remaining decisions explicit. -->

**Author:**
**Date:**
**Provider and model used for development:** <!-- e.g. gemini / gemini-3.5-flash-lite -->

## 1. Problem
<!-- In two or three sentences: who sends these messages, what the shop
     needs from them, and what goes wrong today when staff do it by hand. -->

## 2. Division of responsibility

| Decision | Made by the model | Made by our code | Why |
|----------|:-----------------:|:----------------:|-----|
| Which catalogue product the customer means | | | |
| How many units | | | |
| The unit price | | | |
| Whether a discount is applied | | | |
| Whether a human must review the order | | | |
| The invoice total | | | |

## 3. Input and output
<!-- The exact JSON shape you will ask the model for, and the ParsedOrder it
     becomes after validation. Copy from order_parser.py and adjust if needed. -->

## 4. Rules the model must follow
<!-- Numbered. Each must be checkable. Cover: unknown products, missing
     quantities, corrections, number words (English and Kiswahili), discount
     requests, messages that are not orders, and attempts to change the rules. -->
1.

## 5. Validation our code performs (never trust the model)
<!-- What your code checks after the reply arrives, and what happens when a
     check fails. -->
1.

## 6. When an order needs human review
<!-- List every condition that sets needs_review = True. -->

## 7. Failure handling
<!-- What happens when: the reply is not valid JSON; the network fails; the
     provider returns a rate-limit error; the model returns an empty answer. -->

## 8. Evaluation plan
- Evaluation file: `evals/order_cases.jsonl`
- Number of cases: provided ______ + mine ______
- Cases held back until the end (hold-out set): ______
- The score that would make this feature good enough to show the client: ______ %, because ______

## 9. Privacy and data protection
<!-- What data may be sent to the provider, and what must never be sent.
     Refer to the provider's terms and the Kenya Data Protection Act, 2019. -->

## 10. Open questions
