#!/usr/bin/env python3

import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

CHECKS_DIR = Path(__file__).resolve().parents[1]


def load(name):
    path = CHECKS_DIR / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(name, root):
    module = load(name)
    old_argv = sys.argv
    sys.argv = [name, "--target", str(root), "--json"]

    try:
        buffer = io.StringIO()

        with contextlib.redirect_stdout(buffer):
            rc = module.main()

        return json.loads(buffer.getvalue()), rc
    finally:
        sys.argv = old_argv


def expect(label, got, want):
    assert got == want, f"{label}: {got} != {want}"


def git(root, *args):
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, (
        f"git {' '.join(args)} failed:\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )


def init_git_repo(root):
    git(root, "init")
    git(root, "config", "user.name", "Vibe Security Tests")
    git(root, "config", "user.email", "tests@example.invalid")


def commit_all(root, message):
    git(root, "add", ".")
    git(root, "commit", "-m", message)


def main():
    tests = 0

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "app.py").write_text('print("ok")', encoding="utf-8")

        output, _ = run("check_secrets.py", root)
        expect("secrets pass", output["status"], "PASS")
        tests += 1

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)

        (root / "app.py").write_text(
            'API_KEY="fixture_' + 'secret_value_123456789"',
            encoding="utf-8",
        )

        output, _ = run("check_secrets.py", root)
        expect("secrets fail", output["status"], "FAIL")
        tests += 1

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "prod.pem").write_text("x", encoding="utf-8")

        output, _ = run("check_repo_hygiene.py", root)
        expect("repo fail", output["status"], "FAIL")
        tests += 1

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "package.json").write_text("{}", encoding="utf-8")
        (root / "package-lock.json").write_text("{}", encoding="utf-8")

        output, _ = run("check_dependencies.py", root)
        expect("deps pass", output["status"], "PASS")
        tests += 1

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "SBOM_GUIDE.md").write_text("docs", encoding="utf-8")

        output, _ = run("check_sbom.py", root)
        expect("sbom false positive", output["status"], "WARN")
        tests += 1

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "sbom.cdx.json").write_text("{}", encoding="utf-8")

        output, _ = run("check_sbom.py", root)
        expect("sbom pass", output["status"], "PASS")
        tests += 1

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)

        output, _ = run("check_git_history_secrets.py", root)
        expect("git warn", output["status"], "WARN")
        tests += 1

    # Known synthetic fixtures used by this framework must not make the
    # framework detect its own test history as a real secret finding.
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        init_git_repo(root)

        known_example = "AKIA" + "IOSFODNN7" + "EXAMPLE"
        known_canary = "AKIA" + "LALEMEL" + "33243" + "OLIB"

        (root / "fixtures.txt").write_text(
            (
                f"aws_access_key_id = {known_example}\n"
                f"aws_access_key_id = {known_canary}\n"
            ),
            encoding="utf-8",
        )

        commit_all(root, "add synthetic fixtures")

        output, rc = run("check_git_history_secrets.py", root)

        expect("known synthetic history status", output["status"], "PASS")
        expect("known synthetic history rc", rc, 0)
        tests += 1

    # Any different AWS-shaped value must continue to be detected.
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        init_git_repo(root)

        unknown_fixture = "AKIA" + "ZXCVBNMASDFGHJKL"

        (root / "unsafe.txt").write_text(
            f"aws_access_key_id = {unknown_fixture}\n",
            encoding="utf-8",
        )

        commit_all(root, "add unknown credential-shaped value")

        output, rc = run("check_git_history_secrets.py", root)

        expect("unknown history status", output["status"], "FAIL")
        expect("unknown history rc", rc, 1)
        tests += 1

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        artifact = root / "bad.apk"

        with zipfile.ZipFile(artifact, "w") as archive:
            archive.writestr("assets/key.properties", "x")

        output, _ = run("check_artifact_contents.py", root)
        expect("artifact fail", output["status"], "FAIL")
        tests += 1

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        artifact = root / "clean.apk"

        with zipfile.ZipFile(artifact, "w") as archive:
            archive.writestr("assets/readme.txt", "x")

        output, _ = run("check_artifact_contents.py", root)
        expect("artifact warn", output["status"], "WARN")
        tests += 1

    print(
        json.dumps(
            {
                "suite": "checks-contract",
                "status": "PASS",
                "tests": tests,
            }
        )
    )


if __name__ == "__main__":
    main()
