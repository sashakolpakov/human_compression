"""Historical author-work freeze; build.py is the local native replay."""
from pathlib import Path
import hashlib,json,shutil,sys
if sys.flags.optimize: raise RuntimeError('normal Python required')
W=Path(__file__).resolve().parent;S=W.parents[2]
def need(v,m):
    if not v:raise RuntimeError(m)
def pin(p,role=None):
    b=p.read_bytes();r={'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    if role:r['role']=role
    return r
stems=[
'topic_B_L019_actual_wings_v1','topic_B_L019_actual_wings_independent_review','topic_B_L019_actual_wings_root_adoption',
'topic_B_L019_even_attachment_v1','topic_B_L019_even_attachment_root_review',
'topic_B_L019_odd_attachment_v2','topic_B_L019_odd_attachment_independent_review','topic_B_L019_odd_attachment_root_adoption',
'topic_B_L019_trivial_factor_v2','topic_B_L019_trivial_factor_independent_review','topic_B_L019_trivial_factor_root_adoption',
'topic_B_rank_extension_repair','topic_B_rank_extension_repair_root_review',
'topic_B_L044_singleton_completion_v1','topic_B_L044_singleton_completion_independent_review','topic_B_L044_singleton_completion_root_adoption',
'topic_B_L044_paired_ladder_v1','topic_B_L044_paired_ladder_independent_review','topic_B_L044_paired_ladder_root_adoption',
'topic_B_L044_equality_components_v1','topic_B_L044_paired_cut_lemma_v1','topic_B_L044_paired_cut_independent_review','topic_B_L044_paired_cut_root_adoption',
'corpus106_L044_principal_v1','corpus106_L044_principal_independent_review','corpus106_L044_principal_root_adoption']
deps={};acquired=[]
for stem in stems:
    p=S/stem;m=p/'manifest.json';q=pin(m,'Complete acquired packet '+stem);acquired.append(q);deps[str(m)]=q
    for r in json.loads(m.read_text())['exports']:
        f=p/r['path'];q=pin(f,'Acquired export '+stem)
        need(q['bytes']==r['bytes'] and q['sha256']==r['sha256'],'acquired binding '+str(f));deps[str(f)]=q
for p in [S/'sources/stability2024.pdf',W.parent/'SnJanuary2023.tex']:
    deps[str(p)]=pin(p,'Exact original source, attribution only')
(W/'dependencies.json').write_text(json.dumps(list(deps.values()),indent=2)+'\n')
(W/'acquired_packets.json').write_text(json.dumps(acquired,indent=2)+'\n')
(W/'scope.json').write_text(json.dumps({'original':'L019','status':'BOUNDED_CONDITIONAL_COMPONENT','proved':['An anchored transitive string marking has connected noncommutation diagram.','Every even transitive fractured anchored C-marking of degree at least12 has rank strictly below half its degree, using the complete acquired generic unique-crossing theorem and full paired ladder.','Internal pure or odd sufficient splits transport through an actual one-point factor intersection.','Conditional on sufficient splits at strictly smaller strict symmetric degrees, only an even critical symmetric factor meeting an even factor of degree6,8,10 and half-rank remains.'],'explicit_condition':'The strict smaller-degree sufficient-split induction hypothesis remains unproved at its critical step.','remaining':['The three small even attaching degrees and critical symmetric factor','All-case extension and reversible correspondence','Exact base count premises and whole L019'],'whole_original_credit':0,'new_question_credit':0,'new_Lean':0,'measurement':None,'new_computation':'None; no old census or classification rerun.'},indent=2)+'\n')
(W/'attribution.json').write_text(json.dumps({'author':'/root/l044_resume','borrowed':'Cameron--Fernandes--Leemans--Mixer alternating rank and paired-cut theory through the complete L044 recovery, with its full generic interfaces and reviews. Earlier L019 actual wings, even/odd attachment and trivial-factor proofs; exact pure-leaf theorem retained.','new_work':'Endpoint-anchor exclusion from the full ladder actions, actual one-point transport and parity reduction to even attaching degrees6,8,10.','root_contribution':'Root authored the earlier acquired global middle-colour exchange, with its existing distinct review. No new proof suggestion for this component.','distinct_review':'pending','scope':'No complete critical case or source principal result claimed.'},indent=2)+'\n')
(W/'visual_review.json').write_text(json.dumps({'pages':3,'all_pages_directly_viewed':True,'warnings':False,'images':[pin(W/f'native-{i:02d}.png')for i in range(1,4)]},indent=2)+'\n')
(W/'README.rst').write_text('Even anchored factors\n=====================\n\nRead anchored_even.pdf and scope.json. This is a conditional reduction,\nnot a completed extension or counting theorem. Complete acquired proofs\nand reviews are pinned in dependencies.json. No new finite search is used.\nbuild.py rebuilds and renders the manuscript in a writable copy. freeze.py\nis a historical author-work helper using the original study ancestry.\n')
D=S/'topic_B_L019_anchored_even_v1';need(not D.exists(),'immutable destination exists');D.mkdir()
for p in sorted(W.iterdir()):
    if p.is_file() and p.suffix not in ['.aux','.out','.log'] and not p.name.startswith('native-'):shutil.copy2(p,D/p.name)
exports=[]
for p in sorted(D.rglob('*')):
    if p.is_file():q=pin(p);q['path']=str(p.relative_to(D));exports.append(q)
(D/'manifest.json').write_text(json.dumps({'status':'AUTHOR_FROZEN_BOUNDED_CONDITIONAL_L019_ANCHORED_EVEN','exports':exports,'whole_original_credit':0},indent=2)+'\n')
print(json.dumps({'manifest':pin(D/'manifest.json'),'exports':len(exports),'bindings':len(deps)}))
