"""
12 - Custom middleware
======================
Middleware wraps EVERY request:   code before call_next -> route -> code after.

    request  ->  request_id MW  ->  timing MW  ->  route
    response <-  request_id MW  <-  timing MW  <-  route

Order rule: the middleware registered LAST is the OUTERMOST, so it runs FIRST.
Here `add_request_id` is defined after `time_request`, so it runs first.
Watch the terminal to see the order. (No .env needed for this example.)

Run (from inside this folder):  fastapi dev main.py
"""

import asyncio
import time
import uuid

from fastapi import FastAPI, HTTPException, Request

app = FastAPI(title="12 - Custom Middleware")


@app.middleware("http")
async def time_request(request: Request, call_next):
    print("  [timing]     before route")
    start = time.perf_counter()
    response = await call_next(request)  # <- runs the route (and inner middleware)
    ms = (time.perf_counter() - start) * 1000
    response.headers["X-Process-Time-ms"] = f"{ms:.2f}"
    print("  [timing]     after route")
    print(f"{request.method} {request.url.path} -> {response.status_code} ({ms:.2f} ms)")
    return response


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id  # routes can read it from request.state
    print(f"[request-id] start {request_id}")
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    print("[request-id] end")
    return response


ITEMS = {1: "Pen", 2: "Mug"}


@app.get("/")
def root(request: Request):
    print("      [route] running")
    return {"message": "Check the response headers!", "request_id": request.state.request_id}


@app.get("/slow")
async def slow():
    await asyncio.sleep(0.5)  # X-Process-Time-ms will be ~500
    return {"message": "That took a while"}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in ITEMS:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, "name": ITEMS[item_id]}


# ---------------------------------------------------------------------------
# TRY IT  (look at the response HEADERS and the terminal)
# ---------------------------------------------------------------------------
# GET /       -> 200, headers  x-process-time-ms: 0.85   x-request-id: 3f2c...
#    terminal:  [request-id] start 3f2c...
#                 [timing]     before route
#                     [route] running
#                 [timing]     after route
#               GET / -> 200 (0.85 ms)
#               [request-id] end
# GET /slow   -> 200, x-process-time-ms is about 500
#
# These should FAIL, yet still get BOTH headers (middleware wraps errors too):
# GET /items/99  -> 404 "Item not found"
# GET /items/abc -> 422
