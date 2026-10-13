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
names=['topic_B_L019_head_support_v1','topic_B_L019_head_support_independent_review','topic_B_L019_orbit_budgets_v2','topic_B_L019_orbit_budgets_independent_review','topic_B_L019_orbit_budgets_root_adoption','topic_B_L044_ambient_interval_v1','topic_B_L044_ambient_interval_root_review','topic_B_L044_paired_cut_lemma_v1','topic_B_L044_paired_cut_independent_review','topic_B_L044_paired_cut_root_adoption']
for name in names:
 root=s/name;p=root/'manifest.json';d=pin(p,'Complete acquired proof or acceptance: '+name);deps[str(p)]=d;acquired.append(d)
 for e in json.loads(p.read_text())['exports']:
  f=root/e['path'];q=pin(f,'Complete acquired export: '+name);need(q['bytes']==e['bytes'] and q['sha256']==e['sha256'],'Mismatch: '+str(f));deps[str(f)]=q
for p,role in [(s/'sources/stability2024.pdf','Exact original L019 source'),(w.parent/'SnJanuary2023.tex','Exact primary source TeX')]:deps[str(p)]=pin(p,role)
(w/'dependencies.json').write_text(json.dumps(list(deps.values()),indent=2)+'\n');(w/'acquired_packets.json').write_text(json.dumps(acquired,indent=2)+'\n')
(w/'scope.json').write_text(json.dumps({'original':'L019','status':'BOUNDED_COMPONENT_ONLY','proved':['Under transitivity, connected string noncommutation, all maximal omissions intransitive and 2r>n+2, a perfect split exists.','Two separated unique cuts with the stated support orientations give n>=2r+h-g.','The actual maximal/minimal cut routing proves the two support budgets with reverse index r-1-g and establishes the union before summation.'],'unproved':['Existence of an internal split with one trivial internal factor','The full degree/rank bijection','The six enumerative constants and complete source contract'],'whole_original_credit':0,'new_question_credit':0,'new_Lean':0,'measurement':None},indent=2)+'\n')
(w/'attribution.json').write_text(json.dumps({'author':'/root/l044_resume','borrowed':'Cameron-Fernandes-Leemans Section 5 fracture/support-overlap strategy and earlier alternating source. Complete acquired paired-cut, fixed-prefix and ambient-interval proofs are paid inputs.','new_work':'Parity-free actual-orbit support bounds, explicit orientation at the second cut, and separated three-region count replace equality classification in the strict range.','parent_contribution':'None to this assembly. The acquired paired-cut global middle-colour exchange retains its root mathematical contribution and distinct review.','distinct_review':'pending','computation':'Only native build and dependency integrity; no finite mathematical premise.'},indent=2)+'\n')
(w/'visual_review.json').write_text(json.dumps({'pages':3,'all_pages_directly_viewed':True,'result':'All three pages readable; correct reversed indices and all support orientations explicit; no clipping or unresolved references.','images':[pin(w/f'native-{i:02d}.png') for i in range(1,4)]},indent=2)+'\n')
(w/'README.rst').write_text('A perfect split from two support bounds\n======================================\n\nRead perfect_split.pdf for the complete generic theorem. The precise scope\nand all paid proof interfaces are in scope.json and dependencies.json.\nRun build.py in a writable copy for bounded native replay. freeze.py is a\nhistorical author-work helper, not a standalone replay interface.\nThe stability bijection and complete original remain separate obligations.\n')
dest=s/'topic_B_L019_perfect_split_v1';need(not dest.exists(),'Immutable destination exists');dest.mkdir()
for p in sorted(w.iterdir()):
 if p.is_file() and p.suffix not in ['.aux','.out','.log'] and not p.name.startswith('native-'):shutil.copy2(p,dest/p.name)
exports=[]
for p in sorted(dest.iterdir()):
 d=pin(p);d['path']=p.name;exports.append(d)
(dest/'manifest.json').write_text(json.dumps({'status':'AUTHOR_FROZEN_BOUNDED_L019_PERFECT_SPLIT','exports':exports,'whole_original_credit':0,'new_question_credit':0},indent=2)+'\n');print(json.dumps({'manifest':pin(dest/'manifest.json'),'exports':len(exports),'dependencies':len(deps)}))
