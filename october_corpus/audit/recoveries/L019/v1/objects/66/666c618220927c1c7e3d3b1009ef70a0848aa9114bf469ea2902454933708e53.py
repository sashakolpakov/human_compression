from pathlib import Path
import json,hashlib,datetime
from pypdf import PdfReader
S=Path('/Users/sasha/medusa/research/leemans');W=Path(__file__).resolve().parent;A=S/'topic_B_L019_paired_middle_v1';P=S/'topic_B_L019_paired_middle_independent_review'
def need(v,m):
 if not v:raise RuntimeError(m)
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(S)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def perm(*cycles):
 p=list(range(13))
 for c in cycles:
  for i,x in enumerate(c):p[x]=c[(i+1)%len(c)]
 return tuple(p)
def mul(a,b):return tuple(b[a[i]]for i in range(13))
I=perm();h0=perm((0,1),(2,3));h1=perm((1,2),(3,4),(5,6));h2=perm((4,5),(6,7));x=I
for _ in range(5):x=mul(x,mul(h0,h1))
need(x==perm((5,6)),'fifth power');conj=mul(mul(h2,x),h2);need(conj==perm((4,7)),'conjugate');delta=mul(x,conj);need(delta==perm((4,7),(5,6))and delta not in [I,h2],'intersection contradiction')
(W/'literal_control.json').write_text(json.dumps({'status':'PASS','degree':13,'beta':list(x),'conjugate':list(conj),'delta':list(delta),'purpose':'Independent literal check of new rank-six word; acquired Alt9 and IP are mathematical premises.'},indent=2)+'\n')
for f in ['paired_middle.pdf']:
 old=PdfReader(A/f);new=PdfReader(W/'replay01'/f);need(len(new.pages)==2,'pages');need([p.extract_text()for p in old.pages]==[p.extract_text()for p in new.pages],'native text')
rows={}
def add(p):q=pin(p);rows[q['path']]=q
add(A/'manifest.json')
for e in json.loads((A/'manifest.json').read_text())['exports']:
 p=A/e['path'];q=pin(p);need(q['bytes']==e['bytes']and q['sha256']==e['sha256'],'author');add(p)
for e in json.loads((A/'dependencies.json').read_text()):
 p=S/e['path'];q=pin(p);need(q['bytes']==e['bytes']and q['sha256']==e['sha256'],'dep');add(p)
for p in W.rglob('*'):
 if p.is_file()and '__pycache__'not in p.parts:add(p)
P.mkdir(exist_ok=False)
review={'status':'ACCEPTED_L019_PAIRED_MIDDLE','reviewer':'/root/publication_recovery','author':'/root/l044_resume','independence':'No contribution to this parity induction or rank-six argument. Reviewer previously reviewed, but did not author, the acquired anchor-deletion and critical-route deductions; the earlier generic square discussion is retained under its separate root review. Exact nine-point proof and root distinct review are acquired, not claimed independently reconstructed here.','mathematical_review':['Read both new pages completely; re-read full seven-point orbit proof, nine-point normalization/classification proof and root review, actual critical first-cut and endpoint interfaces.','Ranks one/two use elementary involution support; seven-point rank-three impossibility uses its weaker acquired anchor assumptions; the complete rank-four classification supplies actual A9 and the exact anchored omission centralizer.','For rank six the tail has degree nine/rank four and all paired/IP/anchor hypotheses. beta fixes both tail anchors and centralizes its last three marks, giving exactly identity or (p q). The fifth power and conjugation give the displayed delta. Its membership in actual A9 and the exact original label-set intersection force delta into <h2>, a contradiction.','At rank five the acquired tail would be the impossible rank-three boundary. At rank at least seven the independently accepted anchor-deletion result gives beta=1; the actual supported tail decreases rank by two and retains every hypothesis.','The corollary acquires the complete conditional first-cut and endpoint alternatives and excludes precisely their actual symmetric paired residual; it does not silently discharge the strict smaller-degree sufficient-split induction.'],'checks':{'fresh_replay':'reboot_20261013/L019_paired_middle_distinct/replay01/report.json','exports':16,'direct_bindings':159,'optimization_guards':2,'native_pages':2,'all_native_pages_viewed':True,'native_text_identical':True,'literal_rank_six_word':'reboot_20261013/L019_paired_middle_distinct/literal_control.json'},'scope':'Uniform parity theorem plus the explicitly conditional critical-route conclusion. Complete forward induction, actual contraction IP, least/canonical split choice, reversal compatibility and stable constants remain separate.','whole_original_credit':0,'new_question_credit':0,'new_Lean':0,'measurement':None,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(P/'review.json').write_text(json.dumps(review,indent=2)+'\n');(P/'bindings.json').write_text(json.dumps(sorted(rows.values(),key=lambda x:x['path']),indent=2)+'\n')
exports=[]
for p in sorted(P.iterdir()):
 q=pin(p);q['path']=p.name;exports.append(q)
(P/'manifest.json').write_text(json.dumps({'status':'ACCEPTED_L019_PAIRED_MIDDLE','exports':exports,'whole_original_credit':0},indent=2)+'\n');print(json.dumps({'manifest':pin(P/'manifest.json'),'bindings':len(rows)}))
