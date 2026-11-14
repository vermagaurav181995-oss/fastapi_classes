from typing import Annotated

from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="Task 5 - solution")


@app.get("/whoami")
def whoami(user_agent: Annotated[str | None, Header()] = None):
    if not user_agent:
        raise HTTPException(status_code=400, detail="No User-Agent header sent")
    return {"user_agent": user_agent}
