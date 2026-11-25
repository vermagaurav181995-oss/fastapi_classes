USERS: dict[int, dict] = {}
PROJECTS: dict[int, dict] = {}
TASKS: dict[int, dict] = {}


def next_id(table: dict[int, dict]) -> int:
    return max(table, default=0) + 1


def find_user_by_email(email: str) -> dict | None:
    return next((user for user in USERS.values() if user["email"] == email), None)


def add_user(email: str, hashed_password: str, role: str = "user") -> dict:
    user_id = next_id(USERS)
    USERS[user_id] = {"id": user_id, "email": email, "hashed_password": hashed_password, "role": role}
    return USERS[user_id]
