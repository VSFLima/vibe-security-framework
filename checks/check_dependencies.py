#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

MANIFESTS = {
 "package.json": ["package-lock.json","npm-shrinkwrap.json","yarn.lock","pnpm-lock.yaml"],
 "pyproject.toml": ["poetry.lock","uv.lock","pdm.lock"],
 "requirements.txt": [],
 "pubspec.yaml": ["pubspec.lock"],
 "Cargo.toml": ["Cargo.lock"],
 "go.mod": ["go.sum"],
 "Gemfile": ["Gemfile.lock"],
 "composer.json": ["composer.lock"],
 "pom.xml": [],
 "build.gradle": [],
 "build.gradle.kts": [],
}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--target",default="."); ap.add_argument("--json",action="store_true")
    a=ap.parse_args(); root=Path(a.target).resolve()
    found=[]; warnings=[]
    for name, locks in MANIFESTS.items():
        for p in root.rglob(name):
            if any(x in p.parts for x in ("node_modules","vendor",".git","build",".dart_tool")): continue
            found.append(str(p.relative_to(root)))
            if locks and not any((p.parent/l).exists() for l in locks):
                warnings.append(f"{p.relative_to(root)}: expected lockfile not found ({', '.join(locks)})")
    if not found:
        status="WARN"; summary="No supported dependency manifest found."
    elif warnings:
        status="WARN"; summary=f"{len(found)} manifest(s) found; {len(warnings)} lockfile warning(s)."
    else:
        status="PASS"; summary=f"{len(found)} manifest(s) found; expected lockfiles present where defined."
    out={"check":"dependencies","status":status,"summary":summary,
         "details":[f"Manifest: {x}" for x in found]+warnings,
         "limitations":["Inventory/lockfile check only.",
                        "Does NOT query vulnerability databases and cannot prove dependencies are vulnerability-free.",
                        "Use ecosystem/SBOM vulnerability scanners in CI for control 54."]}
    print(json.dumps(out,ensure_ascii=False) if a.json else out)
    return 0
if __name__=="__main__": raise SystemExit(main())
