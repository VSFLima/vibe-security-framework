#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from common import files_under, read_small_text

PATTERNS = [
    ("private_key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    ("aws_access_key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("github_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{30,}\b")),
    ("slack_token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("generic_secret_assignment", re.compile(
        r"(?i)\b(api[_-]?key|secret|client[_-]?secret|access[_-]?token|auth[_-]?token|password)\b"
        r"\s*[:=]\s*[\"']([^\"'\n]{12,})[\"']"
    )),
]
PLACEHOLDER_WORDS = {"example","changeme","placeholder","your_","dummy","test","fake","redacted","xxx"}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--target",default="."); ap.add_argument("--json",action="store_true")
    a=ap.parse_args(); root=Path(a.target).resolve()
    findings=[]
    for p in files_under(root):
        # Scanner fixtures intentionally contain synthetic secret-shaped strings.
        # Excluding only this framework-owned test-fixture path avoids self-findings
        # without suppressing user/project tests in other locations.
        rel = p.relative_to(root)
        if tuple(rel.parts[:2]) == ("checks", "tests"):
            continue
        text=read_small_text(p)
        if text is None: continue
        for lineno,line in enumerate(text.splitlines(),1):
            for name,rx in PATTERNS:
                m=rx.search(line)
                if not m: continue
                sample=m.group(0)
                if any(w in sample.lower() for w in PLACEHOLDER_WORDS): continue
                findings.append(f"{p.relative_to(root)}:{lineno} [{name}]")
    status="FAIL" if findings else "PASS"
    out={"check":"secrets","status":status,
         "summary": f"{len(findings)} potential secret(s) found." if findings else "No configured secret pattern matched.",
         "details": findings[:100],
         "limitations":["Heuristic scan; false positives/negatives are possible.",
                        "Does not scan Git history. Does not prove rotation/revocation."]}
    print(json.dumps(out,ensure_ascii=False) if a.json else out)
    return 1 if status=="FAIL" else 0
if __name__=="__main__": raise SystemExit(main())
