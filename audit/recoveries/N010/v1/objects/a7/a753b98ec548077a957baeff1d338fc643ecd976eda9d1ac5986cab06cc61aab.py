from pathlib import Path
import json,hashlib,shutil,datetime
S=Path('/Users/sasha/medusa/research/leemans');R=Path('/Users/sasha/medusa/math_compression');W=S/'reboot_20261013/N010_retained_inputs';D=W/'register01'
if D.exists():raise ValueError('immutable register exists')
D.mkdir();d=json.loads((W/'retained_register01.json').read_text());src=S/'reboot_20261013/N010_work/SchulteWeiss.tex';text=src.read_text();deps={}
def pin(p):
 b=p.read_bytes();base=R if p.is_relative_to(R)else S
 return {'namespace':'public'if base==R else'study','path':str(p.relative_to(base)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def add(p):deps[str(p)]=pin(p)
def put(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
for p in [src,S/'sources/phase18_schulte_weiss_2006.pdf',S/'reboot_20261013/N010_work/source_contract02.json']:add(p)
for row in d['rows']:
 if text[:text.index(row['source_anchor'])].count('\n')+1!=row['tex_line']:raise ValueError('source location')
 for key in row['source_citation_keys']:
  if key not in d['source_bibliography']:raise ValueError('citation')
 for name in row['exact_acquired_join']:
  p=R/name[7:]if name.startswith('PUBLIC:')else S/name
  if p.is_file():add(p)
  elif p.is_dir():
   add(p/'manifest.json')
   for q in p.glob('*.tex'):add(q)
  else:raise ValueError('unresolved join '+name)
for name in ['source_contract','realization_cone','chamber_words','universal_amalgamation']:
 p=S/('corpus106_N010_'+name+'_root_adoption')
 for q in p.rglob('*'):
  if q.is_file():add(q)
d['inspection_policy']['primary_metadata_only'][0]['finding']='2008 published metadata and abstract inspected; full PDF unavailable. No equality of the 2006 and 2008 aggregates is inferred.'
d['inspection_policy']['primary_metadata_only'][1]['finding']='The author publication page confirms the bibliography; the full primary text was not acquired.'
d['global_aggregate_boundary']['acquired_one_family']['reason']='No complete historical aggregate partition or cross-family overlap ledger was acquired.'
d['question_policy']='34 numbered and 14 embedded historical records, not necessarily 48 independent conjectures. No present-day open status is inferred. Existing historical answers retain their original authorship.'
d['remaining_joins']=['Distinct review of the two small oriented presentation examples.','The principal manuscript must identify 17 and 441 as source-attributed assertions, not reproduced global censuses.','Acquire the exact new chamber, cone and conditional universal-amalgamation proofs and their reviews.','Insert the short neighborliness argument in the root synthesis.','Separate the finite cone theorem from retained infinite geometric classification inputs.','Complete the distinct whole-source principal review before original credit.']
put(D/'retained_register.json',d);put(D/'dependencies.json',list(deps.values()))
shutil.copy2(W/'build_register.py',D/'build_register.py');shutil.copy2(W/'freeze_register.py',D/'freeze_register.py')
lines=['N010 retained inputs and acquired proofs','=======================================','','This register is a source audit for the principal manuscript. It grants no','whole-original or newly solved-question credit. All 51 rows are tied to exact','locations in the fixed survey and its 66-item bibliography. A reference in the','survey does not mean that the cited primary text was independently inspected.','','The global locally projective totals are particularly limited: seventeen','universals and 441 quotients are recorded as source-attributed assertions. The','accepted correction to 137 quotients in one family supplies no justified new','global total. No subtraction or edition identity is inferred.','','The two square-torus example orders are separately proved and computationally','checked in corpus106_N010_oriented_examples_v1; that author packet still awaits','distinct mathematical acceptance. The other acquired proof joins are explicit.','','The metadata-only historical searches sought the precise cited editions. They','were not a current-literature conjecture search, and their publisher abstracts','are not classification proof premises.','']
for row in d['rows']:
 lines += [row['id']+' — '+row['context'], '-'*(len(row['id'])+len(row['context'])+3),'',row['claim'],'',row['qualification'],'','Disposition: '+row['disposition']+'.','Source physical pages: '+', '.join(map(str,row['physical_pages']))+'; TeX line '+str(row['tex_line'])+'.','Cited keys: '+', '.join(row['source_citation_keys'])+'.','']
(D/'register.rst').write_text('\n'.join(lines))
put(D/'audit.json',{'status':'PRECISE_SOURCE_INPUT_REGISTER_NOT_PRINCIPAL_ACCEPTANCE','author':'/root/l044_resume','rows':len(d['rows']),'contexts':len({r['context']for r in d['rows']}),'bibliography_entries':len(d['source_bibliography']),'source_anchors_and_lines_checked':True,'acquired_join_locators_checked':True,'dependencies':len(deps),'global_17_441_independently_proved':False,'two_small_examples_distinct_review_pending':True,'whole_original_credit':0,'new_question_credit':0,'new_measurements':0,'new_Lean_credit':0,'owned_live_handles':[],'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
put(D/'manifest.json',{'status':'FROZEN_N010_RETAINED_INPUT_REGISTER','exports':[dict(path=str(p.relative_to(D)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())for p in sorted(D.rglob('*'))if p.is_file()]})
print(pin(D/'manifest.json'))
