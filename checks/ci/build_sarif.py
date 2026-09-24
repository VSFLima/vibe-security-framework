#!/usr/bin/env python3
import argparse,json
from pathlib import Path

LEVEL={"CRITICAL":"error","HIGH":"error","MEDIUM":"warning","LOW":"note","UNKNOWN":"warning"}

def main():
 ap=argparse.ArgumentParser();ap.add_argument("--input",action="append",default=[]);ap.add_argument("--output",required=True);a=ap.parse_args()
 results=[];rules={}
 for name in a.input:
  p=Path(name)
  if not p.exists():continue
  d=json.loads(p.read_text(encoding="utf-8"))
  tool=(d.get("tool") or {}).get("name","unknown")
  status=d.get("status")
  if status in {"NOT_AVAILABLE","NOT_RUN","ERROR"}:
   rid=f"vsf.{tool}.{status.lower()}"
   rules[rid]={"id":rid,"shortDescription":{"text":f"{tool}: {status}"}}
   results.append({"ruleId":rid,"level":"warning","message":{"text":f"{tool} returned {status}; this is not PASS."}})
  for f in d.get("findings") or []:
   fid=f.get("finding_id") or f.get("rule_id") or "finding"
   rid=f"{tool}.{fid}"
   rules[rid]={"id":rid,"shortDescription":{"text":str(fid)}}
   msg=f.get("description") or f"{fid}"
   if f.get("package"):msg+=f" — package {f['package']}"
   res={"ruleId":rid,"level":LEVEL.get(str(f.get("severity","UNKNOWN")).upper(),"warning"),"message":{"text":msg}}
   file=f.get("file") or f.get("target")
   line=f.get("start_line")
   if file:
    region={"startLine":int(line)} if isinstance(line,int) and line>0 else {}
    res["locations"]=[{"physicalLocation":{"artifactLocation":{"uri":str(file)},"region":region}}]
   results.append(res)
 sarif={"version":"2.1.0","$schema":"https://json.schemastore.org/sarif-2.1.0.json","runs":[{"tool":{"driver":{"name":"Vibe Security Framework","rules":list(rules.values())}},"results":results}]}
 Path(a.output).write_text(json.dumps(sarif,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({"status":"PASS","results":len(results),"output":a.output}))
if __name__=="__main__":main()
