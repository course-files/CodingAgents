"""The product catalogue: everything the shop sells, with official prices.

Why prices come from here and never from the model
--------------------------------------------------
A language model is good at understanding messy human language. It is not a
reliable source of facts such as today's price, and it can be persuaded by a
cleverly written message to say almost anything. So the design rule for
this whole project is:

    The model decides WHAT the customer asked for (which product, how many).
    Our code decides HOW MUCH it costs, using this catalogue.

If the model ever mentions a price, we ignore it.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from sales_toolkit.invoices import LineItem

DEFAULT_CATALOGUE = Path(__file__).resolve().parents[2] / "data" / "catalogue.csv"


@dataclass(frozen=True)
class CatalogueItem:
    sku: str
    description: str
    category: str
    unit_price: Decimal

    def to_line_item(self, quantity: int) -> LineItem:
        """Build an invoice line using the OFFICIAL catalogue price."""
        return LineItem(self.sku, self.description, self.category, quantity, self.unit_price)


def load_catalogue(path: str | Path = DEFAULT_CATALOGUE) -> dict[str, CatalogueItem]:
    """Return the catalogue as a dictionary keyed by SKU, e.g. catalogue["SKU-003"]."""
    catalogue: dict[str, CatalogueItem] = {}
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            item = CatalogueItem(
                sku=row["sku"].strip(),
                description=row["description"].strip(),
                category=row["category"].strip(),
                unit_price=Decimal(row["unit_price"]),
            )
            catalogue[item.sku] = item
    return catalogue


def catalogue_as_text(catalogue: dict[str, CatalogueItem]) -> str:
    """Format the catalogue for inclusion in a prompt, one product per line.

    Prices are left out on purpose: the model does not need them to identify
    products, and leaving them out removes any temptation to calculate.
    """
    return "\n".join(
        f"{item.sku} | {item.description} | {item.category}" for item in catalogue.values()
    )
