"""Historical author-work helper; build.py is directory-local replay."""
import hashlib,json,shutil,sys
from pathlib import Path
if sys.flags.optimize:raise SystemExit('optimized Python is unsupported')
w=Path(__file__).resolve().parent;s=w.parents[2]
def need(p,m):
 if not p:raise ValueError(m)
def pin(p,role=None):
 d={'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if role:d['role']=role
 return d
deps={};acquired=[]
for name in ['topic_B_L019_perfect_split_v1','topic_B_L019_perfect_split_independent_review','topic_B_L019_head_support_v1','topic_B_L019_head_support_independent_review','topic_B_L019_orbit_budgets_v2','topic_B_L019_orbit_budgets_independent_review','topic_B_L019_orbit_budgets_root_adoption','topic_B_L044_ambient_interval_v1','topic_B_L044_ambient_interval_root_review']:
 root=s/name;p=root/'manifest.json';d=pin(p,'Complete acquired interface and acceptance: '+name);deps[str(p)]=d;acquired.append(d)
 for e in json.loads(p.read_text())['exports']:
  f=root/e['path'];q=pin(f,'Complete acquired export: '+name);need(q['bytes']==e['bytes'] and q['sha256']==e['sha256'],'Mismatch: '+str(f));deps[str(f)]=q
for p,role in [(s/'sources/stability2024.pdf','Exact original L019 source'),(w.parent/'SnJanuary2023.tex','Exact primary source TeX'),(s/'topic_B_L044_block_deficits_v1/block_orbit_deficits.tex','Attribution comparison: earlier block/orbit saturation strategy; new proof does not assume its parity hypotheses')]:deps[str(p)]=pin(p,role)
(w/'dependencies.json').write_text(json.dumps(list(deps.values()),indent=2)+'\n');(w/'acquired_packets.json').write_text(json.dumps(acquired,indent=2)+'\n')
(w/'scope.json').write_text(json.dumps({'original':'L019','status':'BOUNDED_COMPONENT_ONLY','proved':['An inclusion-minimal transitivity family of maximum forest length on two orbits consists of single transpositions forming two trees.','For a unique cut with two imprimitive sides, equality 2r=n+2 forces the cut to be perfect.','The actual primitive-side and head-support interfaces extend to 2r>n+1, with each changed use audited.','Every transitive connected string action with all maximal omissions intransitive and 2r>n+1 has a perfect split.'],'unproved':['An internal perfect split with one trivial internal factor','Leaf-kernel conditions for the canonical extension','Complete stable bijection and six constants'],'whole_original_credit':0,'new_question_credit':0,'new_Lean':0,'measurement':None},indent=2)+'\n')
(w/'attribution.json').write_text(json.dumps({'author':'/root/l044_resume','borrowed':'Source block systems and support-overlap route; complete actual orbit-forest, fixed-prefix, head-support and ambient-interval proofs.','new_work':'Saturated minimal-transitivity forests control actual block images, then force one-sided support of every remaining mark. The positive middle orbit deficit or adjacent support overlap supplies the boundary unit.','parent_contribution':'None to the new saturation or boundary proof. The acquired paired-cut theory retains its disclosed root contribution through the strict split dependency.','distinct_review':'pending','mathematical_computation':'None. Native build and dependency integrity only.'},indent=2)+'\n')
(w/'visual_review.json').write_text(json.dumps({'pages':3,'all_pages_directly_viewed':True,'result':'All three final pages readable; actual-block/contracted-orbit distinction and all endpoint boundaries intact; no clipping or unresolved references.','images':[pin(w/f'native-{i:02d}.png') for i in range(1,4)]},indent=2)+'\n')
(w/'README.rst').write_text('Saturated orbit forests and the even-degree boundary\n===================================================\n\nThe complete proof is boundary_split.pdf and boundary_split.tex. Exact scope\nand all paid interfaces are retained in scope.json and dependencies.json.\nThere is no finite mathematical census. Run build.py in a writable copy for\nbounded native replay; freeze.py is a historical author-work helper only.\nThe remaining internal-split, extension and stability obligations are explicit.\n')
dest=s/'topic_B_L019_boundary_split_v1';need(not dest.exists(),'Immutable destination exists');dest.mkdir()
for p in sorted(w.iterdir()):
 if p.is_file() and p.suffix not in ['.aux','.out','.log'] and not p.name.startswith('native-'):shutil.copy2(p,dest/p.name)
exports=[]
for p in sorted(dest.iterdir()):
 d=pin(p);d['path']=p.name;exports.append(d)
(dest/'manifest.json').write_text(json.dumps({'status':'AUTHOR_FROZEN_BOUNDED_L019_BOUNDARY_SPLIT','exports':exports,'whole_original_credit':0,'new_question_credit':0},indent=2)+'\n');print(json.dumps({'manifest':pin(dest/'manifest.json'),'exports':len(exports),'dependencies':len(deps)}))
