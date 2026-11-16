"""
07 - Protecting a whole router
==============================
routers/auth.py    -> register / login / me   (from examples 03-06)
routers/public.py  -> open to everyone
routers/books.py   -> APIRouter(dependencies=[Depends(get_current_user)])
                      every /books route needs a valid token

Setup:  cp .env.example .env
Run:    fastapi dev main.py         Docs: http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI

from database import Base, engine
from routers import auth, books, public

Base.metadata.create_all(bind=engine)

app = FastAPI(title="07 - Protect a Router")
app.include_router(auth.router)
app.include_router(public.router)
app.include_router(books.router)

# In /docs, protected routes show a padlock icon. Click "Authorize" once,
# log in with your email + password, and /docs sends the token for you.


# ---------------------------------------------------------------------------
# TRY IT
# ---------------------------------------------------------------------------
# GET  /public/info                         -> 200 (no token needed)
# POST /auth/register {"email": "ada@example.com", "password": "supersecret"} -> 201
# POST /auth/login    FORM username=ada@example.com&password=supersecret     -> 200 {token}
# GET  /books         Authorization: Bearer <token> -> 200 [Dune, 1984]
# POST /books {"title": "Neuromancer"} + token     -> 201 {..., "added_by": "ada@example.com"}
#
# These should FAIL:
# GET  /books         (no token)                -> 401 "Not authenticated"
# GET  /books/1       Authorization: Bearer bad  -> 401 "Could not validate credentials"
# POST /books         (no token)                -> 401 (the router check runs first)
# GET  /books/99      + token                   -> 404 "Book not found"
