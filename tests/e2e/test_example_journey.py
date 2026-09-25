"""Backend journey only; a real browser E2E requires a deployed frontend."""

from fastapi.testclient import TestClient

from shop.main import app


def test_example_user_journey() -> None:
    client = TestClient(app)
    assert client.get("/health").status_code == 200
    response = client.post(
        "/checkout",
        json={"user_id": 7, "owner_id": 7, "item_prices": [120, 80], "approved": True},
    )
    assert response.status_code == 200
    assert response.json() == {"total_cents": 200, "payment": "paid", "order_status": "created"}
