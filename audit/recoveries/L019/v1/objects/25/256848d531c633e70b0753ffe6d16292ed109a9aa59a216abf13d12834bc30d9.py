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
groups=[
 ('topic_B_L047_candidate_v2','topic_B_L047_independent_review','topic_B_L047_root_adoption','Complete transitive rank classification and complete small extremal census'),
 ('corpus106_L044_principal_v1','corpus106_L044_principal_independent_review','corpus106_L044_principal_root_adoption','Complete exact alternating rank maxima'),
 ('topic_B_L044_pair_block_centralizers_v1','topic_B_L044_pair_block_centralizers_independent_review','topic_B_L044_pair_block_centralizers_root_adoption','Generic actual pair-centralizer lemma only'),
 ('topic_B_L044_symmetric_faithful_pairs_v1','topic_B_L044_symmetric_faithful_pairs_independent_review','topic_B_L044_symmetric_faithful_pairs_root_adoption','Complete literal S8 rank-six census'),
 ('corpus106_L071_alternating_v1','corpus106_L071_alternating_independent_review','corpus106_L071_alternating_root_adoption','Complete A11 census'),
 ('topic_B_L019_actual_wings_v1','topic_B_L019_actual_wings_independent_review','topic_B_L019_actual_wings_root_adoption','Exact extracted A11 tuples and unchanged permutation library')]
deps={};acquired=[]
for *names,role in groups:
    for name in names:
        root=s/name;p=root/'manifest.json';d=pin(p,role);deps[str(p)]=d;acquired.append(d)
        for item in json.loads(p.read_text())['exports']:
            f=root/item['path'];q=pin(f,'Complete acquired export: '+name)
            need(q['sha256']==item['sha256'] and q['bytes']==item['bytes'],'Acquired export mismatch: '+str(f))
            deps[str(f)]=q
need((w/'permutation_library.py').read_bytes()==(s/'topic_B_L019_actual_wings_v1/check_wings.py').read_bytes(),'Changed reused library')
for p,role in [(s/'sources/stability2024.pdf','Exact original source'),(w.parent/'SnJanuary2023.tex','Exact source TeX')]:deps[str(p)]=pin(p,role)
(w/'dependencies.json').write_text(json.dumps(list(deps.values()),indent=2)+'\n')
(w/'acquired_packets.json').write_text(json.dumps(acquired,indent=2)+'\n')
(w/'scope.json').write_text(json.dumps({'original':'L019','status':'BOUNDED_COMPONENT_ONLY','proved':['For n >= 7 and 2r > n+2, every actual transitive C-marking generates natural Sn and all maximal omissions are intransitive.','A crossing edge of each label always gives a forest.','For n=5,6 the ordinary simplex representative has that property; arbitrary degree-six actions are explicitly not covered.'],'unproved':['Perfect-split existence','All valid extension and contraction interfaces','Principal stability bijection and constants'],'whole_original_credit':0,'new_question_credit':0,'new_Lean':0,'measurement':None},indent=2)+'\n')
(w/'attribution.json').write_text(json.dumps({'author':'/root/l044_resume','new_arguments':'Actual wreath omission exclusion with an unnormalized complement; complete small boundary filtering; explicit outer-S6 action qualification.','borrowed':'Source Proposition4.1 strategy and fracture construction, complete accepted L047/L044 classifications, generic L044 pair-centralizer lemma, exact accepted S8 and A11 censuses.','reused_code':'permutation_library.py is byte-identical to accepted actual_wings_v1/check_wings.py. No census rerun.','parent_contribution':'No mathematical contribution to this component. Parent requested precise actual hypotheses throughout L019.','distinct_review':'pending'},indent=2)+'\n')
(w/'visual_review.json').write_text(json.dumps({'pages':3,'all_pages_directly_viewed':True,'result':'Every final page readable; no clipping or unresolved reference; actual block kernel, eight centralizers and precise action qualification checked.','images':[pin(w/('native-%02d.png'%i)) for i in range(1,4)]},indent=2)+'\n')
(w/'README.rst').write_text('Fracture graphs in the strict high-rank range\n===========================================\n\nRead initial_fracture.pdf and scope.json. This is a bounded L019 component.\nAll acquired theorem and complete census scopes are bound in dependencies.json.\nThe literal check is check_boundaries.py --output report.json; the separate\nGAP check is gap -q -b gap_boundaries.g. prepare_checks.py replays both, checks\nthe exact arrays and five negative controls, and builds the native manuscript.\nThe first comparison CR issue and first TeX alignment error are retained.\nNo mathematical result depended on either failed formatting stage.\n')
dest=s/'topic_B_L019_initial_fracture_v1';need(not dest.exists(),'Immutable destination exists');dest.mkdir()
excluded={'initial_fracture.aux','initial_fracture.out','initial_fracture.log','probe.py','probe.json'}
for f in sorted(w.iterdir()):
    if f.is_file() and f.name not in excluded and not f.name.startswith('native-'):shutil.copy2(f,dest/f.name)
exports=[]
for f in sorted(dest.iterdir()):
    q=pin(f);q['path']=f.name;exports.append(q)
(dest/'manifest.json').write_text(json.dumps({'status':'AUTHOR_FROZEN_BOUNDED_L019_INITIAL_FRACTURE','exports':exports,'whole_original_credit':0,'new_question_credit':0},indent=2)+'\n')
print(json.dumps({'manifest':pin(dest/'manifest.json'),'exports':len(exports),'dependencies':len(deps)}))
