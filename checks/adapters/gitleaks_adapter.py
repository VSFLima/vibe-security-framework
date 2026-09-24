#!/usr/bin/env python3
import argparse,json,shutil,subprocess,tempfile
from pathlib import Path
def emit(status,available,target,version=None,findings=None,limitations=None):
 d={"schema_version":"1.0","tool":{"name":"gitleaks","version":version,"available":available},"check_id":"external.gitleaks","baseline_controls":[1,2,3,4,70],"status":status,"target":str(target),"findings":findings or [],"limitations":limitations or []}
 print(json.dumps(d,ensure_ascii=False,indent=2));return d
def main():
 a=argparse.ArgumentParser();a.add_argument("--target",default=".");a.add_argument("--mode",choices=["auto","git","dir"],default="auto");a.add_argument("--json",action="store_true");x=a.parse_args();target=Path(x.target).resolve()
 b=shutil.which("gitleaks")
 if not b:
  emit("NOT_AVAILABLE",False,target,limitations=["Gitleaks executable not found in PATH.","NOT_AVAILABLE is never PASS."]);return 0
 v=subprocess.run([b,"version"],capture_output=True,text=True,timeout=10);version=(v.stdout or v.stderr).strip().splitlines()[0] if (v.stdout or v.stderr).strip() else None
 mode=x.mode if x.mode!="auto" else ("git" if (target/".git").exists() else "dir")
 with tempfile.TemporaryDirectory() as td:
  rp=Path(td)/"report.json";cmd=[b,mode,str(target),"--report-format","json","--report-path",str(rp),"--redact=100","--no-banner"]
  try:p=subprocess.run(cmd,capture_output=True,text=True,timeout=300)
  except subprocess.TimeoutExpired:
   emit("ERROR",True,target,version,limitations=["Gitleaks timed out."]);return 0
  try:items=json.loads(rp.read_text(encoding="utf-8") or "[]") if rp.exists() else []
  except Exception:
   emit("ERROR",True,target,version,limitations=["Gitleaks report was not valid JSON."]);return 0
  findings=[{"finding_id":f.get("Fingerprint") or f.get("RuleID"),"rule_id":f.get("RuleID"),"description":f.get("Description"),"file":f.get("File"),"start_line":f.get("StartLine"),"commit":f.get("Commit") or None,"redacted":True} for f in items]
  status="FAIL" if findings else ("PASS" if p.returncode==0 else "ERROR")
  emit(status,True,target,version,findings,["Normalized evidence excludes Secret, Match and Line.","Rotation/revocation must be verified separately."])
  return 1 if status=="FAIL" else 0
if __name__=="__main__":raise SystemExit(main())
