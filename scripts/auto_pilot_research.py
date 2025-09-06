#!/usr/bin/env python3
"""
Auto pilot for Dhātu research pipeline:
 - Generates derived data (experiments/dhatu/report.py)
 - Computes metrics and phenomena (experiments/dhatu/validator.py)
 - Optionally builds the MkDocs site
 - Logs outputs and writes a last_status.json
 - Optionally loops for a duration with a fixed interval (default 8h total)

Safe by default: no commits or pushes unless explicitly enabled.
"""
from __future__ import annotations
import argparse, json, os, subprocess, sys, time, datetime, shlex
from typing import Dict, Any, List

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DHATU_DIR = os.path.join(ROOT, "experiments", "dhatu")
DOCS_DIR = os.path.join(ROOT, "docs")
DATA_DIR = os.path.join(DOCS_DIR, "data")
LOG_DIR = os.path.join(ROOT, "logs")

ENV_SAFE = {
    "LC_ALL": "C.UTF-8",
    "LANG": "C.UTF-8",
    "PAGER": "cat",
    "GIT_PAGER": "cat",
    "GH_PAGER": "cat",
    "LESS": "-F -X -R",
    "PYTHONUNBUFFERED": "1",
}

def now_iso() -> str:
    return datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat()

def merge_env(env: Dict[str, str]) -> Dict[str, str]:
    out = os.environ.copy()
    out.update(env)
    return out

def run(cmd: List[str], cwd: str | None = None, env: Dict[str, str] | None = None, timeout: int | None = None) -> subprocess.CompletedProcess:
    effective_env = merge_env(ENV_SAFE)
    if env:
        effective_env.update(env)
    return subprocess.run(cmd, cwd=cwd or ROOT, env=effective_env, capture_output=True, text=True, timeout=timeout)

def ensure_dirs():
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

def write_json(path: str, data: Any):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def append_log(line: Dict[str, Any]):
    path = os.path.join(LOG_DIR, "auto_pilot_research.log.jsonl")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False)+"\n")

def exec_and_record(name: str, cmd: List[str], cwd: str | None = None, timeout: int | None = None) -> Dict[str, Any]:
    start = time.time()
    proc = run(cmd, cwd=cwd, timeout=timeout)
    dur = round(time.time()-start, 3)
    rec = {
        "ts": now_iso(),
        "name": name,
        "cmd": cmd,
        "cwd": cwd or ROOT,
        "rc": proc.returncode,
        "duration_s": dur,
        "stdout": proc.stdout[-4000:],  # trim
        "stderr": proc.stderr[-4000:],
    }
    append_log(rec)
    return rec

def generate_reports() -> Dict[str, Any]:
    return exec_and_record("report", [sys.executable, os.path.join(DHATU_DIR, "report.py")], cwd=DHATU_DIR)

def compute_metrics() -> Dict[str, Any]:
    m = exec_and_record("metrics", [sys.executable, os.path.join(DHATU_DIR, "validator.py"), "--metrics"], cwd=DHATU_DIR)
    ph = exec_and_record("phenomena", [sys.executable, os.path.join(DHATU_DIR, "validator.py"), "--phenomena"], cwd=DHATU_DIR)
    cm = exec_and_record("child-metrics", [sys.executable, os.path.join(DHATU_DIR, "validator.py"), "--child-metrics", "fr", "en"], cwd=DHATU_DIR)
    return {"metrics": m, "phenomena": ph, "child_metrics": cm}

def build_docs() -> Dict[str, Any]:
    mkdocs_bin = os.path.join(ROOT, "venv_docs", "bin", "mkdocs")
    if os.path.exists(mkdocs_bin):
        cmd = [mkdocs_bin, "build", "-q"]
    else:
        cmd = ["mkdocs", "build", "-q"]
    return exec_and_record("mkdocs-build", cmd, cwd=ROOT)

def git_status_paths(paths: List[str]) -> List[str]:
    proc = run(["git", "status", "--porcelain", "--"] + paths)
    changed = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        # format: XY path
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            changed.append(parts[1])
    return changed

def git_commit(paths: List[str], message: str) -> Dict[str, Any]:
    add = exec_and_record("git-add", ["git", "add"] + paths)
    if add["rc"] != 0:
        return {"add": add, "commit": None}
    commit = exec_and_record("git-commit", ["git", "commit", "-m", message, "--no-gpg-sign"])
    return {"add": add, "commit": commit}

def iteration(do_build: bool, do_commit: bool, paths_to_commit: List[str]) -> Dict[str, Any]:
    out: Dict[str, Any] = {"ts": now_iso()}
    out["reports"] = generate_reports()
    out["metrics"] = compute_metrics()
    changed = git_status_paths([os.path.relpath(DATA_DIR, ROOT)])
    out["changed_files"] = changed
    if do_build:
        out["build"] = build_docs()
    if do_commit and changed:
        msg = f"chore(research): update Dhātu generated data [{now_iso()}]"
        out["commit"] = git_commit(changed, msg)
    write_json(os.path.join(LOG_DIR, "auto_pilot_research.last_status.json"), out)
    return out

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--interval", type=int, default=3600, help="Interval between iterations in seconds (default 3600s)")
    ap.add_argument("--duration", type=int, default=8*3600, help="Total duration in seconds (default 8h)")
    ap.add_argument("--once", action="store_true", help="Run a single iteration and exit")
    ap.add_argument("--no-build", dest="build", action="store_false", help="Do not build MkDocs")
    ap.add_argument("--commit", action="store_true", help="Commit generated changes (no push)")
    args = ap.parse_args(argv)

    ensure_dirs()
    start = time.time()
    paths_to_commit = [os.path.relpath(DATA_DIR, ROOT)]

    if args.once:
        iteration(do_build=args.build, do_commit=args.commit, paths_to_commit=paths_to_commit)
        return 0

    deadline = start + max(0, args.duration)
    i = 0
    while True:
        i += 1
        print(f"[auto] iteration {i} at {now_iso()}")
        try:
            iteration(do_build=args.build, do_commit=args.commit, paths_to_commit=paths_to_commit)
        except Exception as e:
            append_log({"ts": now_iso(), "name": "iteration-error", "error": str(e)})
        if time.time() + args.interval > deadline:
            break
        time.sleep(max(1, args.interval))
    return 0

if __name__ == "__main__":
    sys.exit(main())
