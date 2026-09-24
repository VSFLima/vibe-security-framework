#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

EXTS={".apk",".aab",".ipa",".jar",".war",".zip",".tar",".gz",".tgz",".whl"}
MAX=500_000_000

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--target",default="."); ap.add_argument("--json",action="store_true")
    a=ap.parse_args(); root=Path(a.target).resolve()
    found=[]
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in EXTS:
            try:
                size=p.stat().st_size
            except Exception: continue
            found.append(f"{p.relative_to(root)} ({size/1024/1024:.1f} MB)")
    status="WARN" if found else "PASS"
    summary=(f"{len(found)} release/archive artifact(s) detected; manual/deeper artifact inspection required."
             if found else "No supported release/archive artifact detected in target tree.")
    out={"check":"artifacts","status":status,"summary":summary,"details":found[:100],
         "limitations":["Discovery only in v0.1.",
                        "Does not decompile APK/AAB or inspect archive contents yet.",
                        "Source-code PASS never substitutes artifact validation for controls 3/57/70."]}
    print(json.dumps(out,ensure_ascii=False) if a.json else out)
    return 0
if __name__=="__main__": raise SystemExit(main())
