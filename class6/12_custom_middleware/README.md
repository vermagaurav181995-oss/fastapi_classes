# 12: Custom Middleware

## What is this?
`@app.middleware("http")` wraps every request: code before `await call_next(request)` runs before the route, and code after it runs after. `time_request` adds `X-Process-Time-ms` and prints `METHOD path -> status (ms)`. `add_request_id` adds `X-Request-ID` (a uuid4). **The middleware registered last runs first** (it's the outermost layer), and the terminal shows the order. No `.env` is needed.

## Setup
No `.env` needed for this example.

## Run it
```bash
cd 12_custom_middleware
fastapi dev main.py
```

## Open in /docs
http://127.0.0.1:8000/docs. Call any route and look at the **Response headers** box (`x-process-time-ms`, `x-request-id`), then at the terminal.

## TRY IT
1. `GET /` → 200 + both headers; terminal shows request-id → timing → route → timing → request-id
2. `GET /slow` → `x-process-time-ms` is about 500
3. ❌ `GET /items/99` → 404, still with both headers
4. ❌ `GET /items/abc` → 422

All requests are also in [`../test_requests.http`](../test_requests.http).
