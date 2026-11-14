from fastapi import FastAPI, Query

app = FastAPI(title="Task 4 - list query params")


@app.get("/filter")
def filter_genres():
    return {"todo": "implement me"}
