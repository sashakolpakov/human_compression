"""Historical author-work helper; only build.py is directory-local replay."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
if sys.flags.optimize:raise SystemExit('optimized Python is unsupported')
def need(p,message):
    if not p:raise ValueError(message)
def pin(p,role=None):
    d={'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    if role:d['role']=role
    return d
w=Path(__file__).resolve().parent;s=w.parents[2]
deps={};acquired=[]
for name in ['topic_B_L044_paired_cut_lemma_v1','topic_B_L044_paired_cut_independent_review','topic_B_L044_paired_cut_root_adoption']:
    root=s/name;p=root/'manifest.json';d=pin(p,'Complete generic orbit-cut and unique-crossing theorem/review');deps[str(p)]=d;acquired.append(d)
    for item in json.loads(p.read_text())['exports']:
        f=root/item['path'];q=pin(f,'Complete acquired export: '+name)
        need(q['sha256']==item['sha256'] and q['bytes']==item['bytes'],'Acquired export mismatch: '+str(f));deps[str(f)]=q
for p,role in [(s/'sources/stability2024.pdf','Exact original L019 source'),(w.parent/'SnJanuary2023.tex','Exact L019 source TeX'),(s/'topic_B_L044_block_deficits_v1/block_orbit_deficits.tex','Attribution comparison: actual orbit forest, fully reproved here'),(s/'topic_B_L044_two_point_orbit_v1/two_point_orbit.tex','Attribution comparison: primitive interval argument, fully reproved here')]:deps[str(p)]=pin(p,role)
(w/'dependencies.json').write_text(json.dumps(list(deps.values()),indent=2)+'\n')
(w/'acquired_packets.json').write_text(json.dumps(acquired,indent=2)+'\n')
(w/'scope.json').write_text(json.dumps({'original':'L019','status':'BOUNDED_COMPONENT_ONLY','proved':['Elementary minimal-transitivity forest and essentiality at a unique bridge.','Two imprimitive sides imply 2r <= n+2.','Two commuting factors each transitive on the opposite side, or with that side a singleton, satisfy the actual orbit product budget.','An interior singleton side implies 2r <= n+1; the two-point noninterval exception implies 2r <= n.','In the strict range a nonperfect split has a primitive interval side and an explicitly oriented shared label.'],'unproved':['General head-support transfer','Perfect-split existence','Complete stability bijection and constants'],'whole_original_credit':0,'new_question_credit':0,'new_Lean':0,'measurement':None},indent=2)+'\n')
(w/'attribution.json').write_text(json.dumps({'author':'/root/l044_resume','new_arguments':'Minimal transitivity on actual orbits replaces independent group generation and yields the parity-free two-factor budget.','borrowed':'Source fracture framework and split-side route; accepted actual contracted-orbit forest and elementary primitive normal-factor argument, all reproduced explicitly.','parent_contribution':'None to the new counting proof. Acquired paired-cut manuscript retains its disclosed root global-square contribution, which is not used by this packet.','distinct_review':'pending','computation':'None; only native TeX build and dependency integrity.'},indent=2)+'\n')
(w/'visual_review.json').write_text(json.dumps({'pages':3,'all_pages_directly_viewed':True,'result':'All final pages readable; no clipping or unresolved references. Minimal-transitivity transfer and degree-two boundary reviewed in full.','images':[pin(w/('native-%02d.png'%i)) for i in range(1,4)]},indent=2)+'\n')
(w/'README.rst').write_text('Counting generators by their actual orbit requirements\n=====================================================\n\nRead orbit_budgets.pdf and scope.json. The complete generic proof has no\nfinite census or software premise. build.py is a directory-local native\nbuild, with bounded children. Replay it in a writable copy of this immutable\npacket. freeze.py is a historical author-work helper and is not a replay\ninterface. Exact theorem dependencies and attribution comparisons are pinned\nin dependencies.json. No whole L019 principal recovery is claimed.\n')
dest=s/'topic_B_L019_orbit_budgets_v1';need(not dest.exists(),'Immutable destination exists');dest.mkdir()
excluded={'orbit_budgets.aux','orbit_budgets.out','orbit_budgets.log'}
for f in sorted(w.iterdir()):
    if f.is_file() and f.name not in excluded and not f.name.startswith('native-'):shutil.copy2(f,dest/f.name)
exports=[]
for f in sorted(dest.iterdir()):
    q=pin(f);q['path']=f.name;exports.append(q)
(dest/'manifest.json').write_text(json.dumps({'status':'AUTHOR_FROZEN_BOUNDED_L019_ORBIT_BUDGETS','exports':exports,'whole_original_credit':0,'new_question_credit':0},indent=2)+'\n')
print(json.dumps({'manifest':pin(dest/'manifest.json'),'exports':len(exports),'dependencies':len(deps)}))
