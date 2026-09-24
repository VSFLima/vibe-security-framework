#!/usr/bin/env python3

import argparse
import json
import re
import subprocess
from pathlib import Path

PATTERNS = [
    (
        "private_key",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    ),
    (
        "aws_access_key",
        re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    ),
    (
        "github_token",
        re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{30,}\b"),
    ),
]

# Exact synthetic fixtures historically used by this repository.
#
# They are deliberately assembled from fragments so this source file itself
# does not become a secret-pattern finding.
#
# IMPORTANT:
# This allowlist applies only to the exact synthetic values below.
# It does NOT allowlist entire commits, files or AWS-shaped credentials.
KNOWN_SYNTHETIC_VALUES = {
    "AKIA" + "IOSFODNN7" + "EXAMPLE",
    "AKIA" + "LALEMEL" + "33243" + "OLIB",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.target).resolve()

    if not (root / ".git").exists():
        output = {
            "check": "git_history_secrets",
            "status": "WARN",
            "summary": "No .git directory found; Git history was not scanned.",
            "details": [],
            "limitations": [
                "Requires a local Git repository.",
            ],
        }

        print(json.dumps(output) if args.json else output)
        return 0

    commits_result = subprocess.run(
        ["git", "rev-list", "--max-count=500", "--all"],
        cwd=root,
        capture_output=True,
        text=True,
    )

    if commits_result.returncode:
        output = {
            "check": "git_history_secrets",
            "status": "ERROR",
            "summary": "Could not enumerate Git history.",
            "details": [commits_result.stderr.strip()],
            "limitations": [],
        }

        print(json.dumps(output) if args.json else output)
        return 0

    commits = commits_result.stdout.split()
    findings = []

    for commit in commits:
        diff_result = subprocess.run(
            [
                "git",
                "show",
                "--format=",
                "--no-ext-diff",
                "--unified=0",
                commit,
            ],
            cwd=root,
            capture_output=True,
            text=True,
            errors="ignore",
        )

        for line in diff_result.stdout.splitlines():
            if not line.startswith("+") or line.startswith("+++"):
                continue

            for pattern_name, regex in PATTERNS:
                for match in regex.finditer(line):
                    matched_value = match.group(0)

                    # Ignore only the exact synthetic fixtures known to this
                    # repository. Any other matching value remains a finding.
                    if matched_value in KNOWN_SYNTHETIC_VALUES:
                        continue

                    findings.append(
                        f"{commit[:12]} [{pattern_name}]"
                    )

    status = "FAIL" if findings else "PASS"

    output = {
        "check": "git_history_secrets",
        "status": status,
        "summary": (
            f"{len(findings)} potential historical secret occurrence(s) "
            f"across {len(commits)} commit(s)."
        ),
        "details": findings[:100],
        "limitations": [
            "Scans at most 500 commits.",
            (
                "Known synthetic fixtures are ignored only by exact value; "
                "commits and files are not broadly allowlisted."
            ),
            (
                "A match does not prove a credential is still active; "
                "verify rotation/revocation."
            ),
        ],
    }

    print(json.dumps(output) if args.json else output)
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
