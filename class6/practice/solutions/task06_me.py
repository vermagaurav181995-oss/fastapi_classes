"""Solution 6: GET /auth/me with CurrentUser."""

from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from common import DbSession, User, login_router, seed_demo_users, settings

seed_demo_users()
app = FastAPI(title="Task 6 - solution")
app.include_router(login_router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: DbSession) -> User:
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user = db.get(User, int(payload["sub"]))
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise error
    if user is None or not user.is_active:
        raise error
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


@app.get("/auth/me")
def read_me(user: CurrentUser):
    return {"id": user.id, "email": user.email, "role": user.role}

# no token -> 401 "Not authenticated"   fake token -> 401   real token -> 200
