from typing import Annotated

from fastapi import Header, HTTPException, status

API_KEY = "super-secret-key"


def verify_api_key(x_api_key: Annotated[str | None, Header()] = None) -> None:
    if x_api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or missing API key")
