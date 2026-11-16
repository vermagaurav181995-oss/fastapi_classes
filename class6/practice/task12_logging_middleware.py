"""
Task 12 - Logging middleware
Print one line per request:   GET /hello -> 200 (0.31 ms)
Bonus: add an X-Process-Time-ms response header.
Run:  fastapi dev task12_logging_middleware.py   (watch the terminal)
"""

import time  # noqa: F401

from fastapi import FastAPI, HTTPException, Request  # noqa: F401

app = FastAPI(title="Task 12 - logging middleware")


# TODO: @app.middleware("http")
# TODO: async def log_requests(request: Request, call_next):
#           start timer -> response = await call_next(request) -> stop timer
#           print method, path, status code, milliseconds -> return response


@app.get("/hello")
def hello():
    return {"message": "hi"}


@app.get("/fail")
def fail():
    raise HTTPException(status_code=404, detail="Nothing here")
