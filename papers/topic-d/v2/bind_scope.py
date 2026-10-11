#!/usr/bin/env python3
"""Build the local Topic D clause map from the fixed accepted 37-row boundary.
Run before freeze only. This binds proofs; it does not prove their conclusions.
"""
import json,re,hashlib,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent
STUDY=ROOT.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def bind(path,base=ROOT):
 p=base/path
 return dict(path=str(path),bytes=p.stat().st_size,sha256=sha(p))
def sections(path):
 p=ROOT/path;s=p.read_text();matches=list(re.finditer(r'\\(?:sub)?section\*?\{',s));ans=[]
 for i,m in enumerate(matches):
  a=m.start();b=matches[i+1].start() if i+1<len(matches) else len(s)
  fragment=s[a:b];heading=fragment.split('\\label',1)[0].split('\n\n',1)[0]
  ans.append(dict(path=path,start_codepoint=a,end_codepoint_exclusive=b,sha256_utf8=hashlib.sha256(fragment.encode()).hexdigest(),heading=' '.join(heading.split())))
 return ans
spans={}
for key,path in [('A1','sections/commuting-body.tex'),('A2','sections/suzuki-body.tex'),('A3','hall-janko-geometries.tex'),('Census','sections/janko-body.tex'),('Support','sections/02-support.tex'),('Actions','sections/01-actions.tex'),('Panels','sections/03-panels.tex')]:
 for i,span in enumerate(sections(path),1):spans[f'{key}.{i}']=span
# Source positions are physical pages of the three pinned primary PDFs.
pages74=[[2,6,8],[2,9,10,11],[5],[7,11],[3],[4],[4],[4],[5],[6],[7,8],[8],[9],[11],[8,10],[4],[3,10]]
pages104=[[3,4],[3],[3,4],[3,4,5]]
old=json.loads((STUDY/'phase164_enumeration_ledger.json').read_text())
rows=[]
for row in old['contracts']:
 sid=row['source_id']
 if sid not in ['L066','L074','L104']:continue
 r={k:v for k,v in row.items() if k not in ['proof_spans','proof','source_pages']}
 idx=int(row['id'].split('.')[1]);keys=[]
 for sp in row['proof_spans']:
  h=sp['heading']
  if h.startswith('### 3.'):keys.append('A1.'+h.split('.')[1])
  elif h.startswith('### 4.'):keys.append('A2.'+h.split('.')[1])
  elif h.startswith('## 2.'):keys.append('Support.1')
  elif h.startswith('## 5.'):keys+=['Panels.1']
  elif h.startswith('### 5.1.'):keys+=['Panels.2']
  elif h.startswith('### 5.2.'):keys+=['Census.1']
  elif h.startswith('## 7.'):keys+=['A3.2']
  else:raise RuntimeError('Unmapped previous span '+h)
 # Include actual use of the common proofs, retaining the application-specific obligations.
 if sid=='L066':
  if idx in [1,2,3,4,5,6,10,11,14,16]:keys+=['Actions.1']
  if idx in [1,2,5,6,11,14]:keys+=['Support.1']
  if idx in [1,2,8,12,13,15]:keys+=['Actions.1']
  if idx==7:keys+=['U.Conventions']
 elif sid=='L074':
  if idx in [1,2,4,11,12,13,14,15]:keys+=['Support.1']
  if idx in [1,2,13,14,15]:keys+=['Actions.1']
 else:
  if idx<=3:keys+=['Panels.Helly','Panels.1','Panels.2','Census.1','A3.1','U.Conventions']
 r['source_pages']=row.get('source_pages') or (pages74[idx-1] if sid=='L074' else pages104[idx-1])
 r['current_proof_spans']=list(dict.fromkeys(keys))
 r['predecessor_proof_spans']=row['proof_spans']
 if sid=='L104' and idx==4:r['current_status']='excluded_secondary_assertions_in_printed_main_article_and_supplement'
 else:r['current_status']=row['status']
 rows.append(r)
