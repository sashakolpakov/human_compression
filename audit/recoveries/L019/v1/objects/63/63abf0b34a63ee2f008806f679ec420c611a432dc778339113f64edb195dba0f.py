"""Replay the bounded census and independent literal boundary checks."""
import sys
if sys.flags.optimize:raise RuntimeError("normal Python required")
import argparse,hashlib,json,os,shutil,subprocess,time
from pathlib import Path

def need(v,m):
    if not v:raise ValueError(m)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def checked_pin(p,r):
    need(p.is_file(),"missing binding: "+str(p))
    need(p.stat().st_size==r["bytes"] and digest(p)==r["sha256"],"changed binding: "+str(p))
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--out",type=Path,required=True);ap.add_argument("--study",type=Path);ap.add_argument("--render",action="store_true");a=ap.parse_args()
    here=Path(__file__).resolve().parent;out=a.out.resolve();need(not out.exists(),"fresh output directory required");out.mkdir(parents=True)
    manifest=json.loads((here/"manifest.json").read_text());deps=json.loads((here/"dependencies.json").read_text())
    for r in manifest["exports"]:checked_pin(here/r["path"],r)
    prefix=json.loads((here/"scope.json").read_text())["original_study"]
    for r in deps:
        p=Path(r["path"])
        if a.study and str(p).startswith(prefix+"/"):p=a.study/str(p)[len(prefix)+1:]
        checked_pin(p,r)
    env=os.environ.copy();env.pop("PYTHONOPTIMIZE",None);receipts=[]
    def run(name,args,cwd,success=True):
        start=time.monotonic();p=subprocess.run(args,cwd=cwd,env=env,capture_output=True,timeout=45)
        (out/(name+".stdout")).write_bytes(p.stdout);(out/(name+".stderr")).write_bytes(p.stderr)
        receipts.append({"name":name,"args":args,"returncode":p.returncode,"seconds":time.monotonic()-start,"deadline_seconds":45})
        (out/"receipts.json").write_text(json.dumps(receipts,indent=2)+"\n")
        if success:need(p.returncode==0 and not p.stderr,"execution failed: "+name)
        else:need(p.returncode!=0,"rejection failed: "+name)
        return p.stdout.decode().replace("\r","")
    cases=[(6,2,"n6k2"),(6,3,"n6k3"),(8,2,"n8k2"),(8,4,"n8k4"),(10,2,"n10k2"),(10,5,"n10k5"),(5,5,"positive_n5k5")]
    for n,k,name in cases:
        case=out/name;case.mkdir();driver=case/"run.g"
        driver.write_text("Read("+json.dumps(str(here/"anchor_wreath.g"))+");;\nRunAnchoredWreath("+str(n)+","+str(k)+");;\nQUIT;\n")
        actual=run(name,["gap","-q","-T",str(driver)],case)
        expected=(here/name/"stdout.log").read_text().replace("\r","")
        need(actual==expected and actual.count("COMPLETE_ANCHORED_EVEN_WREATH|")==1,"complete census receipt mismatch: "+name)
    literal=out/"literal.json"
    run("literal",[sys.executable,str(here/"verify_small.py"),"--out",str(literal)],out)
    need(json.loads(literal.read_text())==json.loads((here/"direct_report.json").read_text()),"independent literal report mismatch")
    actual=run("leaf_filter",["gap","-q","-T",str(here/"leaf_filter_v2.g")],out)
    need(actual==(here/"leaf_filter_v2.stdout").read_text().replace("\r","") and actual.count("COMPLETE_SMALL_EVEN_LEAF_FILTER")==1,"GAP kernel filter mismatch")
    for opt in ["-O","-OO"]:run("reject"+opt,[sys.executable,opt,str(here/"verify_small.py"),"--out",str(out/(opt+".json"))],out,False)
    run("reject_missing",[sys.executable,str(here/"verify_small.py"),"--input-dir",str(out/"absent"),"--out",str(out/"missing.json")],out,False)
    if a.render:
        native=out/"native";native.mkdir()
        for name in ["build.py","small_even.tex"]:shutil.copy2(here/name,native/name)
        run("native",[sys.executable,str(native/"build.py")],native)
    report={"status":"PASS_SMALL_EVEN_BOUNDARY","exports":len(manifest["exports"]),"dependencies":len(deps),"complete_wreath_cases":len(cases),"independent_literal_check":True,"optimization_and_missing_input_controls":3,"whole_original_credit":0}
    (out/"report.json").write_text(json.dumps(report,indent=2)+"\n");print(json.dumps(report))
if __name__=="__main__":main()
