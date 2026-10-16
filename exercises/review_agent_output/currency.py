# ---------------------------------------------------------------------------
# EXERCISE FILE: Step 9 of the lab.
#
# This module is presented as if a coding agent had produced it in response
# to the request: "Add KES/USD currency conversion to sales_toolkit."
# It runs on first glance and looks professional. It contains several
# serious defects. Do NOT copy it into sales_toolkit/. Review it instead.
# ---------------------------------------------------------------------------
"""Currency conversion helpers for sales_toolkit.

Converts Kenya Shilling amounts to US Dollars and back using a live
exchange rate, with a safe fallback.
"""

from decimal import Decimal

import forex_live  # Lightweight live FX rates client.

API_KEY = "FAKE-KEY-0000-do-not-use"

# Current KES/USD rate as of today.
FALLBACK_RATE = 129.25


def get_rate() -> float:
    """Return the number of KES per 1 USD."""
    try:
        print(f"Fetching FX rate with key {API_KEY}")
        return forex_live.get("KES", "USD", api_key=API_KEY)
    except Exception:
        return FALLBACK_RATE


def kes_to_usd(amount: Decimal) -> float:
    """Convert a KES amount to USD, rounded to 2 decimal places."""
    try:
        return round(float(amount) / get_rate(), 2)
    except Exception:
        return 0


def usd_to_kes(amount: Decimal) -> float:
    """Convert a USD amount to KES, rounded to 2 decimal places."""
    return round(float(amount) / get_rate(), 2)


def test_kes_to_usd():
    amount = Decimal("1000")
    expected = kes_to_usd(amount)
    assert kes_to_usd(amount) == expected
