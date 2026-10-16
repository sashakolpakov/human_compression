"""Import exact accepted proof texts; no scientific acquisition."""
from pathlib import Path
import json,hashlib,shutil
C=Path(__file__).resolve().parent; P=C.parent; S=P.parents[1]
R=Path('/Users/sasha/medusa/math_compression'); U=S/'geometry/suzuki_subgroups'
def pin(p,base=None):
 b=p.read_bytes();return dict(path=str(p.relative_to(base) if base else p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def dump(n,d):(C/n).write_text(json.dumps(d,indent=2)+'\n')
(C/'proofs').mkdir(exist_ok=True)
entries=[('principal',S/'corpus106_L114_compatible_tori_v1/compatible_tori',None),('preliminary',P/'preliminary_scope/preliminaries',None),('prime_degree',P/'prime_degree/prime_degree',None),('restrictions',P/'normalizer_restrictions/restrictions',None),('patterns',P/'prime_patterns/patterns',None),('markings',P/'remaining_markings_application/panels',None),('nonthin8',P/'nonthin_application02/nonthin',None),('nonthin32',P/'nonthin32_application/nonthin32',None),('local_rank',P/'local_rank_v1/local_rank',None),('standard_subfields',S/'corpus106_L110_subfield_boundary_v1/subfield_boundary',None),('scalar_subspaces',S/'corpus106_L115_scalar_subspaces_v1/central_covers',None),('common_preliminaries',U/'preliminaries/preliminaries',U/'preliminaries/native03/preliminaries.pdf'),('normalizer_families',U/'rank_two_families/families',U/'rank_two_families/native02/families.pdf'),('subfield_families',U/'subfield_families_corrected/subfields',U/'subfield_families_corrected/native01/subfields.pdf')]
imports=[]
for name,stem,pdf in entries:
 for ext in ['.tex','.pdf']:
  source=pdf if ext=='.pdf' and pdf else stem.with_suffix(ext)
  dest=C/'proofs'/(name+ext);shutil.copyfile(source,dest)
  imports.append(dict(source=pin(source),destination=pin(dest,C),mode='EXACT'))
for name in ['completion','realizations']:shutil.copyfile(P/'source_synthesis_work'/(name+'.tex'),C/(name+'.tex'))
dump('imports.json',imports)
roots=[S/'corpus106_L114_compatible_tori_v1',S/'corpus106_L114_compatible_tori_root_adoption']
for name in ['preliminary_scope','preliminary_scope_root_review','prime_degree','prime_degree_root_review','normalizer_restrictions','normalizer_restrictions_root_review','prime_patterns','prime_patterns_root_review','remaining_markings_application','remaining_markings_root_review','nonthin_application02','nonthin_root_review','nonthin32_application','nonthin32_root_review','local_rank_v1','local_rank_root_review','higher_split_family','higher_split_family_independent_review']:roots.append(P/name)
for name in ['preliminaries','preliminaries_review_adoption','rank_two_families','rank_two_families_root_review','subfield_families_corrected','subfield_families_root_adoption']:roots.append(U/name)
deps={};gates=[]
def add(row):
 if pin(Path(row['path']))!=row:raise ValueError('changed input '+row['path'])
 deps[row['path']]=row
for root in roots:
 mf=root/'manifest.json';obj=json.loads(mf.read_text());add(pin(mf))
 if 'review' in root.name or 'adoption' in root.name:gates.append(dict(manifest=pin(mf),status=obj['status']))
 for row in obj['exports']:add(dict(row,path=str(root/row['path'])))
 df=root/'dependencies.json'
 if df.exists():
  add(pin(df));rows=json.loads(df.read_text())
  if not isinstance(rows,list):raise ValueError('dependencies format '+str(df))
  for row in rows:add(row)
for row in imports:add(row['source'])
paths=[S/'sources/older_L114.pdf',S/'sources/older_L114.txt',R/'audit/corpus/accessible106/archived_unavailable.json',P/'source_disposition_work/table_join.rst',P/'source_synthesis_work/realizations.tex',P/'source_synthesis_work/completion.tex']
for name in ['phase5_suzuki_realization.md','phase5_suzuki_higher.md','phase5_suzuki_independent_audit.md','phase5_suzuki_audit.json','phase5_suzuki_check.py','phase5_suzuki_check.json','phase5_suzuki_intake.json','phase5_suzuki_higher_audit.json','phase5_suzuki_higher_check.py','phase5_suzuki_higher_check.json','phase5_suzuki_higher_intake.json']:paths.append(S/name)
for f in paths+list((S/'sources/older_L114_ocr').glob('page-*.png')):add(pin(f))
dump('dependencies.json',[deps[k] for k in sorted(deps)]);dump('gates.json',gates)
dump('edition_deltas.json',dict(accepted_proofs_modified=False,working_notes_reassembled=['realizations.tex','completion.tex'],realizations_old_inputs=[pin(S/'phase5_suzuki_realization.md'),pin(S/'phase5_suzuki_higher.md'),pin(S/'phase5_suzuki_independent_audit.md')],realizations_new_interfaces=['Accepted embedded-subfield uniqueness','Accepted scalar-field valuation argument','Explicit nonzero trace implies odd order','All permitted half-order parameters stated'],historical_open_component_sentences='Retained verbatim in exact imports; completion.tex and claims.json give current disposition.'))
print(json.dumps(dict(dependencies=len(deps),accepted_gates=len(gates))))
