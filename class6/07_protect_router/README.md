# 07: Protecting a Whole Router

## What is this?
`APIRouter(dependencies=[Depends(get_current_user)])` protects **every** route in `routers/books.py` at once. `routers/public.py` has no protection, for comparison. `POST /books` also asks for `CurrentUser` because it needs the user's email (FastAPI still runs the dependency only once).

```
07_protect_router/
├── main.py
├── config.py  database.py  models.py  schemas.py  security.py
└── routers/  auth.py  books.py (protected)  public.py (open)
```

## Setup
```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # paste the output as SECRET_KEY in .env
```

## Run it
```bash
cd 07_protect_router
fastapi dev main.py
```

## Open in /docs
http://127.0.0.1:8000/docs. **Authorize button:** click **Authorize** (top right, padlock icon). Type your **email** in `username`, your password in `password`, leave `client_id` / `client_secret` empty, and click **Authorize**, then **Close**. Swagger calls `POST /auth/login` for you and sends `Authorization: Bearer <token>` on every request. Routes with a padlock need it. Every `/books` route shows a padlock; `/public` routes don't.

## TRY IT
1. `GET /public/info` → 200 (no token)
2. Register + log in → token
3. `GET /books` + token → 200 · `POST /books` `{"title": "Neuromancer"}` + token → 201 `added_by: ada@example.com`
4. ❌ `GET /books` (no token) → 401 · bad token → 401
5. ❌ `GET /books/99` + token → 404

All requests are also in [`../test_requests.http`](../test_requests.http).
