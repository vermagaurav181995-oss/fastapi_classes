# 13: WebSocket Chat

## What it shows
- `chat.py`: a `ConnectionManager` (connect / disconnect / broadcast) and `@router.websocket("/ws/chat/{username}")`, which loops on `receive_text()` and catches `WebSocketDisconnect`.
- `main.py`: serves `static/index.html` (a tiny chat page) at `/`.
- `test_chat.py`: `client.websocket_connect(...)`, `send_text`, `receive_json`; one client gets its own message, two clients both get a broadcast, and a disconnect removes the connection.

## Setup
No `.env` needed.

## Run
```bash
cd 13_websocket_chat
fastapi dev main.py        # open http://127.0.0.1:8000 in TWO tabs, join as two names, chat
pytest -v
```

## Expected output
In the browser: both tabs show `system: ben joined the chat`, then `ana: hi`; closing a tab shows `system: ben left the chat`.
Tests: `4 passed`. (WebSocket routes don't appear in `/docs`.)
