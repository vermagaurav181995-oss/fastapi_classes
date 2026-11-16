# 11: CORS

## What is this?
A page on `http://localhost:5173` calling the API on `http://127.0.0.1:8000` is **cross-origin**. The **browser** blocks the response unless the API sends `Access-Control-Allow-Origin`. `CORSMiddleware` allows `http://localhost:5173` and `http://localhost:3000`. CORS only affects browsers: curl, Postman and /docs never see it.

Demo user (created on startup): `student@example.com` / `password123`

## Setup
```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # paste the output as SECRET_KEY in .env
```

In a **second terminal**, serve the frontend:
```bash
cd frontend
python -m http.server 5173
```
Open **http://localhost:5173** (use `localhost`, not `127.0.0.1`: they are different origins).

## Run it
```bash
cd 11_cors
fastapi dev main.py
```

## Open in /docs
http://127.0.0.1:8000/docs. /docs works with or without CORS (same origin). **Authorize button:** click **Authorize** (top right, padlock icon). Type your **email** in `username`, your password in `password`, leave `client_id` / `client_secret` empty, and click **Authorize**, then **Close**. Swagger calls `POST /auth/login` for you and sends `Authorization: Bearer <token>` on every request. Routes with a padlock need it.

## TRY IT
1. Open http://localhost:5173 and click **Log in & call /auth/me** → your user is shown
2. DevTools → Network → `me`: the response has `access-control-allow-origin: http://localhost:5173`
3. ❌ **Show the CORS error:** remove `"http://localhost:5173"` from `ALLOWED_ORIGINS` in `main.py`, save (the server reloads), and click again → *Request blocked*; the console shows `blocked by CORS policy: No 'Access-Control-Allow-Origin' header`. Put it back afterwards.
4. ❌ `OPTIONS /auth/login` with `Origin: http://evil.example` → 400 `Disallowed CORS origin`

All requests are also in [`../test_requests.http`](../test_requests.http).
