from pathlib import Path
import hashlib,json,shutil
S=Path('/Users/sasha/medusa/research/leemans');P=S/'geometry/psl2_rank_two';W=P/'cyclic_three_work';A=P/'cyclic_three'
if A.exists():raise ValueError('fresh packet required')
def pin(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
A.mkdir();shutil.copytree(W/'native01',A/'native');shutil.copytree(W/'source',A/'source');shutil.copyfile(W/'pairs.tex',A/'pairs.tex');shutil.copyfile(W/'native01/pairs.pdf',A/'pairs.pdf')
code=(P/'s4_automorphisms/check.py').read_text().replace('s4_pairs','pairs').replace('PASS_S4_AUTOMORPHISMS_EXACT_NATIVE_REPLAY','PASS_CYCLIC_THREE_EXACT_NATIVE_REPLAY').replace('source_claim_groups=3','source_claim_groups=7');(A/'check.py').write_text(code)
write(A/'scope.json',{'sources':['L063','L064'],'source_claims':[{'source':'L063','claim':'Table2 rows1--5 / Proposition5.6: existence and counts','disposition':'RECOVERED'},{'source':'L063','claim':'Table2 rows6--7 / Proposition5.6: equal-type configurations','disposition':'INNER_COUNTS_CORRECTED_AUT_COUNTS_RECOVERED','printed_inner':'2m-1','corrected_inner':'m+floor(m/2)','aut':'m','m':'(p-epsilon)/6'},{'source':'L064','claim':'Proposition16, physical pages2--4','disposition':'SAME_CONFIGURATIONS_AND_CORRECTION_UNDER_PUBLISHED_UNORDERED_CONVENTION'}],'no_group_search':True,'overgroup_candidate_interface':'proved directly by d-1 dividing3','classical_premises':['A4 maximal precisely under specified prime congruences','one A4 class and one C3 class in those groups','N_PGL(A4)=S4','unique cyclic centralizer torus and dihedral normalizer','Aut PSL2(p)=PGL2(p)'],'new_principal_refutation_credit':0,'whole_original_credit':0,'lean_credit':0,'compression_measurement':None})
write(A/'native_review.json',{'pages':4,'directly_viewed':[1,2,3,4],'dpi':105,'overfull_boxes':False,'source_native_pages_viewed':['L063:2','L063:4','L063:17','L064:2','L064:3','L064:4']})
(A/'development.rst').write_text('One complete four-page proof edition, including references, was built and directly viewed before freezing. The conjugacy correction was derived from the regular normalizer action and inversion, not fitted to finite examples. The small overgroup interface is proved explicitly in the manuscript. This is an author packet awaiting a distinct mathematical/source review.\n')
deps={}
def add(p):
 p=Path(p).resolve();deps[str(p)]={'path':str(p),**pin(p)}
for id in ['L063','L064']:
 for ext in ['pdf','txt']:add(S/f'sources/catalogue_{id}.{ext}')
add(P/'s4_automorphisms/check.py');add(Path('/private/tmp/freeze_cyclic_three_oct16.py'))
for line in (W/'native01/pairs.fls').read_text().splitlines():
 if line.startswith('INPUT '):
  p=Path(line[6:]);p=p if p.is_absolute() else W/'native01'/p
  if p.exists() and not p.is_relative_to(W):add(p)
write(A/'dependencies.json',list(deps.values()));write(A/'manifest.json',{'status':'L063_L064_CYCLIC_THREE_COUNTS_AWAITING_DISTINCT_REVIEW','exports':[{'path':str(p.relative_to(A)),**pin(p)}for p in sorted(A.rglob('*'))if p.is_file()]})
print(pin(A/'manifest.json'));print('dependencies',len(deps))
