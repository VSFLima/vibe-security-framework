#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

A = Path(__file__).resolve().parents[1] / "adapters" / "trivy_adapter.py"

FAKE_PY = r'''
import json
import sys
from pathlib import Path

args = sys.argv[1:]

if args and args[0] == "--version":
    print("Version: 0.fixture")
    raise SystemExit(0)

report = None
target = None

for i, arg in enumerate(args):
    if arg == "--output" and i + 1 < len(args):
        report = Path(args[i + 1])

if args:
    target = args[-1]

if report is None:
    raise SystemExit(2)

if target and "vulnerable" in target:
    data = {
        "Results": [
            {
                "Target": target,
                "Vulnerabilities": [
                    {
                        "VulnerabilityID": "CVE-FIXTURE",
                        "Severity": "HIGH",
                        "PkgName": "fixture",
                        "InstalledVersion": "1.0.0",
                        "FixedVersion": "1.0.1",
                        "Status": "fixed",
                        "PrimaryURL": "https://example.invalid/CVE-FIXTURE"
                    }
                ]
            }
        ]
    }
else:
    data = {"Results": []}

report.write_text(json.dumps(data), encoding="utf-8")
raise SystemExit(0)
'''


def install_fake_trivy(bin_dir: Path):
    fake_py = bin_dir / "trivy_fake.py"
    fake_py.write_text(FAKE_PY, encoding="utf-8")

    if os.name == "nt":
        launcher = bin_dir / "trivy.cmd"
        launcher.write_text(
            '@echo off\r\n'
            f'"{sys.executable}" "%~dp0trivy_fake.py" %*\r\n',
            encoding="utf-8",
        )
    else:
        launcher = bin_dir / "trivy"
        launcher.write_text(
            f'#!/bin/sh\nexec "{sys.executable}" "$(dirname "$0")/trivy_fake.py" "$@"\n',
            encoding="utf-8",
        )
        launcher.chmod(0o755)

    return launcher


def invoke(target: Path, bin_dir: Path, mode: str):
    env = os.environ.copy()
    env["PATH"] = str(bin_dir) + os.pathsep + env.get("PATH", "")

    p = subprocess.run(
        [
            sys.executable,
            str(A),
            "--target",
            str(target),
            "--mode",
            mode,
            "--json",
        ],
        capture_output=True,
        text=True,
        env=env,
        timeout=15,
    )

    return p, json.loads(p.stdout)


def main():
    n = 0

    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        b = r / "bin"
        b.mkdir()

        install_fake_trivy(b)

        clean = r / "clean"
        clean.mkdir()

        p, d = invoke(clean, b, "fs")
        assert d["status"] == "PASS"
        assert d["tool"]["available"] is True
        n += 1

        vulnerable = r / "vulnerable"
        vulnerable.mkdir()

        p, d = invoke(vulnerable, b, "fs")
        assert d["status"] == "FAIL"
        assert d["findings"][0]["finding_id"] == "CVE-FIXTURE"
        assert d["findings"][0]["severity"] == "HIGH"
        n += 1

        sb = r / "fixture.sbom.json"
        sb.write_text("{}", encoding="utf-8")

        p, d = invoke(sb, b, "sbom")
        assert d["scan_mode"] == "sbom"
        n += 1

        assert d["baseline_controls"] == [54, 55, 70]
        n += 1

    print(
        json.dumps(
            {
                "suite": "trivy-adapter",
                "status": "PASS",
                "tests": n,
            }
        )
    )


if __name__ == "__main__":
    main()
