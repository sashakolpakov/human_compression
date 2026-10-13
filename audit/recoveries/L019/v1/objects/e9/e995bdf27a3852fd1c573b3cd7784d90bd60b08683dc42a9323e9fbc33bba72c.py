import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

if sys.flags.optimize:
    raise SystemExit("optimized Python is unsupported")

def need(p,message):
    if not p:
        raise ValueError(message)

w=Path(__file__).resolve().parent;s=w.parents[2]
source=s/"topic_B_L047_candidate_v2/finite_results.json"
rows=json.loads(source.read_text())["primitive_markings"]["literal_solutions"]
data={"representatives":[{"source_index":i,"n":r["n"],"id":r["id"],"types":r["types"],"permutations":r["permutations"]} for i,r in enumerate(rows)]}
(w/"primitive_inputs.json").write_text(json.dumps(data,indent=2)+"\n")
(w/"extraction.json").write_text(json.dumps({"source":str(source),"sha256":hashlib.sha256(source.read_bytes()).hexdigest(),"rule":"Copy every primitive_markings.literal_solutions record in order; no filtering.","count":len(rows)},indent=2)+"\n")
gap="rows:="+json.dumps([r["permutations"] for r in rows])+";;\n"
gap+=r'''
ReplayPrimitiveBoundary:=function()
local k,row,marks,orientation,n,tail,points,a,G,C,images,hom,found;
C:=CyclicGroup(2);found:=[];
for k in [1..Length(rows)] do
 row:=rows[k];n:=Length(row[1]);marks:=List(row,PermList);
 for orientation in [0,1] do
  if orientation=1 then marks:=Reversed(marks);fi;
  G:=Group(marks);tail:=Group(marks{[2..Length(marks)]});
  images:=List(marks,x->One(C));images[1]:=GeneratorsOfGroup(C)[1];
  hom:=GroupHomomorphismByImages(G,C,marks,images);
  points:=Filtered([1..n],a->a^marks[1]<>a and ForAll(marks{[2..Length(marks)]},x->a^x=a));
  for a in points do
   if IsTransitive(tail,Difference([1..n],[a])) and hom<>fail then
    if [n,Length(marks),Size(G),Size(tail),a]<>[6,3,120,10,1] then Error("wrong primitive boundary");fi;
    Add(found,[k-1,orientation]);
   fi;
  od;
 od;
od;
if found<>[[3,1],[4,1],[6,0],[8,0]] then Error("wrong surviving list");fi;
Print("PASS_PRIMITIVE12_ORIENTATIONS24_SURVIVORS4_TYPES2\n");
end;
ReplayPrimitiveBoundary();QUIT_GAP(0);
'''
(w/"gap_boundary.g").write_text(gap)
env=os.environ.copy();env.pop("PYTHONOPTIMIZE",None);receipts=[]
def run(tag,args,success=True,extra=None):
    e=env.copy()
    if extra:e.update(extra)
    start=time.monotonic();p=subprocess.run(args,cwd=w,env=e,capture_output=True,timeout=120)
    (w/(tag+".stdout")).write_bytes(p.stdout);(w/(tag+".stderr")).write_bytes(p.stderr)
    need((p.returncode==0)==success,"unexpected exit: "+tag)
    receipts.append({"tag":tag,"args":args,"returncode":p.returncode,"seconds":time.monotonic()-start,"deadline_seconds":120})
    return p
run("direct",[sys.executable,"check_primitive_boundary.py","--output","direct_report.json"])
p=run("gap",["/opt/homebrew/bin/gap","-q","-b","gap_boundary.g"])
need(not p.stderr and p.stdout.decode().strip()=="PASS_PRIMITIVE12_ORIENTATIONS24_SURVIVORS4_TYPES2","unclean GAP result")
for name,mutate in [("missing_case",lambda d:d["representatives"].pop()),("bad_permutation",lambda d:d["representatives"][0]["permutations"][0].__setitem__(0,99))]:
    bad=copy.deepcopy(data);mutate(bad);(w/(name+".json")).write_text(json.dumps(bad))
    run(name,[sys.executable,"check_primitive_boundary.py","--input",name+".json","--output",name+".report.json"],False)
run("optimization_argument",[sys.executable,"-O","check_primitive_boundary.py","--output","optimization.report.json"],False)
run("optimization_environment",[sys.executable,"check_primitive_boundary.py","--output","optimization_env.report.json"],False,{"PYTHONOPTIMIZE":"1"})
(w/"check_receipts.json").write_text(json.dumps(receipts,indent=2)+"\n")
print("PASS: direct/GAP primitive filtering and four negative controls")
