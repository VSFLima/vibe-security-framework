#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
BLOCK_STRICT={"FAIL","ERROR","NOT_AVAILABLE","NOT_RUN"}
BLOCK_ADVISORY={"FAIL","ERROR"}
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--evidence",action="append",default=[])
 ap.add_argument("--policy",choices=["strict","advisory"],default="strict")
 a=ap.parse_args()
 rows=[]; invalid=[]
 for fn in a.evidence:
  p=Path(fn)
  if not p.exists(): invalid.append({"source":fn,"status":"NOT_RUN"});continue
  try:d=json.loads(p.read_text(encoding="utf-8"))
  except Exception: invalid.append({"source":fn,"status":"ERROR"});continue
  rows.append({"source":fn,"check_id":d.get("check_id"),"status":d.get("status")})
 rows+=invalid
 blockers=BLOCK_STRICT if a.policy=="strict" else BLOCK_ADVISORY
 blocked=[r for r in rows if r.get("status") in blockers]
 inconclusive=[r for r in rows if r.get("status") in {"WARN","NOT_AVAILABLE","NOT_RUN"}]
 status="FAIL" if blocked else ("INCONCLUSIVE" if inconclusive else "PASS")
 print(json.dumps({"policy":a.policy,"status":status,"evidence":rows,"blocked":blocked},ensure_ascii=False))
 if blocked:return 1
 if status=="INCONCLUSIVE" and a.policy=="strict":return 2
 return 0
if __name__=="__main__":raise SystemExit(main())
