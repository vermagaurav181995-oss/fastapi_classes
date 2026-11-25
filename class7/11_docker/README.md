# 11: Docker

## What it shows
The Class 6 bookstore with auth, packaged as a container image.
- `Dockerfile`: `python:3.12-slim` → copy `requirements.txt` **first** and install (a cached layer) → copy the code → `CMD ["fastapi", "run", "main.py", "--port", "8000"]`
- `.dockerignore`: keeps `.env`, `.venv`, `__pycache__`, `.git`, `.pytest_cache` out of the image (secrets are passed at **runtime** with `--env-file`)
- `docker-compose.yml`: the same thing with `docker compose up`

## Setup
```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # paste as SECRET_KEY in .env
```

## Run
```bash
cd 11_docker
docker build -t bookstore .
docker run --rm --env-file .env -p 8000:8000 bookstore
# open http://localhost:8000/docs     (Ctrl+C to stop)

# or, with Compose:
docker compose up --build
docker compose down
```
Useful: `docker ps` (running containers) · `docker logs <id>` · `docker exec -it <id> sh` (a shell inside) · `docker images` (image sizes)

## Expected output
```
$ docker build -t bookstore .
 => [2/5] WORKDIR /app
 => [3/5] COPY requirements.txt .
 => [4/5] RUN pip install --no-cache-dir -r requirements.txt
 => [5/5] COPY . .
 => naming to docker.io/library/bookstore

$ docker run --rm --env-file .env -p 8000:8000 bookstore
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```
`GET http://localhost:8000/books` → the 3 books. The image is about 340 MB. Change only `main.py` and rebuild: step 4 (`pip install`) says **CACHED**.
