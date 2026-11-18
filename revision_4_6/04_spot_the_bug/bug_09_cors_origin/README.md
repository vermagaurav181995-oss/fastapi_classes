# Bug 09: The frontend can't load the books

## Symptom
The API works fine in `/docs`, in curl and in Postman, but the new frontend shows *Request failed: TypeError: Failed to fetch*.

## Reproduce it
1. Start the API (below).
2. In a second terminal: `cd bug_09_cors_origin/frontend && python -m http.server 5173`
3. Open **http://localhost:5173** and click *Load books from the API*.
4. Open DevTools (F12) → **Console** and **Network**, and read the error. Which origin is the page on?

## Expected behavior
Clicking the button shows `["Dune", "1984", "Neuromancer"]`.

## Run it
```bash
cd bug_09_cors_origin/buggy
fastapi dev main.py
```
When you think you've found the bug, compare with `fixed/` (same command, from `bug_09_cors_origin/fixed`) and check `../ANSWERS.md`.