# The conventions are part of the whole common paper rather than an extra theorem.
u=(ROOT/'umbrella.tex').read_text();a=u.index('All groups in the counting statements');b=u.index('\\input{sections/01-actions.tex}')
ps=(ROOT/'sections/03-panels.tex').read_text();pe=ps.index('\\section{Panel')
spans['Panels.Helly']=dict(path='sections/03-panels.tex',start_codepoint=0,end_codepoint_exclusive=pe,sha256_utf8=hashlib.sha256(ps[:pe].encode()).hexdigest(),heading='Typed coset Helly and its complete anchored criterion')
spans['U.Conventions']=dict(path='umbrella.tex',start_codepoint=a,end_codepoint_exclusive=b,sha256_utf8=hashlib.sha256(u[a:b].encode()).hexdigest(),heading='Finite types, geometries and the retained string C-group correspondence')
for r in rows:
 for key in r['current_proof_spans']:
  if key not in spans:raise RuntimeError('Missing span '+key)
source_inputs={s:old['source_editions'][s] for s in ['L066','L074','L104']}
for s,r in source_inputs.items():
 p=STUDY/r['primary']['path']
 if sha(p)!=r['primary']['sha256']:raise RuntimeError('Changed primary '+s)
inv=json.loads((ROOT/'outline_and_inventory.json').read_text())
programs=inv['program_inventory']
for p in programs:
 if sha(ROOT/p['copy'])!=p['sha256']:raise RuntimeError('Changed program '+p['path'])
# The new common theorem replaces two independently repeated odd-order arguments.
changes=[
 {'component':'UD.AdmissibleExtensions','change':'Combines actual stabilizer fibers, invariant admissibility and exact support in one proved formula. Burnside, Mobius inversion and orbit-stabilizer remain classical, not historical novelty.'},
 {'component':'UD.OddOrbits','change':'One arbitrary odd-order action lemma replaces separate inversion and duality orbit-freeness arguments after their explicit local hypotheses.'},
 {'component':'D1','change':'Reversal count is a direct common fixed-point-count consequence; all multiplicity coordinates, parity, formulas and exceptional census preserved.'},
 {'component':'D2','change':'Full normalization, subfield-position, generation, IP, rank and nested-formula equivalence preserved. Suzuki/Luneburg/Fermat/Mobius/Leemans2006 origins made explicit; retained maximal subgroup table written out.'},
 {'component':'D3','change':'Application calls the complete arbitrary-Borel recognition/augmentation proof in U. All 30 representatives and the all-ranks census are certified by the unchanged required programs. Printed diagram/Aut/Cor/doubling omissions remain visible.'},
 {'component':'Lean','change':'Eight actual generic fiber-orbit and odd-period declarations added; two abstract centralizer rank declarations reused. Scope does not include source-specific group structure, Mobius formula, geometric recognition or finite programs.'}]
files=[bind(str(p.relative_to(ROOT))) for p in sorted(ROOT.glob('*.tex'))]+[bind(str(p.relative_to(ROOT))) for p in sorted((ROOT/'sections').glob('*.tex'))]+[bind(str(p.relative_to(ROOT))) for p in sorted(ROOT.glob('*.pdf'))]
result=dict(schema=1,status='AUTHOR_COMPLETE_PENDING_INDEPENDENT_REVIEW',intake_closed=True,source_ids=['L066','L074','L104'],predecessor=dict(ledger=bind('phase164_enumeration_ledger.json',STUDY),manuscript=bind('phase164_enumeration_manuscript.md',STUDY),umbrella=bind('phase138_umbrella_v3.md',STUDY),independent_review=bind('phase173_D_review_export.json',STUDY)),sources=source_inputs,documents=files,proof_spans=spans,contracts=rows,contract_count=len(rows),current_changes=changes,program_inventory=programs,formal_scope=bind('formal/scope.json'),cost_scope=dict(full_common_paper_charged_once_in_this_topic=True,cross_topic_discount=False,complete_applications=['commuting-involutions','suzuki-polyhedra','hall-janko-geometries'],full_mathematical_programs=8,required_programs=5,additional_diagnostic_programs=3,complete_drivers=2,ratio=None,historical_program_cost=None,image_cost=None),not_claimed=['New historical priority for the source classifications','Any M22 result','Recovery of the excluded L104 diagrams, Aut/Cor groups or doubling relation','Complete end-to-end Lean formalization','A new source/question credit or a numerical compression ratio'])
(ROOT/'scope.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'contracts':len(rows),'spans':len(spans),'documents':len(files),'mathematical_programs':8,'drivers':2}))
