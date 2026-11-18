from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def hash_password(plain: str) -> str:
    raise NotImplementedError


def verify_password(plain: str, hashed: str) -> bool:
    raise NotImplementedError


def create_access_token(user_id: int) -> str:
    raise NotImplementedError


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    raise NotImplementedError


CurrentUser = Annotated[dict, Depends(get_current_user)]
