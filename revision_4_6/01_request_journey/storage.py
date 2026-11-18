USERS: dict[int, dict] = {}

BOOKS: dict[int, dict] = {
    1: {"id": 1, "title": "Dune"},
    2: {"id": 2, "title": "1984"},
    3: {"id": 3, "title": "Neuromancer"},
}

DELETION_LOG: list[str] = []


def find_user_by_email(email: str) -> dict | None:
    return next((user for user in USERS.values() if user["email"] == email), None)
