DEFAULT_BOOKS = [
    {"title": "Dune", "price": 9.99},
    {"title": "1984", "price": 7.5},
    {"title": "Neuromancer", "price": 8.25},
]

BOOKS: dict[int, dict] = {}
USERS: dict[int, dict] = {}
SENT_EMAILS: list[dict] = []


def next_id(table: dict[int, dict]) -> int:
    return max(table, default=0) + 1


def seed_books() -> None:
    for book in DEFAULT_BOOKS:
        book_id = next_id(BOOKS)
        BOOKS[book_id] = {"id": book_id, **book}


def find_user_by_email(email: str) -> dict | None:
    return next((user for user in USERS.values() if user["email"] == email), None)


def add_user(email: str, hashed_password: str, role: str = "user") -> dict:
    user_id = next_id(USERS)
    USERS[user_id] = {"id": user_id, "email": email, "hashed_password": hashed_password, "role": role}
    return USERS[user_id]


seed_books()
