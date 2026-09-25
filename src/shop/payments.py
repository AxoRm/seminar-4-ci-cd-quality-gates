"""A fake payment result: no real payment provider is called."""


def payment_result(amount_cents: int, approved: bool) -> str:
    if amount_cents <= 0:
        raise ValueError("Payment amount must be positive")
    if approved:
        return "paid"
    return "declined"
