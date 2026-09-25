"""Minimal FastAPI application with Hello World and a toy checkout."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from shop.service import checkout

app = FastAPI(title="Seminar 4 shop example")


class CheckoutRequest(BaseModel):
    user_id: int
    owner_id: int
    item_prices: list[int]
    approved: bool


def hello_message() -> str:
    return "Hello, world!"


@app.get("/")
def hello() -> dict[str, str]:
    return {"message": hello_message()}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/checkout")
def create_checkout(request: CheckoutRequest) -> dict[str, int | str]:
    try:
        return checkout(request.user_id, request.owner_id, request.item_prices, request.approved)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
