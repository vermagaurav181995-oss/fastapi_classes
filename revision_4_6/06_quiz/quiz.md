# Revision Quiz: Class 4 & Class 6

10 questions. Answers are in `answers.md`; don't peek!

---

**1. List query parameters**
You want `GET /filter?tag=a&tag=b` to give you `["a", "b"]`. What's wrong with this, and how do you fix it?
```python
@app.get("/filter")
def filter_items(tag: list[str] | None = None): ...
```

**2. 404 or 422?**
`item_id: Annotated[int, Path(ge=1)]`. What status code does each request return, and *who* produces it (FastAPI or your code)?
a) `GET /items/0`  b) `GET /items/abc`  c) `GET /items/42` when item 42 doesn't exist

**3. PATCH**
Your stored item is `{"name": "Pen", "price": 1.5}`. A client sends `PATCH /items/1` with `{"price": 2}`. Your code does `item.update(changes.model_dump())`. What does the item look like afterwards, and which one argument fixes it?

**4. Validators**
In a `Register` model, why must the "password == confirm_password" check be a `model_validator(mode="after")` and not a `field_validator("password")`?

**5. Depends**
What's the difference between `Depends(pagination)` and `Depends(pagination())`? What does each one do?

**6. yield dependencies**
```python
def get_connection():
    connection = open_connection()
    yield connection
    connection.close()
```
The route raises `HTTPException(404)`. Is the connection closed? How do you make sure it **always** is?

**7. Hashing**
`hash_password("secret123")` returns a different string every time you call it. How can `verify_password("secret123", stored_hash)` still return `True`? Why is that a good thing?

**8. JWT**
A JWT payload is `{"sub": "2", "exp": 1767225600}`.
a) Can the user read this payload? b) Can the user change `"sub"` to `"1"` and become user 1? Why or why not? c) Why is `"sub"` a string?

**9. 401 vs 403**
For each case, which status code is correct?
a) No `Authorization` header  b) An expired token  c) A valid token from a normal user calling an admin-only route  d) A user trying to edit someone else's note

**10. CORS and middleware order**
a) Your API works in `/docs` and in curl, but a React app on `http://localhost:5173` gets *Failed to fetch*. What's the most likely cause, and why does `/docs` still work?
b) You register middleware `A` with `@app.middleware("http")`, then middleware `B` the same way. Which one sees the request first?
