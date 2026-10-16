"""Command-line entry point.

Usage:
    python -m sales_toolkit invoice data/sample_sales.csv
    python -m sales_toolkit invoice data/sample_sales.csv --discount 10
"""

from __future__ import annotations

import argparse
import sys

from sales_toolkit.invoices import invoice_total, load_line_items


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sales_toolkit")
    commands = parser.add_subparsers(dest="command", required=True)

    invoice = commands.add_parser("invoice", help="print an invoice breakdown")
    invoice.add_argument("path", help="path to a sales CSV file")
    invoice.add_argument(
        "--discount", default="0", help="discount percentage (0 to 100)"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "invoice":
        items = load_line_items(args.path)
        breakdown = invoice_total(items, args.discount)
        for key, value in breakdown.items():
            print(f"{key:<20} KES {value:>12,}")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
