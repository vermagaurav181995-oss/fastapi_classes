from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

app = FastAPI(title="04 - Forms & File Uploads")

UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_TYPES = {"image/png", "image/jpeg"}


@app.post("/login")
def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form(min_length=4)],
):
    if username == "alice" and password == "wonderland":
        return {"message": f"Welcome back, {username}!"}
    raise HTTPException(status_code=401, detail="Wrong username or password")


def check_image(file: UploadFile) -> None:
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"{file.filename}: only PNG or JPEG allowed (got {file.content_type})",
        )


async def save(file: UploadFile) -> dict:
    data = await file.read()
    safe_name = Path(file.filename or "unnamed").name
    (UPLOAD_DIR / safe_name).write_bytes(data)
    return {"filename": safe_name, "content_type": file.content_type, "size": len(data)}


@app.post("/upload")
async def upload_image(file: Annotated[UploadFile, File(description="A PNG or JPEG")]):
    check_image(file)
    return await save(file)


@app.post("/upload-many")
async def upload_many(files: Annotated[list[UploadFile], File(description="Several images")]):
    for file in files:
        check_image(file)
    return {"uploaded": [await save(file) for file in files]}
