from fastapi import FastAPI, HTTPException, UploadFile

app = FastAPI(title="Task 6 - solution")

ALLOWED = {"image/png", "image/jpeg"}


@app.post("/avatar")
async def upload_avatar(file: UploadFile):
    if file.content_type not in ALLOWED:
        raise HTTPException(status_code=400, detail="Avatar must be PNG or JPEG")
    data = await file.read()
    return {"filename": file.filename, "content_type": file.content_type, "size": len(data)}
