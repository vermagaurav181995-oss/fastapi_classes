# 07: Testing Middleware, CORS & Background Tasks

## What it shows
`main.py` has a timing middleware (`X-Process-Time-ms`), CORS for `http://localhost:5173`, and `POST /register`, which queues `send_welcome_email` into the `sent_emails` list.

| Test | How |
|---|---|
| timing header | check `response.headers["X-Process-Time-ms"]`, also on a 422 |
| CORS allowed | send `Origin: http://localhost:5173`, expect `access-control-allow-origin` |
| CORS blocked | `Origin: http://evil.com`: the server still answers 200, but **without** the header (the browser blocks it) |
| CORS preflight | `OPTIONS` + `Access-Control-Request-Method`: 200 allowed / 400 blocked |
| background task ran | TestClient runs background tasks **before** returning, so check `sent_emails` right after the request |
| no task on failure | a 409 queues nothing |

## Setup
No `.env` needed.

## Run
```bash
cd 07_middleware_background
pytest -v
fastapi dev main.py
```

## Expected output
```
7 passed
```
