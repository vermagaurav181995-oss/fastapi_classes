# 10: Workers vs In-memory Data

## What it shows
`--workers 2` starts **two separate Python processes**. Each has its **own** `USERS` dict. A user registered on one worker doesn't exist on the other, which is why real apps keep data in a database.
Routes: `GET /pid` (`os.getpid()`), `POST /register {"username": ...}`, `GET /whoami?username=...`.
`call_many.py` sends 20 requests **at the same time** and counts the answers. Requests sent one by one often all land on the same worker, so the problem stays hidden.

## Setup
No `.env` needed.

## Run
```bash
cd 10_workers_inmemory_demo
fastapi run main.py --workers 2
```
In a second terminal:
```bash
python call_many.py /pid                              # 1. two different pids
curl -X POST localhost:8000/register -H "Content-Type: application/json" -d '{"username": "ana"}'
python call_many.py "/whoami?username=ana"            # 2. a mix of 200 and 404!
```
Compare with ONE worker: stop the server, run `fastapi run main.py`, register again, call `/whoami` again: always 200.

## Expected output
Real output from the class prep machine:
```
$ python call_many.py /pid
 16 x 200 (pid 17286)
  4 x 200 (pid 17285)

$ python call_many.py "/whoami?username=ana"
 11 x 200 (pid 17286)
  9 x 404 'ana' is unknown to worker 17285
```
ana was registered on worker 17286, so worker 17285 has never heard of her.
