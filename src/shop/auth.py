"""Simple ownership check for example orders."""


def can_view_order(user_id: int, owner_id: int) -> bool:
    if user_id <= 0:
        return False
    return user_id == owner_id
