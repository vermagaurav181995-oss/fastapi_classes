# 12: Deploy to Render

## What it shows
A small deploy-ready app (its own `requirements.txt`, `.gitignore`, `Dockerfile`, `.dockerignore`, `render.yaml`) with `GET /health` → `{"status": "ok"}`, settings from env vars, CORS from `ALLOWED_ORIGINS`, and docs hidden in production.

## Setup
```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # paste as SECRET_KEY in .env
```

## Run
### Locally first
```bash
cd 12_deploy_render
fastapi dev main.py            # http://127.0.0.1:8000/health
```

### Step-by-step on Render
1. **Push to GitHub.** Make sure `.env` is *not* committed (`git status` must not list it).
2. Sign in at **render.com** with GitHub → **New +** → **Web Service** → pick your repository.
3. If the app is in a subfolder, set **Root Directory** (e.g. `class7/12_deploy_render`).
4. **Runtime:** Python 3 · **Build Command:** `pip install -r requirements.txt` · **Start Command:** `fastapi run main.py --port $PORT` · **Instance type:** Free
5. **Environment Variables:**
   | Key | Value |
   |---|---|
   | `SECRET_KEY` | click **Generate** |
   | `ENVIRONMENT` | `production` |
   | `ALLOWED_ORIGINS` | `["https://your-frontend.com"]` (JSON list) |
   | `PYTHON_VERSION` | `3.12.8` |
6. Under **Advanced**, set the **Health Check Path** to `/health`.
7. Click **Create Web Service**, then watch the **Logs**: build → `Uvicorn running on http://0.0.0.0:10000` → *Your service is live*.

**Or use the Blueprint:** **New +** → **Blueprint** → select the repo; Render reads `render.yaml` and fills in everything above (`SECRET_KEY` is generated automatically).

**Free tier:** the service **spins down after 15 minutes without traffic**. The next request wakes it up, which takes up to about a minute. Memory is wiped on every restart or deploy, so in-memory data disappears.

### Post-deploy checklist
- [ ] `https://<your-app>.onrender.com/health` → `{"status": "ok"}`
- [ ] `GET /` shows `"environment": "production"`
- [ ] `/docs` → 404 (hidden in production)
- [ ] The logs show no errors at startup (a missing `SECRET_KEY` shows `ValidationError`)
- [ ] `.env` is not in the GitHub repo; secrets live only in Render's Environment tab
- [ ] A frontend on an allowed origin can call the API; other origins are blocked
- [ ] Pushing a new commit triggers an automatic redeploy


## Expected output
Locally: `GET /health` → `{"status": "ok"}`, `GET /` → `{"message": "Bookstore API is running", "environment": "development"}`.
On Render: the same `/health`, `"environment": "production"`, and `/docs` → 404.
