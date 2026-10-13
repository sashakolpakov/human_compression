"""Run the small additional wing checks with explicit process boundaries."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import time

if sys.flags.optimize:
    raise SystemExit("optimized Python is unsupported")

def need(p, message):
    if not p:
        raise ValueError(message)

w = Path(__file__).resolve().parent
data = json.loads((w / "wing_inputs.json").read_text())
small = [r["permutations"] for r in data["small_exceptions"]]
large = [r["permutations"] for r in data["a11_rank_six"]]
gap = "small:= " + json.dumps(small) + ";;\nlarge:= " + json.dumps(large) + ";;\n"
gap += r'''
RunWingReplay:=function()
local row,marks,orientation,a,points,c,s,u,v,inter,middle,count;
for row in small do
 marks:=List(row,PermList);
 for orientation in [0,1] do
  if orientation=1 then marks:=Reversed(marks);fi;
  points:=Filtered([1..Length(row[1])],a->a^marks[1]<>a and ForAll(marks{[2..Length(marks)]},x->a^x=a));
  if Length(points)<>0 then Error("small exception has anchor");fi;
 od;
od;
count:=0;
for row in large do
 marks:=List(row,PermList);
 if Group(marks)<>AlternatingGroup(11) then Error("wrong large group");fi;
 for orientation in [0,1] do
  if orientation=1 then marks:=Reversed(marks);fi;
  points:=Filtered([1..11],a->a^marks[1]<>a and ForAll(marks{[2..6]},x->a^x=a));
  for a in points do
   count:=count+1;
   c:=Stabilizer(Centralizer(SymmetricGroup(11),Group(marks{[2..6]})),a);
   if Size(c)<>1 then Error("nontrivial centralizer");fi;
   s:=Concatenation([(a,12)],marks);
   u:=Group(s{[2..5]});v:=Group(s{[1..4]});inter:=Intersection(u,v);middle:=Group(s{[2..4]});
   if [Size(u),Size(v),Size(inter),Size(middle)]<>[5040,5040,360,60] then Error("wrong obstruction");fi;
  od;
 od;
od;
if count<>4 then Error("wrong anchor count");fi;
Print("PASS_WINGS_SMALL15_LARGE4_ANCHORS4\n");
end;
RunWingReplay();QUIT_GAP(0);
'''
(w / "gap_wings.g").write_text(gap)
env = os.environ.copy(); env.pop("PYTHONOPTIMIZE", None)
receipts = []
def run(tag, args, expected=0, extra_env=None):
    t = time.monotonic(); e = env.copy()
    if extra_env:
        e.update(extra_env)
    p = subprocess.run(args, cwd=w, env=e, capture_output=True, timeout=120)
    (w / (tag + ".stdout")).write_bytes(p.stdout)
    (w / (tag + ".stderr")).write_bytes(p.stderr)
    need((p.returncode == 0) == (expected == 0), "unexpected exit: " + tag)
    receipts.append({"tag": tag, "args": args, "returncode": p.returncode,
                     "seconds": time.monotonic()-t, "deadline_seconds": 120})
    return p
run("direct", [sys.executable, "check_wings.py", "--output", "direct_report.json"])
p = run("gap", ["/opt/homebrew/bin/gap", "-q", "-b", "gap_wings.g"])
need(not p.stderr and p.stdout.decode().strip() == "PASS_WINGS_SMALL15_LARGE4_ANCHORS4", "unclean GAP replay")
for name, mutate in (
    ("invalid_permutation", lambda d: d["a11_rank_six"][0]["permutations"][0].__setitem__(0, 99)),
    ("missing_representative", lambda d: d["a11_rank_six"].pop()),
    ("duplicate_representative", lambda d: d["a11_rank_six"].__setitem__(3, copy.deepcopy(d["a11_rank_six"][0]))),
):
    d = copy.deepcopy(data); mutate(d)
    path = w / (name + ".json"); path.write_text(json.dumps(d))
    run(name, [sys.executable, "check_wings.py", "--input", path.name, "--output", name + ".report.json"], expected=1)
run("optimization_argument", [sys.executable, "-O", "check_wings.py", "--output", "optimized.report.json"], expected=1)
run("optimization_environment", [sys.executable, "check_wings.py", "--output", "optimized_environment.report.json"], expected=1, extra_env={"PYTHONOPTIMIZE": "1"})
(w / "check_receipts.json").write_text(json.dumps(receipts, indent=2) + "\n")
print("PASS: direct and GAP replay, three malformed-input and two optimization controls")
