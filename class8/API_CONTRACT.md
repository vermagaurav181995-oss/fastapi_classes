# BookNest API contract

These are the API endpoints the React UI in `frontend/` calls.
Right now every call is answered by the in-browser mock (`frontend/src/api/mock/server.js`).
The FastAPI backend we build next must match this contract.

- Base URL: `http://localhost:8000`
- Auth: `Authorization: Bearer <access_token>`
- Errors use FastAPI's shape: `{"detail": "message"}`. A 422 returns `{"detail": [{"type", "loc", "msg"}]}`.
- All dates are ISO 8601 strings, and prices are numbers in USD.

## Who can call what

| Mark | Meaning | If the check fails |
|---|---|---|
| public | No token needed | n/a |
| user | Any logged-in user | `401 Not authenticated` or `401 Could not validate credentials` |
| admin | A logged-in user with `role == "admin"` | `403 Not enough permissions` |

## Endpoints

| # | Method | Path | Access | Success | Used by (page) |
|---|---|---|---|---|---|
| 1 | POST | `/auth/register` | public | 201 `UserOut` | Register |
| 2 | POST | `/auth/login` | public | 200 `Token` | Login |
| 3 | GET | `/auth/me` | user | 200 `UserOut` | App start, Layout |
| 4 | PATCH | `/users/me` | user | 200 `UserOut` | Profile |
| 5 | POST | `/users/me/password` | user | 204 | Profile |
| 6 | GET | `/books` | public | 200 `Page[BookOut]` | Books, Dashboard |
| 7 | GET | `/books/genres` | public | 200 `list[str]` | Books filter, Book form |
| 8 | GET | `/books/{book_id}` | public | 200 `BookOut` | Book detail |
| 9 | POST | `/books` | admin | 201 `BookOut` | Books ("Add book") |
| 10 | PATCH | `/books/{book_id}` | admin | 200 `BookOut` | Books and Book detail ("Edit") |
| 11 | DELETE | `/books/{book_id}` | admin | 204 | Books and Book detail ("Delete") |
| 12 | GET | `/books/{book_id}/reviews` | public | 200 `list[ReviewOut]` | Book detail |
| 13 | POST | `/books/{book_id}/reviews` | user | 201 `ReviewOut` | Book detail |
| 14 | GET | `/orders` | user | 200 `list[OrderOut]` | Orders, Dashboard |
| 15 | POST | `/orders` | user | 201 `OrderOut` | Cart ("Place order") |
| 16 | GET | `/orders/{order_id}` | user | 200 `OrderOut` | (not on a page yet) |
| 17 | POST | `/orders/{order_id}/cancel` | user (owner) | 200 `OrderOut` | Orders |
| 18 | PATCH | `/orders/{order_id}/status` | admin | 200 `OrderOut` | Orders (status dropdown) |
| 19 | GET | `/dashboard/stats` | user | 200 `UserStats` or `AdminStats` | Dashboard |

## Schemas

```text
UserOut      { id: int, email: str, full_name: str, role: "user" | "admin", created_at: datetime }
Token        { access_token: str, token_type: "bearer" }

BookOut      { id: int, title: str, author: str, genre: str, description: str, price: float,
               stock: int, published_year: int, avg_rating: float, review_count: int }
Page[T]      { items: list[T], total: int, page: int, size: int, pages: int }

ReviewOut    { id: int, book_id: int, user_id: int, user_name: str, rating: int, comment: str, created_at: datetime }

OrderItemOut { book_id: int, title: str, price: float, quantity: int }
OrderOut     { id: int, user_id: int, user_name: str, items: list[OrderItemOut], total: float,
               status: "pending" | "paid" | "shipped" | "delivered" | "cancelled", created_at: datetime }

UserStats    { role: "user", orders_count: int, pending_orders: int, total_spent: float, reviews_count: int }
AdminStats   { role: "admin", books_count: int, users_count: int, orders_count: int, pending_orders: int,
               revenue: float, low_stock: list[{ id: int, title: str, stock: int }] }
```

`avg_rating` and `review_count` are computed from the reviews. They are not stored on the book.
In an order item, `title` and `price` are a snapshot taken when the order was placed.

