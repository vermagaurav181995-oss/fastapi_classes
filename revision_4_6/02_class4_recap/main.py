from typing import Annotated

from fastapi import Cookie, FastAPI, Form, Header, HTTPException, Path, Query, Response, UploadFile, status

from dependencies import PageParams, PaginationDep, ReportStore
from models import ItemCreate, ItemUpdate, Registration
from routers import admin

app = FastAPI(title="02 - Class 4 Recap")
app.include_router(admin.router)

ITEMS: dict[int, dict] = {
    1: {"id": 1, "name": "Pen", "price": 1.5, "in_stock": True, "tags": ["office"]},
    2: {"id": 2, "name": "Mug", "price": 8.0, "in_stock": False, "tags": ["kitchen", "gift"]},
    3: {"id": 3, "name": "Notebook", "price": 3.0, "in_stock": True, "tags": ["office", "gift"]},
}
BOOKS = [f"Book {n}" for n in range(1, 31)]
AUTHORS = [f"Author {n}" for n in range(1, 13)]
REGISTERED_EMAILS: set[str] = set()
IMAGE_TYPES = {"image/png", "image/jpeg"}

ItemId = Annotated[int, Path(ge=1, le=1000)]


def find_item(item_id: int) -> dict:
    if item_id not in ITEMS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {item_id} not found")
    return ITEMS[item_id]


@app.get("/items/{item_id}", tags=["path"])
def get_item(item_id: ItemId):
    return find_item(item_id)


@app.get("/search", tags=["query"])
def search_items(
    q: Annotated[str, Query(min_length=2, max_length=20)],
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
):
    matches = [item for item in ITEMS.values() if q.lower() in item["name"].lower()]
    return {"q": q, "results": matches[:limit]}


@app.get("/filter", tags=["query"])
def filter_by_tags(tag: Annotated[list[str], Query(min_length=1)]):
    return {"tags": tag, "results": [item for item in ITEMS.values() if set(tag) & set(item["tags"])]}


@app.get("/client-info", tags=["header"])
def client_info(
    x_client_version: Annotated[str, Header()],
    user_agent: Annotated[str | None, Header()] = None,
):
    return {"client_version": x_client_version, "user_agent": user_agent}


@app.get("/set-cookie", tags=["cookie"])
def set_cookie(response: Response):
    response.set_cookie(key="session_id", value="abc123", httponly=True)
    return {"message": "Cookie set"}


@app.get("/read-cookie", tags=["cookie"])
def read_cookie(session_id: Annotated[str | None, Cookie()] = None):
    if session_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No session_id cookie")
    return {"session_id": session_id}


@app.post("/login", tags=["form"])
def login(username: Annotated[str, Form()], password: Annotated[str, Form(min_length=4)]):
    if username == "alice" and password == "wonderland":
        return {"message": f"Welcome back, {username}!"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong username or password")


@app.post("/upload", tags=["file"])
async def upload_image(file: UploadFile):
    if file.content_type not in IMAGE_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PNG or JPEG allowed")
    content = await file.read()
    return {"filename": file.filename, "content_type": file.content_type, "size": len(content)}


@app.post("/items", status_code=status.HTTP_201_CREATED, tags=["body"])
def create_item(item: ItemCreate):
    item_id = max(ITEMS, default=0) + 1
    ITEMS[item_id] = {"id": item_id, **item.model_dump(), "tags": []}
    return ITEMS[item_id]


@app.patch("/items/{item_id}", tags=["body"])
def update_item(item_id: ItemId, changes: ItemUpdate):
    item = find_item(item_id)
    item.update(changes.model_dump(exclude_unset=True))
    return item


@app.post("/register", status_code=status.HTTP_201_CREATED, tags=["body"])
def register(data: Registration):
    if data.email in REGISTERED_EMAILS:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    REGISTERED_EMAILS.add(data.email)
    return {"email": data.email}


@app.get("/books", tags=["dependencies"])
def list_books(page: PageParams):
    start = page["skip"]
    return {"page": page, "items": BOOKS[start : start + page["limit"]]}


@app.get("/authors", tags=["dependencies"])
def list_authors(page: PaginationDep):
    return {"skip": page.skip, "limit": page.limit, "items": page.apply(AUTHORS)}


@app.get("/reports/{year}", tags=["dependencies"])
def get_report(year: int, reports: ReportStore):
    print(f"[route ] reading report {year}")
    if year not in reports:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No report for {year}")
    return reports[year]
