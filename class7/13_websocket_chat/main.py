from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from chat import router as chat_router

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="13 - WebSocket Chat")
app.include_router(chat_router)


@app.get("/", include_in_schema=False)
def chat_page():
    return FileResponse(STATIC_DIR / "index.html")
