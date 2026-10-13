import hashlib
import json
from pathlib import Path
import shutil
import sys

if sys.flags.optimize:
    raise SystemExit("optimized Python is unsupported")

def need(p,message):
    if not p:raise ValueError(message)

def pin(p,role=None):
    d={"path":str(p),"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
    if role:d["role"]=role
    return d

w=Path(__file__).resolve().parent;s=w.parents[2]
packets=[
 ("topic_B_L019_actual_wings_v1","Actual perfect-split support and symmetric-wing theorem; literal permutation library"),
 ("topic_B_L019_actual_wings_independent_review","Distinct mathematical review of actual wings"),
 ("topic_B_L019_actual_wings_root_adoption","Root adoption of actual wings"),
 ("topic_B_L047_candidate_v2","Complete exact primitive rank bound and its twelve literal exceptions"),
 ("topic_B_L047_independent_review","Distinct complete L047 review"),
 ("topic_B_L047_root_adoption","Root complete L047 adoption")]
deps={};acquired=[]
for name,role in packets:
    root=s/name;p=root/"manifest.json";d=pin(p,role);deps[str(p)]=d;acquired.append(d)
    for item in json.loads(p.read_text())["exports"]:
        f=root/item["path"];q=pin(f,"Complete acquired export: "+name)
        need(q["sha256"]==item["sha256"] and q["bytes"]==item["bytes"],"Acquired export mismatch: "+str(f))
        deps[str(f)]=q
need((w/"permutation_library.py").read_bytes()==(s/"topic_B_L019_actual_wings_v1/check_wings.py").read_bytes(),"Changed reused permutation library")
for p,role in [(s/"sources/stability2024.pdf","Exact original source"),(w.parent/"SnJanuary2023.tex","Exact original source TeX")]:deps[str(p)]=pin(p,role)
(w/"dependencies.json").write_text(json.dumps(list(deps.values()),indent=2)+"\n")
(w/"acquired_packets.json").write_text(json.dumps(acquired,indent=2)+"\n")
scope={"original":"L019","status":"BOUNDED_COMPONENT_ONLY","proved":[
 "With an actual symmetric wing and two nontrivial internal factors, the opposite augmented action is faithfully a primitive C-group with the specified nontrivial C2 character.",
 "The augmented image is neither natural alternating nor natural symmetric.",
 "The symmetric wing satisfies the same strict high-rank inequality, except precisely the stated even-degree rank-half-plus-one reduction with a degree-six S5 attachment of type [6,5] or [4,5].",
 "Every strictly interior perfect split of the wing lifts with its internal factors unchanged."],
 "unproved":["Exclusion or resolution of the residual even-degree case","General interior-perfect-split existence","Leaf-kernel tests throughout the stability range","Complete stability bijection and constants"],
 "whole_original_credit":0,"new_question_credit":0,"new_Lean":0,"measurement":None}
(w/"scope.json").write_text(json.dumps(scope,indent=2)+"\n")
(w/"attribution.json").write_text(json.dumps({"author":"/root/l044_resume","new_arguments":"Faithful augmented restriction using the actual IP kernel, the C2 character contradiction, and exact boundary filtering.","borrowed":"Complete primitive rank classification through the reviewed L047 recovery; actual symmetric-wing theorem; elementary support inheritance from the source, proved fully here.","reused_code":"permutation_library.py is byte-identical to check_wings.py in accepted actual_wings_v1.","parent_contribution":"Requested exact hypotheses and exception inventory in the preceding component. No new mathematical contribution to this component.","distinct_review":"pending"},indent=2)+"\n")
(w/"visual_review.json").write_text(json.dumps({"pages":3,"all_pages_directly_viewed":True,"result":"All final pages readable; displayed permutations, character argument and inequalities checked. No clipping or unresolved references.","images":[pin(w/("native-%02d.png"%i)) for i in range(1,4)]},indent=2)+"\n")
(w/"README.rst").write_text("Faithful augmentation at a symmetric wing\n========================================\n\nRead faithful_augmentation.pdf and scope.json. This is a bounded component,\nnot a complete L019 principal recovery. It retains the exact unresolved\neven-degree case. dependencies.json binds the acquired complete theorem inputs.\n\nThe finite filter runs with check_primitive_boundary.py --output report.json;\nits reused literal-permutation library has unchanged accepted bytes.\nThe separate GAP replay is gap -q -b gap_boundary.g.\nNo new census was run; these tests filter twelve complete retained exceptions.\n")
dest=s/"topic_B_L019_faithful_augmentation_v1";need(not dest.exists(),"Immutable destination exists");dest.mkdir()
excluded={"faithful_augmentation.aux","faithful_augmentation.out","faithful_augmentation.log","primitive_boundary_diagnostic.py","primitive_boundary_diagnostic.json"}
for f in sorted(w.iterdir()):
    if f.is_file() and f.name not in excluded and not f.name.startswith("native-"):shutil.copy2(f,dest/f.name)
exports=[]
for f in sorted(dest.iterdir()):
    q=pin(f);q["path"]=f.name;exports.append(q)
(dest/"manifest.json").write_text(json.dumps({"status":"AUTHOR_FROZEN_BOUNDED_L019_FAITHFUL_AUGMENTATION","exports":exports,"whole_original_credit":0,"new_question_credit":0},indent=2)+"\n")
print(json.dumps({"manifest":pin(dest/"manifest.json"),"exports":len(exports),"dependencies":len(deps)}))
