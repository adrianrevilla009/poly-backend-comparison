# python-fastapi

The Orders endpoint in FastAPI: `main.py` (15 lines) and `requirements.txt` pinning `fastapi==0.115.6` and `uvicorn==0.34.0`.

## Goal
Implement the shared contract (`GET /orders/{id}`, `GET /health`) in FastAPI, the shortest and most Python-native version of it.

## Run it
```bash
cd python-fastapi && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn main:app --port 8080
curl -s localhost:8080/orders/7
```
Expected: `{"id":7,"customer":"c-7","total":7.5,"status":"NEW"}`. A negative id returns 400 and a non-integer id returns 422.

Not run end to end: FastAPI and uvicorn are not installed on the machine these READMEs were written on, so the server was never started. The output above is derived from reading `main.py`. Unlike the other folders, `main.py` does not read `PORT`; the port is the `--port` flag (the benchmark passes 18080 itself).

## What it proves
- The type hint `order_id: int` gives path validation for free: FastAPI rejects `/orders/x` with 422 before the handler runs.
- The explicit `HTTPException(status_code=400)` covers negative ids.
- OpenAPI docs are generated at `/docs` without extra code.

## Trade-offs
- Fastest to write, but one interpreter per worker means high memory per core, and the GIL limits CPU-bound work.
- The invalid-id status differs from the other stacks (422 for non-integers, 400 elsewhere).
- Scaling means adding uvicorn workers.

## When not to use it
- For latency-critical or CPU-heavy hot paths.
- When a small static binary is required.
