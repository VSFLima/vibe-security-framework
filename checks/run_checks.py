#!/usr/bin/env python3
"""
Vibe Security Framework - local safe checks runner.
Read-only by design. No network calls, no writes to the target repository.
"""
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path

CHECKS = [
    ("secrets", "check_secrets.py"),
    ("git_history_secrets", "check_git_history_secrets.py"),
    ("repo", "check_repo_hygiene.py"),
    ("dependencies", "check_dependencies.py"),
    ("sbom", "check_sbom.py"),
    ("artifacts", "check_artifacts.py"),
    ("artifact_contents", "check_artifact_contents.py"),
]

def run_check(script: Path, target: Path):
    p = subprocess.run(
        [sys.executable, str(script), "--target", str(target), "--json"],
        capture_output=True, text=True
    )
    try:
        data = json.loads(p.stdout)
    except Exception:
        data = {
            "check": script.stem,
            "status": "ERROR",
            "summary": "Check did not return valid JSON.",
            "details": [p.stderr.strip() or p.stdout.strip()]
        }
    return data

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=".", help="Repository/project directory to inspect")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    target = Path(args.target).resolve()
    here = Path(__file__).resolve().parent

    results = [run_check(here / script, target) for _, script in CHECKS]
    statuses = [r.get("status") for r in results]
    overall = "FAIL" if "FAIL" in statuses else ("WARN" if "WARN" in statuses or "ERROR" in statuses else "PASS")
    report = {"framework": "vibe-security-framework", "checks_version": "0.2.2",
              "target": str(target), "overall": overall, "results": results}

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Vibe Security Checks 0.2.2 — {target}")
        print(f"OVERALL: {overall}\n")
        for r in results:
            print(f"[{r['status']}] {r['check']}: {r['summary']}")
            for d in r.get("details", [])[:12]:
                print(f"  - {d}")
            print()
        print("Important: PASS means only that these local checks found no configured failure.")
        print("It does NOT validate the full 99-control baseline.")

    return 1 if overall == "FAIL" else 0

if __name__ == "__main__":
    raise SystemExit(main())
