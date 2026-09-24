#!/usr/bin/env python3
import json,subprocess,sys,tempfile
from pathlib import Path
M=Path(__file__).resolve().parents[1]/"evidence"/"map_evidence.py"
MAP=Path(__file__).resolve().parents[1]/"evidence"/"CONTROL_EVIDENCE_MAP.json"
def main():
 with tempfile.TemporaryDirectory() as td:
  r=Path(td)
  g=r/"g.json";g.write_text(json.dumps({"check_id":"external.gitleaks","status":"PASS","findings":[]}))
  t=r/"t.json";t.write_text(json.dumps({"check_id":"external.trivy","status":"FAIL","findings":[{"finding_id":"CVE-X"}]}))
  u=r/"u.json";u.write_text(json.dumps({"check_id":"external.future","status":"PASS","findings":[]}))
  out=r/"mapped.json"
  p=subprocess.run([sys.executable,str(M),"--map",str(MAP),"--evidence",str(g),"--evidence",str(t),"--evidence",str(u),"--output",str(out)],capture_output=True,text=True,timeout=10)
  assert p.returncode==0
  d=json.loads(out.read_text(encoding="utf-8"));controls={x["control"]:x for x in d["controls"]}
  assert set(controls)=={1,2,3,4,54,55,70}
  assert all(x["auto_validated"] is False and x["suggested_status"]=="REVIEW_REQUIRED" for x in controls.values())
  assert controls[1]["evidence"][0]["scanner_status"]=="PASS"
  assert controls[54]["evidence"][0]["scanner_status"]=="FAIL"
  assert d["unmapped_or_invalid"][0]["reason"]=="unmapped_check"
  assert "validated/✅" in d["policy"]["message"]
 print(json.dumps({"suite":"evidence-mapper","status":"PASS","tests":6}))
if __name__=="__main__":main()
