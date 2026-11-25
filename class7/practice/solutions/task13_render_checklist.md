# Solution 13: Deploy to Render (checklist)

## Before deploying
- [x] `requirements.txt` contains `fastapi[standard]` and `pydantic-settings` (plus `pyjwt` / `pwdlib[argon2]` if the app uses auth)
- [x] `.gitignore` keeps `.env`, `.venv/` and `__pycache__/` out of GitHub
- [x] Start command: `fastapi run main.py --port $PORT` (`run`, not `dev`; Render picks the port)
- [x] The app reads `SECRET_KEY` from the environment through pydantic-settings, never from the code
- [x] `GET /health` returns `{"status": "ok"}`
- [x] Tests pass locally: `pytest`

## On Render
- [x] New → Web Service → connect the GitHub repo (set **Root Directory** if the app is in a subfolder)
- [x] Runtime: Python 3 · Build command: `pip install -r requirements.txt`
- [x] Environment variables: `SECRET_KEY` (click *Generate*), `ENVIRONMENT=production`, `ALLOWED_ORIGINS=["https://myapp.com"]`, `PYTHON_VERSION=3.12.8`
- [x] My URL: `https://<service-name>.onrender.com`

## After deploying
- [x] `GET /health` → `200 {"status": "ok"}`
- [x] `GET /docs` → `404`, because docs are hidden when `ENVIRONMENT=production`
- [x] The logs show `GET /health 200`, with no errors at startup
- [x] Free plan: after **15 minutes without traffic** the service spins down; the next request wakes it up, which takes up to about a minute. In-memory data is lost every time.
