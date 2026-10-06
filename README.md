# poly-backend-comparison

The same small Orders endpoint written in Go, NestJS, FastAPI, Rust Axum and Scala Pekko, plus one load-test script, so you can compare how each stack looks and behaves on identical work.

## What is inside

| Folder | What it shows | Run |
| --- | --- | --- |
| [`same endpoint in go`](./same%20endpoint%20in%20go) | Reference implementation with the Go standard library only | `go build -o orders . && ./orders` |
| [`node-nestjs`](./node-nestjs) | NestJS 10 on plain Node, decorators applied by hand | `npm install && npm start` |
| [`python-fastapi`](./python-fastapi) | FastAPI served by uvicorn | `uvicorn main:app --port 8080` |
| [`rust-axum`](./rust-axum) | Axum 0.7 on Tokio | `cargo build --release && ./target/release/orders` |
| [`scala-pekko`](./scala-pekko) | Scala 3 with Pekko HTTP | `sbt run` |
| [`plus a benchmark folder`](./plus%20a%20benchmark%20folder) | Stdlib Python load test that prints one results table | `python3 "plus a benchmark folder/bench.py"` |

Every server exposes `GET /orders/{id}` and `GET /health` and reads its port from `PORT` (default 8080). The folder names `same endpoint in go` and `plus a benchmark folder` contain spaces; quote them in shell commands.

## Prerequisites

- Go 1.22 for the Go folder
- Node 22 and npm for `node-nestjs`
- Python 3.8+ on Linux for the benchmark; Python 3 with `uvicorn` and `fastapi` (see `requirements.txt`) for `python-fastapi`
- Rust with Cargo for `rust-axum`
- JDK 21 and sbt 1.10 for `scala-pekko`

You only need the toolchains of the stacks you want to compare; the benchmark skips the others.

## How to read it

Start with `same endpoint in go` to see the contract, skim the other four implementations next to it, then run `plus a benchmark folder/bench.py`. Only the NestJS folder and the benchmark were run end to end while writing these READMEs; the others are described from their code and were not built here.
