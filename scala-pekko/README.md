# scala-pekko

The Orders endpoint in Scala 3.3.4 with Apache Pekko HTTP: `src/main/scala/orders/Main.scala` (27 lines), `build.sbt` and `project/build.properties` (sbt 1.10.6).

## Goal
Implement the shared contract (`GET /orders/{id}`, `GET /health`, port from `PORT`, default 8080) with Pekko's route DSL on the JVM.

## Run it
```bash
cd scala-pekko && sbt run
curl -s localhost:8080/orders/7
```
Expected: `{"id":7,"customer":"c-7","total":7.5,"status":"NEW"}`. A negative or non-numeric id returns 400 with `{"error":"bad id"}`.

Not run end to end: sbt is not installed on the machine these READMEs were written on, so this folder was never compiled. The output above is derived from reading `Main.scala`. It needs JDK 21 and sbt.

## What it proves
- Routes are composed declaratively with `concat`, `path` and `get`; the id is matched with `Segment` and validated with `toLongOption`.
- The server is built on an `ActorSystem` and Pekko streams, with `build.sbt` pinning pekko-actor-typed and pekko-stream 1.1.2 and pekko-http 1.1.0.
- The JSON is assembled with string interpolation, so no JSON library is needed.

## Trade-offs
- Slowest start and largest memory footprint here (JVM plus actor system), and long sbt compiles.
- Hand-built JSON is fragile; real code would use a JSON library.
- The `bind` result is never awaited or shut down, so the server runs until killed.

## When not to use it
- For plain request/response services with no streaming or actor needs.
- When the team has no Scala experience.
