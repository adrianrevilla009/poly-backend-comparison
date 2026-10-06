# plus a benchmark folder

`bench.py`, a stdlib-only Python script that builds, starts and load-tests each implementation and prints a Markdown table.

## Goal
Run the same load against every implementation and record throughput, latency, memory, build time and lines of code from one run, so the numbers are comparable on one machine.

## Run it
```bash
python3 "plus a benchmark folder/bench.py" --seconds 5 --threads 16
python3 "plus a benchmark folder/bench.py" node-nestjs
```
Expected: a table with one row per folder, such as this real run of the NestJS folder (3 s, 16 threads, WSL2):

    | node-nestjs | 1616 | 9.41 / 23.24 | 130 | 2.1 | 28 |

A folder whose tool (`go`, `npm`, `uvicorn`, `cargo`, `sbt`) is missing gets a `skipped` row. Servers listen on port 18080 and need Linux, because memory is read from `/proc`.

Only the NestJS row was measured. Go, FastAPI, Rust and Scala were skipped because their toolchains are not installed here, so there are no numbers for them and no comparison between stacks has been made.

## What it proves
- Every stack gets the same steps: build, wait for `/health`, 1 s warm-up, then timed `GET /orders/{id}` with keep-alive connections.
- The columns are req/s, p50 / p99 in ms, RSS in MB (server plus child processes), build seconds and lines of source counted from the globs in `IMPLS`.
- Failed requests are counted and printed as `errors=N` instead of being hidden.

## Trade-offs
- The client is a threaded Python script, so it tops out at a few thousand req/s and will understate fast servers such as Go and Rust. Use `wrk`, `hey` or k6 for serious numbers.
- Build time for NestJS is `npm install` only, and the FastAPI build step is a no-op.
- RSS is taken once after the run, JVM numbers depend on heap flags, and a single short run has no confidence interval.

## When not to use it
- For capacity planning or choosing a production language; real services are dominated by the database and network.
- For comparing numbers across different machines.
