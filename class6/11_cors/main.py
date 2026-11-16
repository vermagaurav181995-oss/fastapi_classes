"""
11 - CORS (Cross-Origin Resource Sharing)
=========================================
A page served from http://localhost:5173 that calls http://127.0.0.1:8000 is
a CROSS-ORIGIN request. The BROWSER blocks the response unless the API says
"I allow that origin" with an  Access-Control-Allow-Origin  header.
CORSMiddleware adds those headers (and answers the OPTIONS "preflight" request).
CORS is a BROWSER rule: curl, Postman and /docs are not affected.

Setup:  cp .env.example .env
Run:    fastapi dev main.py
Then:   cd frontend && python -m http.server 5173  ->  open http://localhost:5173
Demo user (created on startup): student@example.com / password123
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from database import Base, SessionLocal, engine
from models import User
from routers import auth
from security import hash_password

Base.metadata.create_all(bind=engine)
with SessionLocal() as db:  # seed one demo user for the frontend
    if db.scalar(select(User).where(User.email == "student@example.com")) is None:
        db.add(User(email="student@example.com", hashed_password=hash_password("password123")))
        db.commit()

app = FastAPI(title="11 - CORS")

# Exact origins: scheme + host + port. "localhost" and "127.0.0.1" are DIFFERENT origins!
ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite / our tiny frontend
    "http://localhost:3000",  # React / Next.js dev servers
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # never ["*"] together with credentials in production
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PATCH, DELETE, ...
    allow_headers=["*"],  # e.g. Authorization, Content-Type
)

app.include_router(auth.router)


# ---------------------------------------------------------------------------
# TRY IT
# ---------------------------------------------------------------------------
# Browser: open http://localhost:5173, click "Log in & call /auth/me"
#   -> the page shows {"email": "student@example.com", ...}
# Allowed origin:   GET /auth/me  header Origin: http://localhost:5173
#   -> response has  access-control-allow-origin: http://localhost:5173
# Preflight:        OPTIONS /auth/login  Origin: http://localhost:5173
#                   Access-Control-Request-Method: POST  -> 200
#
# These should FAIL:
# Remove "http://localhost:5173" from ALLOWED_ORIGINS, reload the page, click again
#   -> browser console: "blocked by CORS policy: No 'Access-Control-Allow-Origin' header"
# OPTIONS /auth/login  Origin: http://evil.example  -> 400 "Disallowed CORS origin"
# GET /auth/me without a token                      -> 401 (CORS headers are still added)
