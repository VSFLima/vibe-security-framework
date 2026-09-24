#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

SENSITIVE = [".env", ".env.local", ".env.production", ".npmrc", ".pypirc",
             "id_rsa", "id_ed25519", "key.properties"]
KEY_EXTS = {".pem",".p12",".pfx",".jks",".keystore"}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--target",default="."); ap.add_argument("--json",action="store_true")
    a=ap.parse_args(); root=Path(a.target).resolve()
    details=[]; fail=[]
    gitignore=root/".gitignore"
    gi=gitignore.read_text(encoding="utf-8",errors="ignore") if gitignore.exists() else ""
    if not gitignore.exists(): details.append("No .gitignore found.")
    for p in root.rglob("*"):
        if not p.is_file() or ".git" in p.parts: continue
        if p.name in SENSITIVE or p.suffix.lower() in KEY_EXTS:
            rel=str(p.relative_to(root))
            if p.name.startswith(".env") and p.name.endswith(".example"): continue
            fail.append(f"Sensitive-looking file present: {rel}")
    for expected in [".env", "*.pem", "*.p12", "*.pfx", "*.jks", "*.keystore"]:
        if expected not in gi:
            details.append(f".gitignore does not explicitly contain: {expected}")
    status="FAIL" if fail else ("WARN" if details else "PASS")
    out={"check":"repo_hygiene","status":status,
         "summary": f"{len(fail)} sensitive-looking file(s); {len(details)} hygiene warning(s).",
         "details": fail+details,
         "limitations":["Presence does not prove the file is tracked by Git.",
                        "Use a Git-history-aware scanner separately for historical exposure."]}
    print(json.dumps(out,ensure_ascii=False) if a.json else out)
    return 1 if status=="FAIL" else 0
if __name__=="__main__": raise SystemExit(main())
