#!/usr/bin/env python3
"""Trivy -> Vibe Security Evidence adapter. The framework does not install Trivy."""
import argparse,json,shutil,subprocess,tempfile
from pathlib import Path

def emit(status,available,target,version=None,findings=None,limitations=None,mode="fs"):
 d={"schema_version":"1.0","tool":{"name":"trivy","version":version,"available":available},
 "check_id":"external.trivy","baseline_controls":[54,55,70],"status":status,"target":str(target),
 "scan_mode":mode,"findings":findings or [],"limitations":limitations or []}
 print(json.dumps(d,ensure_ascii=False,indent=2));return d

def version_of(binary):
 p=subprocess.run([binary,"--version"],capture_output=True,text=True,timeout=10)
 t=(p.stdout or p.stderr).strip()
 return t.splitlines()[0] if t else None

def normalize(report):
 out=[]
 for result in report.get("Results") or []:
  target=result.get("Target")
  for v in result.get("Vulnerabilities") or []:
   out.append({"finding_id":v.get("VulnerabilityID"),"severity":v.get("Severity"),
    "package":v.get("PkgName"),"installed_version":v.get("InstalledVersion"),
    "fixed_version":v.get("FixedVersion") or None,"target":target,
    "status":v.get("Status") or None,"primary_url":v.get("PrimaryURL") or None})
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument("--target",default=".");ap.add_argument("--mode",choices=["fs","sbom"],default="fs");ap.add_argument("--json",action="store_true");a=ap.parse_args()
 target=Path(a.target).resolve();binary=shutil.which("trivy")
 if not binary:
  emit("NOT_AVAILABLE",False,target,limitations=["Trivy executable not found in PATH.","NOT_AVAILABLE is never PASS."],mode=a.mode);return 0
 version=version_of(binary)
 with tempfile.TemporaryDirectory() as td:
  rp=Path(td)/"trivy.json"
  cmd=[binary,a.mode,"--format","json","--output",str(rp)]
  if a.mode=="fs":cmd += ["--scanners","vuln",str(target)]
  else:cmd += [str(target)]
  try:p=subprocess.run(cmd,capture_output=True,text=True,timeout=600)
  except subprocess.TimeoutExpired:
   emit("ERROR",True,target,version,limitations=["Trivy timed out after 600 seconds."],mode=a.mode);return 0
  if not rp.exists():
   emit("ERROR",True,target,version,limitations=["Trivy did not produce the expected JSON report.",(p.stderr or "").strip()[:500]],mode=a.mode);return 0
  try:report=json.loads(rp.read_text(encoding="utf-8") or "{}")
  except Exception:
   emit("ERROR",True,target,version,limitations=["Trivy report was not valid JSON."],mode=a.mode);return 0
  findings=normalize(report)
  status="FAIL" if findings else ("PASS" if p.returncode==0 else "ERROR")
  emit(status,True,target,version,findings,[
   "A PASS only means this Trivy invocation returned no normalized vulnerability findings.",
   "Database freshness, scanner configuration and package-detection coverage affect results.",
   "A scanner result does not automatically promote baseline controls to validated."
  ],a.mode)
  return 1 if status=="FAIL" else 0
if __name__=="__main__":raise SystemExit(main())
