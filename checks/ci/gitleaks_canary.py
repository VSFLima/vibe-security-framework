#!/usr/bin/env python3
import argparse,json,subprocess,tempfile,os,sys
from pathlib import Path
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--gitleaks",default="gitleaks");a=ap.parse_args()
 with tempfile.TemporaryDirectory() as td:
  r=Path(td); fixture=r/"canary.txt"; report=r/"report.json"
  # Synthetic Gitleaks-positive fixture used only for scanner validation; never a real credential.
  synthetic_key = "AKIA" + "LALEMEL" + "33243" + "OLIB"
  fixture.write_text(f"aws_access_key_id = {synthetic_key}\n",encoding="utf-8")
  q=subprocess.run([a.gitleaks,"dir",str(r),"--report-format","json","--report-path",str(report),"--redact=100","--no-banner"],capture_output=True,text=True,timeout=60)
  try:data=json.loads(report.read_text(encoding="utf-8")) if report.exists() else []
  except Exception:data=[]
  found=bool(data)
  print(json.dumps({"canary":"gitleaks","status":"PASS" if found else "FAIL","finding_detected":found,"secret_value_emitted":False}))
  return 0 if found else 1
if __name__=="__main__":raise SystemExit(main())
