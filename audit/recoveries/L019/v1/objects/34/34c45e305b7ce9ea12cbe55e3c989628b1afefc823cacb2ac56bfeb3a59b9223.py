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
for stem in ['topic_B_L019_faithful_augmentation_v1', 'topic_B_L019_faithful_augmentation_root_adoption', 'topic_B_L019_actual_wings_v1', 'topic_B_L019_actual_wings_root_adoption', 'topic_B_L019_initial_fracture_v1', 'topic_B_L019_initial_fracture_root_adoption', 'topic_B_L019_boundary_split_v1', 'topic_B_L019_boundary_split_root_adoption', 'topic_B_L019_split_inheritance_v2', 'topic_B_L019_split_inheritance_independent_review', 'topic_B_L019_endpoint_anchors_v1', 'topic_B_L019_endpoint_anchors_independent_review']:
 root=s/stem;p=root/'manifest.json';d=pin(p,'Complete acquired packet: '+stem);deps[str(p)]=d;acquired.append(d)
 for e in json.loads(p.read_text())['exports']:
  f=root/e['path'];q=pin(f,'Complete acquired export: '+stem);need(q['bytes']==e['bytes'] and q['sha256']==e['sha256'],'Mismatch: '+str(f));deps[str(f)]=q
for p in [s/'sources/stability2024.pdf',w.parent/'SnJanuary2023.tex']:deps[str(p)]=pin(p,'Exact primary original source')
(w/'dependencies.json').write_text(json.dumps(list(deps.values()),indent=2)+'\n');(w/'acquired_packets.json').write_text(json.dumps(acquired,indent=2)+'\n')
(w/'scope.json').write_text(json.dumps({'original':'L019','status':'BOUNDED_COMPONENT_ONLY','proved':['A fractured natural symmetric C-marking with n>=5 and 2r>n+2 has an internal perfect split with at least one trivial internal factor.','The initial-fracture theorem supplies the hypotheses for every natural symmetric marking with n>=7 in the same range.','The exceptional even wing is resolved by moving a split and, if necessary, intersecting two actual symmetric wings with opposite five-point ends.'],'unproved':['Actual leaf-kernel conditions and degree/rank extension','Reversible correspondence, canonical choice and duality','Exact base constants and complete original contract'],'whole_original_credit':0,'new_Lean':0,'measurement':None},indent=2)+'\n')
(w/'attribution.json').write_text(json.dumps({'author':'/root/l044_resume','borrowed':'Source Section 8 smaller-wing induction strategy, complete historical rank and finite classification premises retained through acquired packets, and all exact actual-wing/inheritance/anchor interfaces.','new_work':'Move the split in the critical even symmetric wing; a second failure of strict descent forces two opposite five-point ends. Actual symmetric-wing intersection and endpoint anchors close this case without quotient IP.','parent_contribution':'None to this new argument. Earlier paired-cut contribution remains explicitly attributed in acquired theory.','distinct_review':'pending','computation':'No new census; full written proof, exact binding checks and native compilation.'},indent=2)+'\n')
(w/'visual_review.json').write_text(json.dumps({'pages':3,'all_pages_directly_viewed':True,'result':'All final pages read and directly viewed; no clipping or unresolved references; changed numerical and actual-action hypotheses retained.','images':[pin(w/f'native-{i:02d}.png') for i in range(1,4)]},indent=2)+'\n')
(w/'README.rst').write_text('A trivial internal factor by moving the split\n=============================================\n\nRead trivial_factor.pdf and scope.json for the precise theorem.\nAll small classification and actual-action interfaces are acquired.\nbuild.py is the bounded native replay; freeze.py is historical only.\nLeaf kernels, the full correspondence and whole L019 remain pending.\n')
d=s/'topic_B_L019_trivial_factor_v1';need(not d.exists(),'Immutable destination exists');d.mkdir()
for p in sorted(w.iterdir()):
 if p.is_file() and p.suffix not in ['.aux','.out','.log'] and not p.name.startswith('native-'):shutil.copy2(p,d/p.name)
exports=[]
for p in sorted(d.iterdir()):
 q=pin(p);q['path']=p.name;exports.append(q)
(d/'manifest.json').write_text(json.dumps({'status':'AUTHOR_FROZEN_BOUNDED_L019_TRIVIAL_FACTOR','exports':exports,'whole_original_credit':0,'new_question_credit':0},indent=2)+'\n');print(json.dumps({'manifest':pin(d/'manifest.json'),'exports':len(exports),'dependencies':len(deps)}))
