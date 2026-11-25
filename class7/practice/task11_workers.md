# Task 11: Workers and in-memory data

Use `../10_workers_inmemory_demo`.

1. Run `fastapi run main.py --workers 2` and call `/pid` many times (`python call_many.py /pid`).
   *TODO: how many different pids did you see? Why?*

2. `POST /register {"username": "ana"}`, then `python call_many.py "/whoami?username=ana"`.
   *TODO: what happened, and why?*

3. *TODO: explain in 3–5 sentences why in-memory dicts break with several workers (or several servers), and what real apps use instead.*

4. *TODO: why does the same app work fine with `fastapi dev`?*
