# 02: TestClient Basics

## What it shows
`TestClient(app)` sends real HTTP requests to your app in memory, with no server running.

| Test | Shows |
|---|---|
| `test_get_book_returns_200` / `..._404` / `..._422` / `test_create_book_returns_201` | checking `status_code` and `json()` |
| `test_send_json_body` | `json=` → JSON body |
| `test_send_query_params` | `params=` → `?q=du` |
| `test_send_headers` | `headers=` |
| `test_send_form_data` | `data=` → form body (like a login form) |
| `test_upload_a_file` | `files={"file": (name, bytes, content_type)}` |
| `test_send_cookies` | `client.cookies.set(...)` |

## Setup
No `.env` needed.

## Run
```bash
cd 02_testclient_basics
pytest -v                  # the tests
fastapi dev main.py        # the app, if you want to click around in /docs
```

## Expected output
```
10 passed
```
