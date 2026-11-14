from pathlib import Path

UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

AUTHORS: dict[int, dict] = {
    1: {"id": 1, "name": "Frank Herbert"},
    2: {"id": 2, "name": "George Orwell"},
    3: {"id": 3, "name": "William Gibson"},
}

BOOKS: dict[int, dict] = {
    1: {"id": 1, "title": "Dune", "author_id": 1, "price": 9.99, "stock": 5, "cost_price": 4.0, "cover": None},
    2: {"id": 2, "title": "1984", "author_id": 2, "price": 7.5, "stock": 0, "cost_price": 3.0, "cover": None},
    3: {"id": 3, "title": "Animal Farm", "author_id": 2, "price": 6.0, "stock": 8, "cost_price": 2.5, "cover": None},
    4: {"id": 4, "title": "Neuromancer", "author_id": 3, "price": 8.25, "stock": 3, "cost_price": 3.5, "cover": None},
}


def next_id(table: dict[int, dict]) -> int:
    return max(table, default=0) + 1
