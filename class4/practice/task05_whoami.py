from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="Task 5 - whoami")


@app.get("/whoami")
def whoami():
    return {"todo": "implement me"}
