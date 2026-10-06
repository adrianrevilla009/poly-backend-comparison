# node-nestjs

The Orders endpoint in NestJS 10 on plain Node: `main.js` (28 lines) and `package.json` with exact versions.

## Goal
Implement the shared contract (`GET /orders/{id}`, `GET /health`, port from `PORT`, default 8080) with NestJS, so its structure and cost can be compared with the other stacks.

## Run it
```bash
cd node-nestjs && npm install && PORT=8080 npm start
curl -s localhost:8080/orders/7
```
Expected: `{"id":7,"customer":"c-7","total":7.5,"status":"NEW"}`; `/orders/x` returns 400 and `/health` returns `{"status":"UP"}`.

The server was started and load-tested through `plus a benchmark folder/bench.py` (about 1,600 req/s, 130 MB RSS in a 3 s run). The individual curl calls for 400 and `/health` were not re-run separately; they follow from `main.js`.

## What it proves
- A Nest module, controller and route parameter work without TypeScript: `main.js` applies `Controller`, `Get`, `Param` and `Module` as plain function calls, so there is no build step.
- A bad id is turned into a 400 by `BadRequestException`, handled by Nest's exception layer.
- `package.json` pins `@nestjs/common`, `@nestjs/core` and `@nestjs/platform-express` to 10.4.15.

## Trade-offs
- Idiomatic Nest uses TypeScript decorators and `nest build`; the hand-applied decorators here are unusual and harder to read.
- A large `node_modules` and a slow start for two routes.
- One event loop, so CPU-bound work blocks all requests unless moved to workers.

## When not to use it
- For one or two tiny endpoints, where Express or Fastify directly is enough.
- For CPU-heavy request handling.
