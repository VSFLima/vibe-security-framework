#!/usr/bin/env python3
import argparse,json,re,zipfile
from pathlib import Path
EXT={".apk",".aab",".jar",".war",".zip"};MAX_MEMBER=5000000;MAX_TOTAL=150000000
RX=[("private_key",re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),("aws_access_key",re.compile(rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"))];NAMES={".env","key.properties","service-account.json","credentials.json"}
def main():
 a=argparse.ArgumentParser();a.add_argument("--target",default=".");a.add_argument("--json",action="store_true");x=a.parse_args();r=Path(x.target).resolve();bad=[];warn=[];det=[];count=0
 for p in r.rglob("*"):
  if not p.is_file() or p.suffix.lower() not in EXT:continue
  count+=1;sc=0
  try:
   with zipfile.ZipFile(p) as z:
    for i in z.infolist():
     if Path(i.filename).name in NAMES or Path(i.filename).suffix.lower() in {".pem",".p12",".pfx",".jks",".keystore"}:bad.append(f"{p.relative_to(r)}: sensitive-looking member {i.filename}")
     if i.file_size>MAX_MEMBER or sc+i.file_size>MAX_TOTAL:continue
     try:d=z.read(i)
     except Exception:continue
     sc+=len(d)
     for n,rx in RX:
      if rx.search(d):bad.append(f"{p.relative_to(r)}: {n} pattern in {i.filename}")
    det.append(f"{p.relative_to(r)}: scanned ~{sc/1048576:.1f} MB")
  except zipfile.BadZipFile:warn.append(f"{p.relative_to(r)}: unreadable as ZIP")
 status="FAIL" if bad else ("WARN" if count or warn else "PASS");o={"check":"artifact_inspection","status":status,"summary":f"{count} artifact(s) inspected; {len(bad)} finding(s).","details":bad+warn+det,"limitations":["Static archive inspection only; no Android decompilation, manifest semantics, signing or runtime validation.","Read budgets reduce ZIP-bomb risk."]}
 print(json.dumps(o) if x.json else o);return 1 if bad else 0
if __name__=="__main__":raise SystemExit(main())
