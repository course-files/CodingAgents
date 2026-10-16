"""Tests for sales_toolkit.invoices.

These tests pass on the starter code. Passing tests do not prove the code
is correct; they only prove that the cases someone thought to check work.
"""

from decimal import Decimal
from pathlib import Path

import pytest

from sales_toolkit.invoices import (
    LineItem,
    apply_discount,
    invoice_total,
    line_total,
    load_line_items,
    money,
    subtotal,
)

DATA = Path(__file__).resolve().parent.parent / "data" / "sample_sales.csv"


def item(quantity: int, price: str, category: str = "Stationery") -> LineItem:
    return LineItem("SKU-X", "Test item", category, quantity, Decimal(price))


def test_load_line_items_reads_every_row():
    items = load_line_items(DATA)
    assert len(items) == 8
    assert items[0].sku == "SKU-001"
    assert items[0].unit_price == Decimal("145.00")


def test_line_total_multiplies_quantity_by_price():
    assert line_total(item(3, "100.00")) == Decimal("300.00")


def test_subtotal_adds_line_totals():
    items = [item(1, "100.00"), item(2, "50.50")]
    assert subtotal(items) == Decimal("201.00")


def test_money_rounds_half_up():
    assert money(Decimal("10.005")) == Decimal("10.01")
    assert money(Decimal("10.004")) == Decimal("10.00")


def test_apply_discount_percentage():
    assert apply_discount(Decimal("1000"), 10) == Decimal("900")


def test_apply_discount_rejects_out_of_range():
    with pytest.raises(ValueError):
        apply_discount(Decimal("1000"), 120)


def test_invoice_total_without_discount():
    breakdown = invoice_total([item(10, "100.00")])
    assert breakdown["subtotal"] == Decimal("1000.00")
    assert breakdown["vat"] == Decimal("160.00")
    assert breakdown["total"] == Decimal("1160.00")
