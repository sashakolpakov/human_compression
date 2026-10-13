"""Historical author-work freezer; build.py is directory-local replay."""
import hashlib,json,shutil,sys
from pathlib import Path
if sys.flags.optimize:raise SystemExit('optimized Python is unsupported')
w=Path(__file__).resolve().parent;s=w.parents[2]
def need(p,message):
 if not p:raise ValueError(message)
def pin(p,role=None):
 q={'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if role:q['role']=role
 return q
deps={};acquired=[]
for name,role in [('topic_B_L019_orbit_budgets_v2','Minimal-transitivity lemma and actual essentiality; all other statements retained'),('topic_B_L019_orbit_budgets_independent_review','Distinct acceptance of exact v2'),('topic_B_L044_single_crossing_v1','Only generic fixed-prefix and no-gap Lemmas 1 and 2 used; full manuscript retained'),('topic_B_L044_single_crossing_root_review','Review of complete acquired fixed-prefix manuscript'),('topic_B_L044_paired_cut_lemma_v1','Actual unique-crossing interface'),('topic_B_L044_paired_cut_independent_review','Distinct review of acquired orbit-cut proof'),('topic_B_L044_paired_cut_root_adoption','Root adoption of acquired orbit-cut proof')]:
 root=s/name;p=root/'manifest.json';d=pin(p,role);deps[str(p)]=d;acquired.append(d)
 for item in json.loads(p.read_text())['exports']:
  f=root/item['path'];q=pin(f,'Complete acquired export: '+name)
  need(q['sha256']==item['sha256'] and q['bytes']==item['bytes'],'Export mismatch: '+str(f));deps[str(f)]=q
for rel,role in [('sources/stability2024.pdf','Exact original L019 source'),('reboot_20261013/L019_recovery_work/SnJanuary2023.tex','Exact original source TeX'),('topic_B_L044_internal_block_v2/internal_orbit_block.tex','Earlier internal-action proof, fully reworked with actual minimal transitivity'),('topic_B_L044_orbit_distance_v1/orbit_distance_deficit.tex','Earlier orbit-distance proof, reworked without parity equality exclusions'),('topic_B_L044_transitive_side_v1/transitive_side_deficit.tex','Earlier transitive-side strategy, bound reproved here')]:
 p=s/rel;deps[str(p)]=pin(p,role)
(w/'dependencies.json').write_text(json.dumps(list(deps.values()),indent=2)+'\n')
(w/'acquired_packets.json').write_text(json.dumps(acquired,indent=2)+'\n')
(w/'scope.json').write_text(json.dumps({'original':'L019','status':'BOUNDED_COMPONENT_ONLY','proved':['Actual commuting-orbit counts and internal distance-two pair count without parity or IP.','An outside side acted on by index h after a unique cut i has at least i+h+1 points.','If the final mark acts on the first side of a positive cut, n >= 2r; an endpoint shared final mark has the same bound.','For 2r > n+2, the final tail after the last shared h is supported on the prescribed side and fixes at least 2h+1 points.'],'unproved':['Existence of a perfect split','Complete degree/rank stability bijection and constants'],'whole_original_credit':0,'new_question_credit':0,'new_Lean':0,'measurement':None},indent=2)+'\n')
(w/'attribution.json').write_text(json.dumps({'author':'/root/l044_resume','borrowed':'Source commuting-orbit and path strategy; complete acquired L044 fixed-prefix/no-gap proofs. Earlier internal-block, orbit-distance and transitive-side arguments remain explicitly attributed.','new_work':'Every altered hypothesis is proved using minimal transitivity on actual orbits. No quotient intersection property, alternating rank classification or parity equality exclusion is used.','parent_contribution':'None to the new support-count proof. Acquired paired-cut work retains its disclosed root contribution.','distinct_review':'pending','mathematical_computation':'None. Native TeX build and dependency verification only.'},indent=2)+'\n')
(w/'visual_review.json').write_text(json.dumps({'pages':3,'all_pages_directly_viewed':True,'result':'All final pages readable, all inequalities and case splits intact; no clipping or unresolved references.','images':[pin(w/f'native-{i:02d}.png') for i in range(1,4)]},indent=2)+'\n')
(w/'README.rst').write_text('Support bounds without a parity hypothesis\n==========================================\n\nThe full proof is in head_support.pdf and head_support.tex. Exact premises\nand deliberate equality boundaries are in scope.json and dependencies.json.\nThere is no finite mathematical calculation. Run build.py in a writable copy\nfor bounded native replay. freeze.py is a historical author-work helper and\nis not a standalone replay interface. The harmless initial helper path error\nis retained. No complete L019 principal recovery is claimed.\n')
dest=s/'topic_B_L019_head_support_v1';need(not dest.exists(),'Immutable destination exists');dest.mkdir()
for p in sorted(w.iterdir()):
 if p.is_file() and p.suffix not in ['.aux','.out','.log'] and not p.name.startswith('native-'):shutil.copy2(p,dest/p.name)
exports=[]
for p in sorted(dest.iterdir()):
 q=pin(p);q['path']=p.name;exports.append(q)
(dest/'manifest.json').write_text(json.dumps({'status':'AUTHOR_FROZEN_BOUNDED_L019_HEAD_SUPPORT','exports':exports,'whole_original_credit':0,'new_question_credit':0},indent=2)+'\n')
print(json.dumps({'manifest':pin(dest/'manifest.json'),'exports':len(exports),'dependencies':len(deps)}))
