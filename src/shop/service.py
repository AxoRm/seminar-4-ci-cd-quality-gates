"""Connect the small business rules into one checkout operation."""

from shop.auth import can_view_order
from shop.orders import order_status
from shop.payments import payment_result
from shop.pricing import total_cents


def checkout(user_id: int, owner_id: int, item_prices: list[int], approved: bool) -> dict[str, int | str]:
    if not can_view_order(user_id, owner_id):
        raise PermissionError("Order belongs to another user")

    total = total_cents(item_prices)
    status = payment_result(total, approved)
    return {"total_cents": total, "payment": status, "order_status": order_status(status)}
