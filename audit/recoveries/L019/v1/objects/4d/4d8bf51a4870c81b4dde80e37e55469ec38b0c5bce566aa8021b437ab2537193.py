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
for name in ['topic_B_L019_orbit_budgets_v2','topic_B_L019_orbit_budgets_independent_review','topic_B_L019_orbit_budgets_root_adoption','topic_B_L044_paired_cut_lemma_v1','topic_B_L044_paired_cut_independent_review','topic_B_L044_paired_cut_root_adoption']:
 root=s/name;p=root/'manifest.json';d=pin(p,'Complete acquired interface: '+name);deps[str(p)]=d;acquired.append(d)
 for e in json.loads(p.read_text())['exports']:
  f=root/e['path'];q=pin(f,'Complete acquired export: '+name);need(q['bytes']==e['bytes'] and q['sha256']==e['sha256'],'Mismatch: '+str(f));deps[str(f)]=q
for p,role in [(s/'sources/stability2024.pdf','Exact original L019 source'),(w.parent/'SnJanuary2023.tex','Exact primary source TeX'),(s/'topic_B_L019_faithful_augmentation_v1/faithful_augmentation.tex','Earlier restricted interior inheritance proof, explicitly extended here')]:deps[str(p)]=pin(p,role)
(w/'dependencies.json').write_text(json.dumps(list(deps.values()),indent=2)+'\n');(w/'acquired_packets.json').write_text(json.dumps(acquired,indent=2)+'\n')
(w/'scope.json').write_text(json.dumps({'original':'L019','status':'BOUNDED_COMPONENT_ONLY','proved':['Parent intransitive maximal omissions imply actual wing maximal omissions are intransitive.','A nonadjacent perfect wing split inherits to the parent, including the terminal singleton case, preserving trivial internal factors.','If a wing of degree m and rank t has 2t>m-1 and its adjacent endpoint is a perfect split, that split inherits with a trivial near internal factor; the old factor on the far side is also trivial.'],'unproved':['Existence of the required internal wing split','Leaf-kernel conditions and complete reversible stability correspondence','All enumerative constants and full original contract'],'whole_original_credit':0,'new_question_credit':0,'new_Lean':0,'measurement':None},indent=2)+'\n')
(w/'attribution.json').write_text(json.dumps({'author':'/root/l044_resume','borrowed':'Source Section 8 inheritance mechanism and acquired actual unique-crossing/minimal-transitivity proofs. Earlier strictly interior inheritance proof remains attributed.','new_work':'Explicit ambient omission argument for all nonadjacent inherited splits, including a singleton far side; elementary actual pair-transitivity bound replaces the adjacent-case classification estimate.','parent_contribution':'None to the new inheritance proof. Historical paired-cut attribution remains in its acquired packet.','distinct_review':'pending','mathematical_computation':'None. Native build and exact dependency verification only.'},indent=2)+'\n')
(w/'visual_review.json').write_text(json.dumps({'pages':2,'all_pages_directly_viewed':True,'result':'Both final pages readable, all singleton and adjacent cases retained; no clipping or unresolved references.','images':[pin(w/f'native-{i:02d}.png') for i in range(1,3)]},indent=2)+'\n')
(w/'README.rst').write_text('Inheritance of perfect splits in actual wings\n============================================\n\nRead inheritance.pdf for the complete arguments and scope.json for their\nexact hypotheses. No finite census or formal declaration is involved.\nRun build.py in a writable copy for bounded native replay. freeze.py is a\nhistorical author-work helper, not a standalone replay interface.\nThe remaining existence and stability obligations are not credited here.\n')
dest=s/'topic_B_L019_split_inheritance_v1';need(not dest.exists(),'Immutable destination exists');dest.mkdir()
for p in sorted(w.iterdir()):
 if p.is_file() and p.suffix not in ['.aux','.out','.log'] and not p.name.startswith('native-'):shutil.copy2(p,dest/p.name)
exports=[]
for p in sorted(dest.iterdir()):
 d=pin(p);d['path']=p.name;exports.append(d)
(dest/'manifest.json').write_text(json.dumps({'status':'AUTHOR_FROZEN_BOUNDED_L019_SPLIT_INHERITANCE','exports':exports,'whole_original_credit':0,'new_question_credit':0},indent=2)+'\n');print(json.dumps({'manifest':pin(dest/'manifest.json'),'exports':len(exports),'dependencies':len(deps)}))
