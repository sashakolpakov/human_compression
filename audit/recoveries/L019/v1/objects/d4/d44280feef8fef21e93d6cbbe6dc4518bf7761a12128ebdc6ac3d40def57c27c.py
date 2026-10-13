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
for stem in ['topic_B_rank_extension_repair','topic_B_rank_extension_repair_root_review']:
 root=s/stem;p=root/'manifest.json';d=pin(p,'Complete acquired packet: '+stem);deps[str(p)]=d;acquired.append(d)
 for e in json.loads(p.read_text())['exports']:
  f=root/e['path'];q=pin(f,'Complete acquired export: '+stem);need(q['bytes']==e['bytes'] and q['sha256']==e['sha256'],'Mismatch: '+str(f));deps[str(f)]=q
for p in [s/'sources/stability2024.pdf',w.parent/'SnJanuary2023.tex']:deps[str(p)]=pin(p,'Exact primary original source')
(w/'dependencies.json').write_text(json.dumps(list(deps.values()),indent=2)+'\n');(w/'acquired_packets.json').write_text(json.dumps(acquired,indent=2)+'\n')
(w/'scope.json').write_text(json.dumps({'original':'L019','status':'BOUNDED_COMPONENT_ONLY','proved':['Two transitive root orbits meeting at one point generate their supported alternating group; an odd element supported on one whole side yields the supported symmetric group.','An external disjoint-label transitive group proves all even leaf-kernel inclusions through original IP; if it is odd, all full leaf conditions hold.','Any remaining failed kernel inclusion has exactly an index-two sign defect.','A usable internal split with both attaching groups odd has a valid rank/degree extension generating the next symmetric group.'],'unproved':['Existence of a suitable odd split throughout the high-rank range or exclusion of the remaining sign defects','Reversible correspondence, canonical choice and duality','Exact base constants and complete original contract'],'whole_original_credit':0,'new_Lean':0,'measurement':None},indent=2)+'\n')
(w/'attribution.json').write_text(json.dumps({'author':'/root/l044_resume','borrowed':'Source rank/degree construction and the complete separately reviewed restriction-kernel repair, including the standard end criterion and central twist attribution.','new_work':'External attaching group and original IP imply supported alternating kernel inclusion, and full kernel inclusion when an odd element is present. The only possible residual is identified exactly as a sign quotient of order two.','parent_contribution':'None to the new argument.','distinct_review':'pending','computation':'No finite census or computational premise; written permutation identities and native build only.'},indent=2)+'\n')
(w/'visual_review.json').write_text(json.dumps({'pages':2,'all_pages_directly_viewed':True,'result':'All final pages read and directly viewed; no clipping or unresolved references; changed numerical and actual-action hypotheses retained.','images':[pin(w/f'native-{i:02d}.png') for i in range(1,3)]},indent=2)+'\n')
(w/'README.rst').write_text('Odd permutations at an attachment\n==================================\n\nRead odd_attachment.pdf and scope.json. The complete acquired kernel\ncriterion is retained. This is a sufficient extension theorem, with\nthe remaining sign obstruction stated explicitly. build.py supplies\nbounded native replay; freeze.py is historical author-work tooling.\nWhole L019 remains pending.\n')
d=s/'topic_B_L019_odd_attachment_v1';need(not d.exists(),'Immutable destination exists');d.mkdir()
for p in sorted(w.iterdir()):
 if p.is_file() and p.suffix not in ['.aux','.out','.log'] and not p.name.startswith('native-'):shutil.copy2(p,d/p.name)
exports=[]
for p in sorted(d.iterdir()):
 q=pin(p);q['path']=p.name;exports.append(q)
(d/'manifest.json').write_text(json.dumps({'status':'AUTHOR_FROZEN_BOUNDED_L019_ODD_ATTACHMENT','exports':exports,'whole_original_credit':0,'new_question_credit':0},indent=2)+'\n');print(json.dumps({'manifest':pin(d/'manifest.json'),'exports':len(exports),'dependencies':len(deps)}))
