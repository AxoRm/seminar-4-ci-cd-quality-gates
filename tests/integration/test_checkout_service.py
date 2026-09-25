import pytest

from shop.service import checkout


def test_paid_checkout_creates_order_with_correct_total() -> None:
    assert checkout(7, 7, [120, 80], True) == {
        "total_cents": 200,
        "payment": "paid",
        "order_status": "created",
    }


def test_declined_payment_does_not_create_order() -> None:
    assert checkout(7, 7, [120], False)["order_status"] == "not_created"


def test_checkout_prevents_access_to_another_users_order() -> None:
    with pytest.raises(PermissionError):
        checkout(7, 8, [120], True)


def test_checkout_rejects_empty_cart() -> None:
    with pytest.raises(ValueError):
        checkout(7, 7, [], True)


def test_checkout_rejects_invalid_user() -> None:
    with pytest.raises(PermissionError):
        checkout(0, 7, [120], True)
