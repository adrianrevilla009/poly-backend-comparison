#!/usr/bin/env python3
"""Same load test for every implementation: build, start, hammer GET /orders/{id}, print one table row.

Usage: bench.py [--seconds 5] [--threads 16] [folder ...]   (default: all five folders, skipping missing toolchains)
Stdlib only. Needs Python 3.8+ on Linux (memory is read from /proc).
"""
import argparse, http.client, os, shutil, statistics, subprocess, threading, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PORT = 18080
# folder -> (required tool, build command, run command, source globs for the lines-of-code column)
IMPLS = {
    "same endpoint in go": ("go", ["go", "build", "-o", "orders", "."], ["./orders"], ["*.go"]),
    "node-nestjs": ("npm", ["npm", "install", "--silent", "--no-audit", "--no-fund"], ["node", "main.js"], ["main.js"]),
    "python-fastapi": ("uvicorn", ["true"], ["uvicorn", "main:app", "--port", str(PORT), "--log-level", "warning"], ["main.py"]),
    "rust-axum": ("cargo", ["cargo", "build", "--release", "--quiet"], ["./target/release/orders"], ["src/*.rs"]),
    "scala-pekko": ("sbt", ["sbt", "-batch", "compile"], ["sbt", "-batch", "run"], ["src/main/scala/orders/*.scala"]),
}


def rss_mb(pid):
    kids = subprocess.run(["pgrep", "-P", str(pid)], capture_output=True, text=True).stdout.split()
    total = 0
    for p in [str(pid), *kids]:
        try:
            total += int(next(l for l in Path(f"/proc/{p}/status").read_text().splitlines() if l.startswith("VmRSS")).split()[1])
        except (OSError, StopIteration):
            pass
    return total / 1024


def load(seconds, threads):
    lat, errors, stop = [], [0], time.time() + seconds
    def worker(n):
        conn = http.client.HTTPConnection("127.0.0.1", PORT)
        i = n
        while time.time() < stop:
            t = time.perf_counter()
            try:
                conn.request("GET", f"/orders/{i}")
                r = conn.getresponse(); r.read()
                (lat.append if r.status == 200 else lambda _: errors.__setitem__(0, errors[0] + 1))(time.perf_counter() - t)
            except OSError:
                errors[0] += 1; conn = http.client.HTTPConnection("127.0.0.1", PORT)
            i += threads
    ts = [threading.Thread(target=worker, args=(n,)) for n in range(threads)]
    [t.start() for t in ts]; [t.join() for t in ts]
    lat.sort()
    if not lat:
        return 0.0, float("nan"), float("nan"), errors[0]
    return len(lat) / seconds, lat[len(lat) // 2] * 1000, lat[int(len(lat) * 0.99)] * 1000, errors[0]


def run(name, seconds, threads):
    tool, build, cmd, globs = IMPLS[name]
    d = ROOT / name
    if not shutil.which(tool):
        return f"| {name} | skipped: `{tool}` not installed | | | | |"
    loc = sum(len(f.read_text().splitlines()) for g in globs for f in d.glob(g))
    t = time.time(); subprocess.run(build, cwd=d, check=True); build_s = time.time() - t
    srv = subprocess.Popen(cmd, cwd=d, env={**os.environ, "PORT": str(PORT)}, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(120):  # wait up to 60 s for the port
            try:
                http.client.HTTPConnection("127.0.0.1", PORT, timeout=1).request("GET", "/health"); break
            except OSError:
                time.sleep(0.5)
        load(1, threads)  # warm-up
        rps, p50, p99, err = load(seconds, threads)
        return f"| {name} | {rps:.0f} | {p50:.2f} / {p99:.2f} | {rss_mb(srv.pid):.0f} | {build_s:.1f} | {loc} |" + (f" errors={err}" if err else "")
    finally:
        srv.terminate(); srv.wait()


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--seconds", type=int, default=5); ap.add_argument("--threads", type=int, default=16)
    ap.add_argument("folders", nargs="*", default=list(IMPLS)); a = ap.parse_args()
    print("| Implementation | req/s | p50 / p99 ms | RSS MB | build s | LOC |\n|---|---|---|---|---|---|")
    for n in a.folders:
        print(run(n, a.seconds, a.threads), flush=True)
