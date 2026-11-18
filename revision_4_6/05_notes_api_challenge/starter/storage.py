USERS: dict[int, dict] = {}
NOTES: dict[int, dict] = {}


def find_user_by_email(email: str) -> dict | None:
    raise NotImplementedError


def add_user(email: str, hashed_password: str, role: str = "user") -> dict:
    raise NotImplementedError


def add_note(title: str, content: str, owner_id: int) -> dict:
    raise NotImplementedError
