#!/usr/bin/env python3
import json,subprocess,sys,tempfile
from pathlib import Path
B=Path(__file__).resolve().parents[1]/"ci"/"build_sarif.py"
def main():
 with tempfile.TemporaryDirectory() as td:
  r=Path(td)
  a=r/"g.json";a.write_text(json.dumps({"tool":{"name":"gitleaks"},"status":"FAIL","findings":[{"finding_id":"rule-x","description":"fixture","file":"a.py","start_line":7}]}))
  b=r/"t.json";b.write_text(json.dumps({"tool":{"name":"trivy"},"status":"NOT_AVAILABLE","findings":[]}))
  out=r/"o.sarif"
  p=subprocess.run([sys.executable,str(B),"--input",str(a),"--input",str(b),"--output",str(out)],capture_output=True,text=True,timeout=10)
  assert p.returncode==0
  d=json.loads(out.read_text(encoding="utf-8"));res=d["runs"][0]["results"]
  assert d["version"]=="2.1.0";assert len(res)==2
  assert any(x["ruleId"]=="gitleaks.rule-x" for x in res)
  assert any("NOT_AVAILABLE" in x["message"]["text"] for x in res)
 print(json.dumps({"suite":"sarif-builder","status":"PASS","tests":4}))
if __name__=="__main__":main()
