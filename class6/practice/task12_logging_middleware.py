import time

from fastapi import FastAPI, HTTPException, Request

app = FastAPI(title="Task 12 - logging middleware")


@app.get("/hello")
def hello():
    return {"message": "hi"}


@app.get("/fail")
def fail():
    raise HTTPException(status_code=404, detail="Nothing here")
