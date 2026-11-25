# Solution 11: Workers and in-memory data

1. **Different pids.** `--workers 2` starts **two separate Python processes**, each running its own copy of the app. The OS hands each incoming request to one of them, so `/pid` answers with two different process ids. (Concurrent requests spread more evenly, which is why `call_many.py` sends 20 at once.)

2. **`/whoami` is sometimes 200, sometimes 404.** `USERS` is a dict **inside a process**. The register request was handled by one worker, so only that worker's dict has `ana`. Requests that land on the other worker get `404 'ana' is unknown to worker <pid>`. In our run: 11 × 200, 9 × 404.

3. **Why it breaks:** every worker (and every server, when you scale to several machines, or after a restart or redeploy) has its own memory, and memory isn't shared or kept. Data stored in Python dicts is therefore split between processes and lost on restart. Real apps keep state **outside** the app processes, in a database (PostgreSQL, MySQL, SQLite for small apps) or a shared store like Redis, so that every worker reads and writes the same data.

4. **`fastapi dev` works** because it runs a **single** process (plus auto-reload), so there is only one `USERS` dict. Even then, the data is lost every time the server reloads.
