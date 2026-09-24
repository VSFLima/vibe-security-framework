import json,subprocess,sys,tempfile
from pathlib import Path
G=Path(__file__).resolve().parents[1]/"ci"/"evaluate_gate.py"
def run(status,policy="strict"):
 with tempfile.TemporaryDirectory() as td:
  p=Path(td)/"e.json";p.write_text(json.dumps({"check_id":"x","status":status,"findings":[]}))
  return subprocess.run([sys.executable,str(G),"--policy",policy,"--evidence",str(p)],capture_output=True,text=True)
def main():
 assert run("PASS").returncode==0
 assert run("FAIL").returncode==1
 assert run("ERROR").returncode==1
 assert run("NOT_AVAILABLE").returncode!=0
 assert run("NOT_RUN").returncode!=0
 assert run("NOT_AVAILABLE","advisory").returncode==0
 print(json.dumps({"suite":"gate-policy","status":"PASS","tests":6}))
if __name__=="__main__":main()
