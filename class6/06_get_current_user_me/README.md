# 06: get_current_user & /auth/me

## What is this?
`OAuth2PasswordBearer(tokenUrl="auth/login")` reads the `Authorization: Bearer` header. `get_current_user` decodes the token, loads the user from the DB and checks `is_active`. `CurrentUser = Annotated[User, Depends(get_current_user)]` protects any route that uses it.

## Setup
```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # paste the output as SECRET_KEY in .env
```

## Run it
```bash
cd 06_get_current_user_me
fastapi dev main.py
```

## Open in /docs
http://127.0.0.1:8000/docs. **Authorize button:** click **Authorize** (top right, padlock icon). Type your **email** in `username`, your password in `password`, leave `client_id` / `client_secret` empty, and click **Authorize**, then **Close**. Swagger calls `POST /auth/login` for you and sends `Authorization: Bearer <token>` on every request. Routes with a padlock need it. Then call **GET /auth/me**. Click **Logout** in the Authorize dialog and call it again to get a 401.

## TRY IT
1. Register, then log in → token
2. `GET /auth/me` with `Authorization: Bearer <token>` → 200 your user
3. ❌ no token → 401 `Not authenticated`
4. ❌ `Bearer fake.token.x` → 401 `Could not validate credentials`
5. ❌ expired token: set `ACCESS_TOKEN_EXPIRE_MINUTES=1` in `.env`, log in, wait 1 minute → 401

All requests are also in [`../test_requests.http`](../test_requests.http).
