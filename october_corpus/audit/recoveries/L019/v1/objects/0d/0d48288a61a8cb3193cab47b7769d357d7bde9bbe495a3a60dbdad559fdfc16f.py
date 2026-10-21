"""Historical author-work helper; build.py is the directory-local replay."""
from pathlib import Path
import hashlib,json,shutil,sys
if sys.flags.optimize:raise SystemExit('optimized Python is unsupported')
w=Path(__file__).resolve().parent;s=w.parents[2]
def need(p,m):
 if not p:raise ValueError(m)
def pin(p,role=None):
 d={'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if role:d['role']=role
 return d
deps={};acquired=[]
for stem in ['topic_B_L019_orbit_budgets_v2','topic_B_L019_orbit_budgets_root_adoption','topic_B_L019_boundary_split_v1','topic_B_L019_boundary_split_independent_review','topic_B_L019_boundary_split_root_adoption','topic_B_L019_perfect_split_v1','topic_B_L019_perfect_split_root_adoption','topic_B_L019_initial_fracture_v1','topic_B_L019_initial_fracture_root_adoption','topic_B_L019_actual_wings_v1','topic_B_L019_actual_wings_root_adoption','topic_B_L019_split_inheritance_v2','topic_B_L044_paired_cut_lemma_v1','topic_B_L044_paired_cut_root_adoption']:
 root=s/stem;p=root/'manifest.json';d=pin(p,'Complete acquired packet: '+stem);deps[str(p)]=d;acquired.append(d)
 for e in json.loads(p.read_text())['exports']:
  f=root/e['path'];q=pin(f,'Complete acquired export: '+stem);need(q['bytes']==e['bytes'] and q['sha256']==e['sha256'],'Mismatch: '+str(f));deps[str(f)]=q
for p in [s/'sources/stability2024.pdf',w.parent/'SnJanuary2023.tex']:deps[str(p)]=pin(p,'Exact primary original source')
(w/'dependencies.json').write_text(json.dumps(list(deps.values()),indent=2)+'\n');(w/'acquired_packets.json').write_text(json.dumps(acquired,indent=2)+'\n')
(w/'scope.json').write_text(json.dumps({'original':'L019','status':'BOUNDED_COMPONENT_ONLY','proved':['Odd-degree both-imprimitive equality at 2t=d+1 forces a perfect split under actual fracture hypotheses.','A fractured connected string action with endpoint anchors at both ends and 2t>d has a perfect split.','A natural symmetric C-marking with n>=7 and 2r>n+2 has an internal perfect split.'],'unproved':['Trivial internal factor','Actual leaf-kernel conditions and reversible correspondence','Exact base constants and complete original contract'],'pending_interface':'The acquired split-inheritance v2 is frozen and currently under distinct review. Final admission of this component remains conditional on that review.','whole_original_credit':0,'new_Lean':0,'measurement':None},indent=2)+'\n')
(w/'attribution.json').write_text(json.dumps({'author':'/root/l044_resume','borrowed':'Source Section 8 internal-split objective and the complete retained actual-wing, rank, fracture, orbit-budget, saturated-forest and inheritance proofs. Exact authorship and finite premises remain in acquired packets.','new_work':'Use of endpoint anchors to rule out a nonperfect primitive orientation, the odd parity equality giving saturation, and actual symmetric-wing intersection identifying the transitive middle group.','parent_contribution':'None to the new argument; prior paired-cut contribution remains attributed in its acquired packet.','distinct_review':'pending','computation':'No new finite census; exact binding checks and native build only.'},indent=2)+'\n')
(w/'visual_review.json').write_text(json.dumps({'pages':3,'all_pages_directly_viewed':True,'result':'All final pages read and directly viewed; no clipping or unresolved references; changed numerical and actual-action hypotheses retained.','images':[pin(w/f'native-{i:02d}.png') for i in range(1,4)]},indent=2)+'\n')
(w/'README.rst').write_text('Two endpoint anchors and an internal perfect split\n==================================================\n\nRead endpoint_anchors.pdf and scope.json for the precise conclusions.\nThe new arguments use actual orbits and intersections. No exceptional\ndiagram enumeration is invoked. build.py replays the native document\nin a writable copy. freeze.py is a historical work helper only.\nWhole L019, the trivial-factor and stability steps remain pending.\n')
d=s/'topic_B_L019_endpoint_anchors_v1';need(not d.exists(),'Immutable destination exists');d.mkdir()
for p in sorted(w.iterdir()):
 if p.is_file() and p.suffix not in ['.aux','.out','.log'] and not p.name.startswith('native-'):shutil.copy2(p,d/p.name)
exports=[]
for p in sorted(d.iterdir()):
 q=pin(p);q['path']=p.name;exports.append(q)
(d/'manifest.json').write_text(json.dumps({'status':'AUTHOR_FROZEN_BOUNDED_L019_ENDPOINT_ANCHORS','exports':exports,'whole_original_credit':0,'new_question_credit':0},indent=2)+'\n');print(json.dumps({'manifest':pin(d/'manifest.json'),'exports':len(exports),'dependencies':len(deps)}))
