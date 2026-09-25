"""The example creates an order only after successful payment."""


def order_status(payment_status: str) -> str:
    if payment_status == "paid":
        return "created"
    return "not_created"
