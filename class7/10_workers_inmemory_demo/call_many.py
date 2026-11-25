import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

import httpx

BASE_URL = "http://127.0.0.1:8000"
path = sys.argv[1] if len(sys.argv) > 1 else "/pid"


def call(_: int) -> str:
    response = httpx.get(BASE_URL + path)
    pid = response.json().get("pid") or response.json().get("answered_by_pid") or "?"
    return f"{response.status_code} (pid {pid})" if response.status_code == 200 else f"{response.status_code} {response.json()['detail']}"


with ThreadPoolExecutor(max_workers=10) as pool:
    results = Counter(pool.map(call, range(20)))

for result, count in results.most_common():
    print(f"{count:3} x {result}")
