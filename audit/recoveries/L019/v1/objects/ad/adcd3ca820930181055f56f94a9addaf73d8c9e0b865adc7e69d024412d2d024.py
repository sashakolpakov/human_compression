"""Historical author-work freeze; check.py and build.py are local replay interfaces."""
from pathlib import Path
import hashlib,json,shutil,sys
if sys.flags.optimize:raise SystemExit('optimized Python is unsupported')
w=Path(__file__).resolve().parent;s=w.parents[2]
def need(x,m):
 if not x:raise ValueError(m)
def pin(p,role=None):
 b=p.read_bytes();r={'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 if role:r['role']=role
 return r
stems=['topic_B_L019_actual_wings_v1','topic_B_L019_actual_wings_independent_review','topic_B_L019_actual_wings_root_adoption','topic_B_L019_faithful_augmentation_v1','topic_B_L019_faithful_augmentation_independent_review','topic_B_L019_faithful_augmentation_root_adoption','topic_B_L044_small_maxima_v1','topic_B_L044_small_maxima_root_review','topic_B_L019_central_intersections_v1','topic_B_L019_central_intersections_root_review']
deps={};acquired=[]
for stem in stems:
 root=s/stem;m=root/'manifest.json';r=pin(m,'Complete acquired mathematical packet: '+stem);deps[str(m)]=r;acquired.append(r)
 for e in json.loads(m.read_text())['exports']:
  p=root/e['path'];r=pin(p,'Acquired export: '+stem);need(r['bytes']==e['bytes'] and r['sha256']==e['sha256'],'changed acquired export '+str(p));deps[str(p)]=r
for p in [s/'sources/stability2024.pdf',w.parent/'SnJanuary2023.tex']:
 deps[str(p)]=pin(p,'Exact primary original; source attribution only')
(w/'dependencies.json').write_text(json.dumps(list(deps.values()),indent=2)+'\n');(w/'acquired_packets.json').write_text(json.dumps(acquired,indent=2)+'\n')
(w/'scope.json').write_text(json.dumps({'original':'L019','status':'BOUNDED_COMPONENT_ONLY','proved':['No natural A10 rank5 marking with endpoint anchor and transitive complementary tail admits an outside involution attachment.','A primitive even actual C-marking with such an attachment has 2rank<=degree-1, except the degree6 rank3 A5 cases with D10 tail.','At a usable split with even augmented right group, the actual symmetric left wing lies in the strict smaller-degree range, except degree5 right side and critical even left wing.'],'finite_scope':'Filter complete previously accepted census; no new census. Ten terminal candidates include eight full A10 tuples and two order1920 groups; all four survivors generate A10.','remaining':['Critical even symmetric wing extension','Opposite even-wing configuration','Valid leaf kernels and reversible correspondence','Complete source principal contract and base constants'],'whole_original_credit':0,'new_Lean':0,'measurement':None},indent=2)+'\n')
(w/'attribution.json').write_text(json.dumps({'author':'/root/l044_resume','borrowed':'Complete L044 and L047 classification inputs, actual-wing exception tests, faithful-augmentation finite filter without its character assumption, and central-intersection obstruction. All original attributions retained.','new_work':'Four A10 attachment prefix obstructions and the exact even-primitive rank interface; direct and GAP filtering of unchanged complete input.','parent_contribution':'No new proof contribution. Parent requested exact exception inventory earlier; present work explicitly includes natural A10.','distinct_review':'pending','diagnostic_boundary':'The separate S12 example only rejects a proposed stronger oddness condition; it is not used as a premise of the three theorems.'},indent=2)+'\n')
(w/'visual_review.json').write_text(json.dumps({'pages':3,'all_pages_directly_viewed':True,'warnings':False,'images':[pin(w/f'native-{i:02d}.png') for i in range(1,4)]},indent=2)+'\n')
(w/'README.rst').write_text('An even attaching group\n=======================\n\nRead even_attachment.pdf and scope.json. This is a bounded descent reduction.\ncheck.py --out NEW_DIRECTORY replays the exact A10 filter with direct literal\nclosures and GAP, including four negative controls. build.py supplies native\nreplay in a writable copy. extract_a10.g and freeze.py are historical\nauthor-work helpers with the original work ancestry, not portable replay.\nThe complete accepted census and its full validation remain acquired.\nNo new census, whole L019, conjecture or Lean result is claimed.\n')
d=s/'topic_B_L019_even_attachment_v1';need(not d.exists(),'immutable destination exists');d.mkdir()
for p in sorted(w.rglob('*')):
 if not p.is_file() or '__pycache__' in p.parts or p.suffix in ['.aux','.out','.log'] or p.name.startswith('native-'):continue
 q=d/p.relative_to(w);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
probe=w.parent/'critical_even_twelve_probe01'
for p in sorted(probe.iterdir()):
 if p.is_file():q=d/'retained_diagnostic'/p.name;q.parent.mkdir(exist_ok=True);shutil.copy2(p,q)
exports=[]
for p in sorted(d.rglob('*')):
 if p.is_file():r=pin(p);r['path']=str(p.relative_to(d));exports.append(r)
(d/'manifest.json').write_text(json.dumps({'status':'AUTHOR_FROZEN_BOUNDED_L019_EVEN_ATTACHMENT','exports':exports,'whole_original_credit':0,'new_question_credit':0},indent=2)+'\n')
print(json.dumps({'manifest':pin(d/'manifest.json'),'exports':len(exports),'dependencies':len(deps)}))
