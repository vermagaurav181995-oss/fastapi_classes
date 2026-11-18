USERS: dict[int, dict] = {}
NOTES: dict[int, dict] = {}
NOTE_EVENTS: list[str] = []


def find_user_by_email(email: str) -> dict | None:
    return next((user for user in USERS.values() if user["email"] == email), None)


def add_user(email: str, hashed_password: str, role: str = "user") -> dict:
    user_id = max(USERS, default=0) + 1
    USERS[user_id] = {"id": user_id, "email": email, "hashed_password": hashed_password, "role": role}
    return USERS[user_id]


def add_note(title: str, content: str, owner_id: int) -> dict:
    note_id = max(NOTES, default=0) + 1
    NOTES[note_id] = {"id": note_id, "title": title, "content": content, "owner_id": owner_id}
    return NOTES[note_id]
