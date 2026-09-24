#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

A = Path(__file__).resolve().parents[1] / "adapters" / "gitleaks_adapter.py"


FAKE_PY = r'''
import json
import sys
from pathlib import Path

args = sys.argv[1:]

if args and args[0] == "version":
    print("8.fixture")
    raise SystemExit(0)

target = args[1] if len(args) > 1 else ""

report = None
for i, arg in enumerate(args):
    if arg == "--report-path" and i + 1 < len(args):
        report = Path(args[i + 1])
        break

if report is None:
    raise SystemExit(2)

if "leaky" in target:
    data = [
        {
            "Description": "fixture",
            "File": "a.txt",
            "StartLine": 1,
            "RuleID": "fixture",
            "Fingerprint": "fp",
            "Secret": "MUST_NOT_LEAK",
            "Match": "MUST_NOT_LEAK",
            "Line": "MUST_NOT_LEAK",
        }
    ]
    report.write_text(json.dumps(data), encoding="utf-8")
    raise SystemExit(1)

report.write_text("[]", encoding="utf-8")
raise SystemExit(0)
'''


def install_fake_gitleaks(bin_dir: Path):
    fake_py = bin_dir / "gitleaks_fake.py"
    fake_py.write_text(FAKE_PY, encoding="utf-8")

    if os.name == "nt":
        launcher = bin_dir / "gitleaks.cmd"
        launcher.write_text(
            '@echo off\r\n'
            f'"{sys.executable}" "%~dp0gitleaks_fake.py" %*\r\n',
            encoding="utf-8",
        )
    else:
        launcher = bin_dir / "gitleaks"
        launcher.write_text(
            f'#!/bin/sh\nexec "{sys.executable}" "$(dirname "$0")/gitleaks_fake.py" "$@"\n',
            encoding="utf-8",
        )
        launcher.chmod(0o755)

    return launcher


def main():
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        b = r / "bin"
        b.mkdir()

        install_fake_gitleaks(b)

        env = os.environ.copy()
        env["PATH"] = str(b) + os.pathsep + env.get("PATH", "")

        clean = r / "clean"
        clean.mkdir()

        p = subprocess.run(
            [
                sys.executable,
                str(A),
                "--target",
                str(clean),
                "--json",
            ],
            capture_output=True,
            text=True,
            env=env,
            timeout=15,
        )

        d = json.loads(p.stdout)

        assert d["status"] == "PASS"
        assert d["tool"]["available"] is True

        leaky = r / "leaky"
        leaky.mkdir()

        p = subprocess.run(
            [
                sys.executable,
                str(A),
                "--target",
                str(leaky),
                "--json",
            ],
            capture_output=True,
            text=True,
            env=env,
            timeout=15,
        )

        d = json.loads(p.stdout)

        assert d["status"] == "FAIL"
        assert "MUST_NOT_LEAK" not in json.dumps(d)
        assert d["findings"][0]["redacted"] is True

    print(
        json.dumps(
            {
                "suite": "gitleaks-adapter",
                "status": "PASS",
                "tests": 4,
            }
        )
    )


if __name__ == "__main__":
    main()
