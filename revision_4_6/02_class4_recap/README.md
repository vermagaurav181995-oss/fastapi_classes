# 02: Class 4 Recap

## What is this?
One app with a route for every **input source** and every **dependency style** from Class 4. Routes are grouped by tag in `/docs`.

| Tag | Route | Shows |
|---|---|---|
| path | `GET /items/{item_id}` | `Path(ge=1, le=1000)`, 404 for missing items |
| query | `GET /search?q=&limit=` | `Query(min_length=2, max_length=20)`, `limit` 1–50 |
| query | `GET /filter?tag=a&tag=b` | a **list** query parameter (`Query()` is required) |
| header | `GET /client-info` | required `X-Client-Version` header, optional `User-Agent` |
| cookie | `GET /set-cookie`, `GET /read-cookie` | `response.set_cookie(...)` and `Cookie()` |
| form | `POST /login` | `Form()` fields (alice / wonderland) |
| file | `POST /upload` | `UploadFile`, PNG/JPEG only |
| body | `POST /items` | JSON body → 201 |
| body | `PATCH /items/{item_id}` | partial update with `model_dump(exclude_unset=True)` |
| body | `POST /register` | `EmailStr` + `model_validator(mode="after")`: password == confirm_password |
| dependencies | `GET /books` | a **function** dependency (`pagination`) |
| dependencies | `GET /authors` | a **class** dependency (`Annotated[Pagination, Depends()]`) |
| dependencies | `GET /reports/{year}` | a **yield** dependency (prints open/close) |
| admin | `GET /admin/stats`, `POST /admin/stats/reset` | router with `dependencies=[Depends(verify_api_key)]` |

`API_KEY` comes from `.env` (never hard-code secrets).

## Setup
```bash
cp .env.example .env     # then set API_KEY to any secret value
```

## Run it
```bash
cd 02_class4_recap
fastapi dev main.py
```

## Open in /docs
http://127.0.0.1:8000/docs. Every tag is one input source. For `/admin/*`, fill in the `x-api-key` field with your `API_KEY`. For the cookie routes, call `/set-cookie` first: the browser stores the cookie and sends it to `/read-cookie` automatically.

## TRY IT
| Request | Expected | Failing request | Expected |
|---|---|---|---|
| `GET /items/1` | 200 Pen | `GET /items/0` · `GET /items/99` | 422 · 404 |
| `GET /search?q=no` | 200 Notebook | `GET /search?q=a` · `?q=pen&limit=99` | 422 · 422 |
| `GET /filter?tag=gift&tag=kitchen` | 200 Mug, Notebook | `GET /filter` | 422 |
| `GET /client-info` + `X-Client-Version: 2.1` | 200 | no header | 422 |
| `GET /set-cookie` then `GET /read-cookie` | 200 `abc123` | `/read-cookie` without the cookie | 401 |
| `POST /login` form `username=alice&password=wonderland` | 200 | wrong password · JSON body | 401 · 422 |
| `POST /upload` with a PNG | 200 name, type, size | a `.txt` file | 400 |
| `POST /items` `{"name": "Lamp", "price": 20}` | 201 `id: 4` | `"price": -1` | 422 |
| `PATCH /items/1` `{"price": 2.0}` | 200, name kept | `PATCH /items/99` | 404 |
| `POST /register` matching passwords | 201 | same email again · passwords differ | 409 · 422 |
| `GET /books?skip=10&limit=2` | 200 Book 11, 12 | `?limit=50` | 422 |
| `GET /authors?skip=10` | 200 Author 11, 12 | `?skip=-1` | 422 |
| `GET /reports/2025` (terminal: open → close) | 200 | `GET /reports/1999` (still closes) | 404 |
| `GET /admin/stats` + `X-API-Key: <your key>` | 200 | no key / wrong key | 403 |

All requests are also in [`../test_requests.http`](../test_requests.http).
