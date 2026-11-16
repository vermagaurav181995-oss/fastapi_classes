"""Solution 12: logging middleware printing method, path, status and time."""

import time

from fastapi import FastAPI, HTTPException, Request

app = FastAPI(title="Task 12 - solution")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    ms = (time.perf_counter() - start) * 1000
    response.headers["X-Process-Time-ms"] = f"{ms:.2f}"
    print(f"{request.method} {request.url.path} -> {response.status_code} ({ms:.2f} ms)")
    return response


@app.get("/hello")
def hello():
    return {"message": "hi"}


@app.get("/fail")
def fail():
    raise HTTPException(status_code=404, detail="Nothing here")

# terminal: "GET /hello -> 200 (0.31 ms)"   "GET /fail -> 404 (0.20 ms)"
