from fastapi.testclient import TestClient

from shop.main import app

client = TestClient(app)


def test_hello_and_health_http_responses() -> None:
    assert client.get("/").json() == {"message": "Hello, world!"}
    assert client.get("/health").json() == {"status": "ok"}


def test_checkout_http_success_and_access_error() -> None:
    payload = {"user_id": 7, "owner_id": 7, "item_prices": [120, 80], "approved": True}
    response = client.post("/checkout", json=payload)
    assert response.status_code == 200
    assert response.json()["total_cents"] == 200

    payload["owner_id"] = 8
    assert client.post("/checkout", json=payload).status_code == 403


def test_checkout_http_rejects_empty_cart() -> None:
    response = client.post(
        "/checkout",
        json={"user_id": 7, "owner_id": 7, "item_prices": [], "approved": True},
    )
    assert response.status_code == 400
