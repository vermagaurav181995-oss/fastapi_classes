# Revision: Class 4 + Class 6

Revision examples for **Requests, Responses & Dependency Injection** (Class 4) and **Authentication, Security & Middleware** (Class 6).
No database: all data lives in Python dicts. Each numbered folder is a standalone app.

## Setup (once)
Requires **Python 3.11+**.
```bash
cd revision_4_6
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Secrets
Folders with a `.env.example` need a `.env` next to it:
```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"   # paste as SECRET_KEY (or API_KEY in 02)
```
`.env` is git-ignored. Only `.env.example` is committed.

## Examples

| # | What | .env? | Run (from `revision_4_6/`) |
|---|---|---|---|
| 01 | The request journey: middleware → CORS → auth chain → validation → route → background task → cleanup | yes | `cd 01_request_journey && fastapi dev main.py` |
| 02 | Class 4 recap: every input source + every dependency style | yes (`API_KEY`) | `cd 02_class4_recap && fastapi dev main.py` |
| 03 | Class 6 recap: register, login, me, roles, CORS, middleware, background email, lifespan | yes | `cd 03_class6_recap && fastapi dev main.py` |
| 04 | Spot the bug: 9 bugs, each with `buggy/` + `fixed/` | only bug 08 `fixed/` | `cd 04_spot_the_bug/bug_01_tags_filter/buggy && fastapi dev main.py` |
| 05 | Notes API challenge: starter | yes | `cd 05_notes_api_challenge/starter && fastapi dev main.py` |
| 05 | Notes API challenge: solution | yes | `cd 05_notes_api_challenge/solution && fastapi dev main.py` |
| 06 | Quiz | no | open `06_quiz/quiz.md`, answers in `06_quiz/answers.md` |

### Spot the bug

| Bug | Run the buggy version | Run the fixed version |
|---|---|---|
| 01 tags filter | `cd 04_spot_the_bug/bug_01_tags_filter/buggy && fastapi dev main.py` | `.../bug_01_tags_filter/fixed` |
| 02 partial update | `cd 04_spot_the_bug/bug_02_partial_update/buggy && fastapi dev main.py` | `.../bug_02_partial_update/fixed` |
| 03 Depends called | `cd 04_spot_the_bug/bug_03_depends_called/buggy && fastapi dev main.py` | `.../bug_03_depends_called/fixed` |
| 04 connection cleanup | `cd 04_spot_the_bug/bug_04_connection_cleanup/buggy && fastapi dev main.py` | `.../bug_04_connection_cleanup/fixed` |
| 05 plain password | `cd 04_spot_the_bug/bug_05_plain_password/buggy && fastapi dev main.py` | `.../bug_05_plain_password/fixed` |
| 06 login messages | `cd 04_spot_the_bug/bug_06_login_messages/buggy && fastapi dev main.py` | `.../bug_06_login_messages/fixed` |
| 07 admin 401 | `cd 04_spot_the_bug/bug_07_admin_401/buggy && fastapi dev main.py` | `.../bug_07_admin_401/fixed` |
| 08 secret in code | `cd 04_spot_the_bug/bug_08_secret_in_code/buggy && fastapi dev main.py` | `.../bug_08_secret_in_code/fixed` (needs `.env`) |
| 09 CORS origin | `cd 04_spot_the_bug/bug_09_cors_origin/buggy && fastapi dev main.py` + `cd 04_spot_the_bug/bug_09_cors_origin/frontend && python -m http.server 5173` | `.../bug_09_cors_origin/fixed` |

Each bug's README describes the symptom only. The answers are in `04_spot_the_bug/ANSWERS.md`.

## Other files
- `test_requests.http`: requests for the VS Code **REST Client** extension (01, 02, 03 and the notes solution). Log in once per section; the token is reused through `@token` variables.
- `test_revision.py`: automated tests (no `.env` needed, test secrets come from environment variables):
  ```bash
  pytest -v test_revision.py
  ```
