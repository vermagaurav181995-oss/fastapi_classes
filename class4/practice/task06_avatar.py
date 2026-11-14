from fastapi import FastAPI, HTTPException, UploadFile

app = FastAPI(title="Task 6 - avatar upload")

ALLOWED = {"image/png", "image/jpeg"}


@app.post("/avatar")
async def upload_avatar():
    return {"todo": "implement me"}
