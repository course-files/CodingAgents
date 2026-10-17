"""Measure how well parse_order performs on a set of labelled examples.

Why an evaluation ("eval") is needed
------------------------------------
Normal unit tests check code that always behaves the same way. A language
model does not: the same message can produce slightly different answers on
different runs, and a change to the prompt that fixes one case can quietly
break another. The only reliable way to know whether a change helped is to
run the same set of examples before and after, and compare the scores.

This script is that measuring instrument. It does not change your code.

Usage (run from the track folder, with your virtual environment active):

    python evals/run_eval.py                       # uses LLM_PROVIDER from .env
    python evals/run_eval.py --provider keyword    # offline rule-based baseline
    python evals/run_eval.py --limit 3             # only the first 3 cases
    python evals/run_eval.py --delay 6             # wait 6 s between calls
    python evals/run_eval.py --repeat 3            # run every case 3 times

Each run prints a table and saves full details to evals/results/ (ignored by
Git). Copy the summary you need into docs/EVAL_REPORT.md.

Format of a case (one JSON object per line in evals/order_cases.jsonl):

    {"id": "P05", "type": "item not in catalogue",
     "message": "Send 4 HDMI cables and a laptop bag.",
     "expected": {"items": {"SKU-008": 4},
                  "requested_discount_percent": null,
                  "needs_review": true}}

"needs_review" is optional. When it is present, it is checked too.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from decimal import Decimal
from pathlib import Path

# Make "import sales_toolkit" work when this file is run directly.
TRACK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TRACK_ROOT))

from sales_toolkit.ai.catalogue import load_catalogue  # noqa: E402
from sales_toolkit.ai.llm_client import LLMError, get_client  # noqa: E402
from sales_toolkit.ai.order_parser import parse_order  # noqa: E402

DEFAULT_CASES = TRACK_ROOT / "evals" / "order_cases.jsonl"
RESULTS_DIR = TRACK_ROOT / "evals" / "results"


def load_cases(path: Path) -> list[dict]:
    cases = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue  # blank lines and comment lines are allowed
        try:
            cases.append(json.loads(line))
        except json.JSONDecodeError as exc:
            sys.exit(f"{path.name} line {number} is not valid JSON: {exc}")
    return cases


def to_number(value):
    """Compare discounts as numbers, so 10, 10.0 and Decimal('10') are equal."""
    return None if value is None else Decimal(str(value))


def baseline_parse(message: str, client):
    """Used only before parse_order exists, and only with the keyword client.

    It accepts whatever JSON the client returns, with NO validation. This
    lets you measure the offline keyword baseline in Step 20.
    """
    from sales_toolkit.ai.order_parser import OrderLine, ParsedOrder

    data = json.loads(client.generate("", message).text)
    return ParsedOrder(
        items=[OrderLine(i["sku"], int(i["quantity"])) for i in data.get("items", [])],
        unmatched=data.get("unmatched", []),
        requested_discount_percent=to_number(data.get("requested_discount_percent")),
        needs_review=bool(data.get("needs_review")),
    )


def score_case(case: dict, order) -> tuple[bool, list[str]]:
    """Return (passed, reasons for failure)."""
    expected = case["expected"]
    reasons = []

    got_items: dict[str, int] = {}
    for line in order.items:
        got_items[line.sku] = got_items.get(line.sku, 0) + line.quantity
    if got_items != expected["items"]:
        reasons.append(f"items: expected {expected['items']}, got {got_items}")

    want_discount = to_number(expected.get("requested_discount_percent"))
    got_discount = to_number(order.requested_discount_percent)
    if want_discount != got_discount:
        reasons.append(f"discount: expected {want_discount}, got {got_discount}")

    if "needs_review" in expected and expected["needs_review"] != order.needs_review:
        reasons.append(
            f"needs_review: expected {expected['needs_review']}, got {order.needs_review}"
        )
    return (not reasons, reasons)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--provider", help="override LLM_PROVIDER for this run")
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--limit", type=int, help="only run the first N cases")
    parser.add_argument("--repeat", type=int, default=1, help="runs per case")
    parser.add_argument(
        "--delay", type=float, default=None,
        help="seconds to wait between model calls (default: 5 for real models, 0 offline)",
    )
    args = parser.parse_args()

    try:
        client = get_client(args.provider)
    except LLMError as exc:
        sys.exit(f"Setup problem: {exc}")

    # Free tiers limit how many requests you may send per minute. A short
    # pause between calls keeps a class of students under those limits.
    delay = args.delay if args.delay is not None else (0 if client.provider == "keyword" else 5)

    catalogue = load_catalogue()
    cases = load_cases(args.cases)[: args.limit]
    print(f"Provider: {client.provider}   Model: {client.model}   "
          f"Cases: {len(cases)}   Repeats: {args.repeat}\n")

    rows, passed = [], 0
    total = len(cases) * args.repeat
    for case in cases:
        for run in range(1, args.repeat + 1):
            started = time.perf_counter()
            try:
                order = parse_order(case["message"], catalogue, client)
            except NotImplementedError:
                if client.provider != "keyword":
                    sys.exit("parse_order is not implemented yet. Complete Step 21 first, "
                             "or use --provider keyword for the offline baseline.")
                order = baseline_parse(case["message"], client)
            except LLMError as exc:
                sys.exit(f"Stopped: the model call failed. {exc}")
            seconds = time.perf_counter() - started
            ok, reasons = score_case(case, order)
            passed += ok
            label = case["id"] if args.repeat == 1 else f"{case['id']}#{run}"
            print(f"{'PASS' if ok else 'FAIL'}  {label:<8} {case.get('type', ''):<30} {seconds:5.1f}s")
            for reason in reasons:
                print(f"        {reason}")
            rows.append({
                "id": case["id"], "run": run, "type": case.get("type"),
                "passed": ok, "reasons": reasons, "seconds": round(seconds, 2),
                "items": [vars(line) for line in order.items],
                "unmatched": order.unmatched,
                "requested_discount_percent": None if order.requested_discount_percent is None
                else str(order.requested_discount_percent),
                "needs_review": order.needs_review, "problems": order.problems,
            })
            if delay:
                time.sleep(delay)

    accuracy = 100 * passed / total if total else 0
    print(f"\nPassed {passed} of {total} ({accuracy:.1f}%)")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out = RESULTS_DIR / f"{stamp}-{client.provider}.json"
    out.write_text(json.dumps({
        "provider": client.provider, "model": client.model, "cases_file": args.cases.name,
        "passed": passed, "total": total, "accuracy_percent": round(accuracy, 1),
        "results": rows,
    }, indent=2), encoding="utf-8")
    print(f"Details saved to {out.relative_to(TRACK_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
