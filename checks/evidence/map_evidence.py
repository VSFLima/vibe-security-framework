#!/usr/bin/env python3
import argparse,json
from pathlib import Path

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--evidence",action="append",default=[])
 ap.add_argument("--map",dest="mapfile",default=str(Path(__file__).with_name("CONTROL_EVIDENCE_MAP.json")))
 ap.add_argument("--output",required=True)
 a=ap.parse_args()
 m=json.loads(Path(a.mapfile).read_text(encoding="utf-8"))
 controls={}
 unknown=[]
 for fn in a.evidence:
  p=Path(fn)
  if not p.exists():
   unknown.append({"source":fn,"reason":"evidence_file_missing"});continue
  try:d=json.loads(p.read_text(encoding="utf-8"))
  except Exception:
   unknown.append({"source":fn,"reason":"invalid_json"});continue
  cid=d.get("check_id")
  spec=(m.get("checks") or {}).get(cid)
  if not spec:
   unknown.append({"source":fn,"check_id":cid,"reason":"unmapped_check"});continue
  for n in spec.get("controls",[]):
   key=str(n);controls.setdefault(key,{"control":n,"suggested_status":"REVIEW_REQUIRED","auto_validated":False,"evidence":[]})
   controls[key]["evidence"].append({
    "check_id":cid,"scanner_status":d.get("status"),"source":fn,
    "finding_count":len(d.get("findings") or []),
    "coverage":spec.get("coverage","supporting"),
    "note":(spec.get("notes") or {}).get(key)
   })
 out={
  "schema_version":"1.0",
  "policy":{"automatic_validation":False,"message":"Evidence mapping never sets a baseline control to validated/✅. Rule 99 still applies."},
  "controls":[controls[k] for k in sorted(controls,key=lambda x:int(x))],
  "unmapped_or_invalid":unknown
 }
 Path(a.output).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({"status":"PASS","mapped_controls":len(out["controls"]),"unmapped_or_invalid":len(unknown),"output":a.output}))
if __name__=="__main__":main()
