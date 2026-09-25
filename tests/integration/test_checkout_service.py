import pytest

from shop.service import checkout


def test_checkout_connects_pricing_payment_and_order() -> None:
    assert checkout(7, 7, [120, 80], True) == {
        "total_cents": 200,
        "payment": "paid",
        "order_status": "created",
    }
    assert checkout(7, 7, [120], False)["order_status"] == "not_created"


def test_checkout_prevents_other_users_and_empty_cart() -> None:
    with pytest.raises(PermissionError):
        checkout(7, 8, [120], True)
    with pytest.raises(ValueError):
        checkout(7, 7, [], True)
