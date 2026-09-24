#!/usr/bin/env python3
import argparse,json
from pathlib import Path
LOCKS={"package-lock.json","yarn.lock","pnpm-lock.yaml","poetry.lock","uv.lock","pubspec.lock","Cargo.lock","go.sum","Gemfile.lock","composer.lock"}
def main():
 a=argparse.ArgumentParser();a.add_argument("--target",default=".");a.add_argument("--json",action="store_true");x=a.parse_args();r=Path(x.target).resolve();ls=[];sb=[]
 for p in r.rglob("*"):
  if p.is_file() and ".git" not in p.parts:
   if p.name in LOCKS:ls.append(str(p.relative_to(r)))
   if p.name.lower() in {"bom.json","bom.xml","sbom.json","sbom.xml","sbom.spdx","sbom.spdx.json","sbom.cdx.json","sbom.cdx.xml"}:sb.append(str(p.relative_to(r)))
 status="PASS" if sb else "WARN";o={"check":"sbom","status":status,"summary":f"{len(sb)} SBOM file(s); {len(ls)} lockfile(s) detected.","details":[f"SBOM: {v}" for v in sb]+[f"Lockfile: {v}" for v in ls],"limitations":["Discovery only; does not generate/validate SBOM or query vulnerability databases."]}
 print(json.dumps(o) if x.json else o);return 0
if __name__=="__main__":raise SystemExit(main())
