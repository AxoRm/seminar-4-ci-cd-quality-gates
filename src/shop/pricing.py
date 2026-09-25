"""Prices are integer cents, so totals avoid floating-point rounding."""


def total_cents(item_prices: list[int]) -> int:
    if not item_prices:
        return 0
    return sum(item_prices)
