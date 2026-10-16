"""Invoice calculations for a small Nairobi retailer.

All monetary values are in Kenya Shillings (KES) and are handled as
``Decimal`` to avoid floating-point rounding errors. Unit prices in the
input data are VAT-exclusive.

Business rules (agreed with the client):
    1. A line total is quantity multiplied by unit price.
    2. A discount, when given, is a percentage applied to the subtotal.
    3. VAT at 16% is charged on the amount the customer actually pays
       for the goods, that is, on the subtotal AFTER any discount.
    4. Every reported amount is rounded to 2 decimal places, with halves
       rounded up (ROUND_HALF_UP).
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

VAT_RATE = Decimal("0.16")
CENTS = Decimal("0.01")


@dataclass(frozen=True)
class LineItem:
    """One row of a sales file."""

    sku: str
    description: str
    category: str
    quantity: int
    unit_price: Decimal


def money(amount: Decimal) -> Decimal:
    """Round an amount to 2 decimal places using ROUND_HALF_UP."""
    return amount.quantize(CENTS, rounding=ROUND_HALF_UP)


def load_line_items(path: str | Path) -> list[LineItem]:
    """Read line items from a CSV file with the columns
    sku, description, category, quantity, unit_price."""
    items: list[LineItem] = []
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            items.append(
                LineItem(
                    sku=row["sku"].strip(),
                    description=row["description"].strip(),
                    category=row["category"].strip(),
                    quantity=int(row["quantity"]),
                    unit_price=Decimal(row["unit_price"]),
                )
            )
    return items


def line_total(item: LineItem) -> Decimal:
    """Return quantity multiplied by unit price (rule 1)."""
    return item.unit_price * item.quantity


def subtotal(items: list[LineItem]) -> Decimal:
    """Return the sum of all line totals."""
    return sum((line_total(item) for item in items), Decimal("0"))


def apply_discount(amount: Decimal, percent: Decimal | int | str = 0) -> Decimal:
    """Return the amount after deducting a percentage discount (rule 2)."""
    percent = Decimal(str(percent))
    if percent < 0 or percent > 100:
        raise ValueError("discount percent must be between 0 and 100")
    return amount * (Decimal("1") - percent / Decimal("100"))


def vat(amount: Decimal) -> Decimal:
    """Return the VAT payable on an amount."""
    return amount * VAT_RATE


def invoice_total(
    items: list[LineItem], discount_percent: Decimal | int | str = 0
) -> dict[str, Decimal]:
    """Return a breakdown of the invoice.

    Keys: subtotal, discounted_subtotal, vat, total.
    """
    gross = subtotal(items)
    discounted = apply_discount(gross, discount_percent)
    tax = vat(gross)
    return {
        "subtotal": money(gross),
        "discounted_subtotal": money(discounted),
        "vat": money(tax),
        "total": money(discounted + tax),
    }
