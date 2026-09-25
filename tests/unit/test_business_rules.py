import pytest

from shop.auth import can_view_order
from shop.orders import order_status
from shop.payments import payment_result
from shop.pricing import total_cents


def test_owner_can_view_order_but_stranger_and_invalid_user_cannot() -> None:
    assert can_view_order(7, 7)
    assert not can_view_order(7, 8)
    assert not can_view_order(0, 7)


def test_total_handles_empty_cart_and_multiple_prices() -> None:
    assert total_cents([]) == 0
    assert total_cents([120, 80]) == 200


def test_payment_rejects_zero_and_records_approval_or_decline() -> None:
    with pytest.raises(ValueError):
        payment_result(0, True)
    assert payment_result(200, True) == "paid"
    assert payment_result(200, False) == "declined"


def test_order_is_created_only_after_payment() -> None:
    assert order_status("paid") == "created"
    assert order_status("declined") == "not_created"
