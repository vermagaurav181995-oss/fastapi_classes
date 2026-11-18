USERS: dict[int, dict] = {}
SENT_EMAILS: list[str] = []


def find_user_by_email(email: str) -> dict | None:
    return next((user for user in USERS.values() if user["email"] == email), None)


def add_user(email: str, hashed_password: str, role: str = "user") -> dict:
    user_id = max(USERS, default=0) + 1
    USERS[user_id] = {"id": user_id, "email": email, "hashed_password": hashed_password, "role": role}
    return USERS[user_id]