## Request bodies and rules

### 1. POST /auth/register
JSON body: `{ "full_name": str (1-100), "email": EmailStr, "password": str (8-128) }`
- The email is stored in lowercase. A duplicate email returns `409 Email already registered`.
- New users always get `role: "user"`.

### 2. POST /auth/login
**Form data**, not JSON (`application/x-www-form-urlencoded`). This is the `OAuth2PasswordRequestForm` format.
- Fields: `username=<email>&password=<password>`.
- A wrong email or password returns `401 Incorrect email or password`.

### 4. PATCH /users/me
JSON body: `{ "full_name"?: str (1-100) }`

### 5. POST /users/me/password
JSON body: `{ "current_password": str, "new_password": str (8-128) }`
- A wrong current password returns `400 Current password is incorrect`.

### 6. GET /books
| Query param | Type | Default | Notes |
|---|---|---|---|
| `search` | str | none | Case-insensitive match on title or author |
| `genre` | str | none | Exact match |
| `in_stock` | bool | none | `true` returns only books with `stock > 0` |
| `sort` | str | `title` | One of `title`, `price`, `rating`, `published_year`. Prefix `-` for descending, e.g. `-rating`. Anything else returns 422. |
| `page` | int | 1 | Must be ≥ 1 |
| `size` | int | 8 | Must be between 1 and 50 |

### 9. POST /books and 10. PATCH /books/{book_id}
JSON body. PATCH only changes the fields it sends.
```text
title: str (1-200)   author: str (1-120)   genre: str (1-50)   description: str (0-2000, optional)
price: float > 0     stock: int ≥ 0        published_year: int (1000 to the current year)
```
- An unknown id returns `404 Book not found`.
- A non-integer id returns 422.

### 11. DELETE /books/{book_id}
Also deletes the book's reviews. Existing orders keep their item snapshot.

### 13. POST /books/{book_id}/reviews
JSON body: `{ "rating": int (1-5), "comment"?: str (0-500) }`
- Each user can review a book once. A second review returns `409 You have already reviewed this book`.

### 14. GET /orders
- Query params: `status` (one of the 5 statuses, optional) and `limit` (int, optional).
- A user sees their own orders. An admin sees everyone's orders.
- Results are sorted newest first.

### 15. POST /orders
JSON body: `{ "items": [{ "book_id": int, "quantity": int ≥ 1 }, ...] }`. It needs at least one item.
- An unknown book returns 404.
- Not enough stock returns `400 Only N left of "Title"`, or `400 "Title" is out of stock`.
- On success:
  - stock is reduced;
  - `status` is set to `"pending"`;
  - `total` is the sum of `price × quantity`.

### 16. GET /orders/{order_id}
- Owner or admin only.
- Anyone else gets `404 Order not found`, so the API does not reveal that the order exists.

### 17. POST /orders/{order_id}/cancel
- Only the owner can cancel. Anyone else gets 403 (or 404 if they cannot see the order).
- Only `pending` orders can be cancelled. Anything else returns `400 Only pending orders can be cancelled`.
- Cancelling puts the books back into stock.

### 18. PATCH /orders/{order_id}/status
JSON body: `{ "status": "pending" | "paid" | "shipped" | "delivered" | "cancelled" }`
- Changing a cancelled order returns `400 Cancelled orders cannot be changed`.
- Setting `cancelled` puts the books back into stock.

### 19. GET /dashboard/stats
- Returns `AdminStats` for admins and `UserStats` for everyone else.
- In `AdminStats`:
  - `revenue` is the sum of non-cancelled orders;
  - `users_count` counts only users with role `user`;
  - `low_stock` lists books with `stock ≤ 3`, lowest first.

## Seed data (same as the mock)

| Email | Password | Role |
|---|---|---|
| admin@booknest.dev | admin123 | admin |
| reader@booknest.dev | reader123 | user |
| sam@booknest.dev | sam12345 | user |

The seed also includes 12 books, 8 reviews and 4 orders. See `frontend/src/api/mock/db.js`.

## CORS

The UI runs on `http://localhost:5173`, so the backend must allow that origin.
