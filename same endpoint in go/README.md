# same endpoint in go

The Orders endpoint in Go using only `net/http`: `main.go` (38 lines) and a `go.mod` that declares Go 1.22.

## Goal
Define the contract every other folder copies: `GET /orders/{id}` returns `id`, `customer`, `total` and `status`; `GET /health` returns `{"status":"UP"}`; the port comes from `PORT` and defaults to 8080.

## Run it
```bash
cd "same endpoint in go" && go build -o orders . && PORT=8080 ./orders
curl -s localhost:8080/orders/7
```
Expected: `{"id":7,"customer":"c-7","total":7.5,"status":"NEW"}`. A non-numeric or negative id returns 400 with `{"error":"bad id"}`.

Not run end to end: Go is not installed on the machine these READMEs were written on, so this folder was not compiled or executed. The output above is derived from reading `main.go`.

## What it proves
- A complete JSON service fits in one file with no third-party dependency (`go.mod` has no `require` lines).
- The order is computed from the id: customer is `c-<id % 100>`, total is `id % 1000 + 0.5`, status is always `NEW`.
- Invalid ids are rejected in the handler by `strconv.ParseInt`, not by the framework.

## Trade-offs
- Routing is the standard mux with a `/orders/` prefix, so the id is parsed by hand and every route needs its own error handling.
- Errors from `w.Write`, `Encode` and `ListenAndServe` are ignored for brevity.
- No built-in validation or dependency injection.

## When not to use it
- When the team already shares domain code on the JVM or in TypeScript and a second language costs more than it saves.
- When the service is mostly data-science or ML code that lives in Python.
