from typing import Annotated

import jwt
from fastapi import Depends, FastAPI

from common import CurrentUser, login_router, oauth2_scheme, seed_demo_users, settings

seed_demo_users()
app = FastAPI(title="Task 7 - solution")
app.include_router(login_router)


@app.get("/auth/me")
def read_me(user: CurrentUser):
    return {"email": user.email}


@app.get("/auth/token-info")
def token_info(user: CurrentUser, token: Annotated[str, Depends(oauth2_scheme)]):
    exp = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])["exp"]
    return {"expire_minutes_setting": settings.access_token_expire_minutes, "exp": exp}
