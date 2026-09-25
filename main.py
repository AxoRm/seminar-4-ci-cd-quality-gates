"""Run with `python main.py` or `uvicorn main:app`."""

from shop.main import app, hello_message


if __name__ == "__main__":
    print(hello_message())
