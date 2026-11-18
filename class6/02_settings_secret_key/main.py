from fastapi import FastAPI, HTTPException

from config import settings

app = FastAPI(title="02 - Settings & SECRET_KEY")


@app.get("/settings")
def show_settings():
    return {
        "algorithm": settings.algorithm,
        "access_token_expire_minutes": settings.access_token_expire_minutes,
        "database_url": settings.database_url,
        "secret_key_length": len(settings.secret_key),
        "secret_key_preview": settings.secret_key[:4] + "...",
    }


@app.get("/settings/{name}")
def show_one_setting(name: str):
    public = {"algorithm", "access_token_expire_minutes", "database_url"}
    if name not in public:
        raise HTTPException(status_code=404, detail=f"No public setting called '{name}'")
    return {name: getattr(settings, name)}
