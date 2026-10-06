# rust-axum

The Orders endpoint in Rust with Axum 0.7 on Tokio: `src/main.rs` (30 lines) and a `Cargo.toml` that pins every dependency with `=`.

## Goal
Implement the shared contract (`GET /orders/{id}`, `GET /health`, port from `PORT`, default 8080) with typed handlers and no runtime beyond Tokio.

## Run it
```bash
cd rust-axum && cargo build --release && PORT=8080 ./target/release/orders
curl -s localhost:8080/orders/7
```
Expected: `{"id":7,"customer":"c-7","total":7.5,"status":"NEW"}`. A negative id returns 400; a non-integer id is rejected by the extractor, also with a 4xx.

Not run end to end: the Rust toolchain is not installed on the machine these READMEs were written on, so this folder was never compiled. The output above is derived from reading `src/main.rs`.

## What it proves
- `Path<i64>` makes Axum parse and reject the id before `order` in `src/main.rs` is called.
- Responses are serialized from a typed `Order` struct with `serde`, so field names and types are checked at compile time.
- `Cargo.toml` pins axum 0.7.9, tokio 1.42.0, serde 1.0.216 and serde_json 1.0.133.

## Trade-offs
- Dependencies compile from source, so a cold release build is slow.
- Ownership and async types make even a small handler more demanding to write.
- The 400 for a negative id has no body, unlike the Go and Scala versions.

## When not to use it
- For CRUD services where developer speed matters more than per-request cost.
- When the team has no Rust experience and no memory or latency pressure.
