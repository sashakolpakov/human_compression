"""Inventory only the actual reads of the accepted occurrence-join functions."""
from pathlib import Path
import hashlib,json,re
P=Path(__file__).resolve().parent;H=P.parent;A=H/'principal_synthesis_v1'
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def main():
 names=['principal_synthesis_v1/'+n for n in ['verify.py','source_catalogue.json','corrections.json','claims.json','gates.json','proof_registry.json']]
 names += ['supplement_source_audit_v1/full_diagram_transcription.json','source_coordinates_v1/joins.json',
 'local_structure_atoms_v1/source_joins.json','local_structure_compound_v1/source_joins.json',
 'parabolic_structure_frozen01/source_join/source_joins.json','local_structure_atoms_v1/corrections.json',
 'local_structure_compound_v1/corrections.json','parabolic_structure_frozen01/source_join/corrections.json',
 'source_flags_component_v1/claims.json','table_one_join_component_v1/result01.json','j3_table_join_v1/source_join.json']
 for r in json.loads((A/'source_catalogue.json').read_text())['full_group_batches']:
  names.append(r['proof']+'/manifest.json')
  if (H/r['proof']/'expected_groups.json').exists():names.append(r['proof']+'/expected_groups.json')
 assert len(names)==len(set(names))
 selected=[dict(pin(H/n),relative_to_H=n) for n in names]
 command=re.compile(r'\\(input|include|includegraphics|bibliography|addbibresource|includepdf)(?:\[[^\]]*\])?\s*\{([^}]+)\}')
 native=[]
 registry=json.loads((A/'proof_registry.json').read_text())
 original_parents={str(A/r['copied_tex']):Path(r['source_tex']['path']).parent for r in registry}
 mains=[A/'synthesis.tex',A/'complete.tex']+[A/r['copied_tex'] for r in registry]
 for tex in mains:
  base=tex.parent;pending=[tex];seen={};edges=[]
  while pending:
   q=pending.pop();content=re.sub(r'(?<!\\)%[^\n]*','',q.read_text())
   for kind,values in command.findall(content):
    for name in values.split(',') if kind=='bibliography' else [values]:
     if '\\' in name:raise ValueError('dynamic native input '+name)
     target=base/name
     choices=[target] if target.suffix else [target.with_suffix(e) for e in (['.tex'] if kind in ['input','include'] else ['.bib'] if kind in ['bibliography','addbibresource'] else ['.pdf','.png','.jpg','.eps'])]
     found=[t.resolve() for t in choices if t.is_file()]
     destination=target
     if not found and str(tex) in original_parents:
      original_target=original_parents[str(tex)]/name
      original_choices=[original_target] if original_target.suffix else [original_target.with_suffix(t.suffix) for t in choices]
      found=[t.resolve() for t in original_choices if t.is_file()]
     if len(found)!=1:raise ValueError('missing/ambiguous native input '+name)
     target=found[0]
     if destination.suffix=='':destination=destination.with_suffix(target.suffix)
     destination.relative_to(A)
     edges.append(dict(from_file=str(q),command=kind,literal=name,resolved=str(target)))
     if str(target) not in seen:
      seen[str(target)]=dict(pin(target),relative_to_author=str(destination.relative_to(A)))
      if target.suffix=='.tex':pending.append(target)
  native.append(dict(main=pin(tex),relative_to_author=str(tex.relative_to(A)),adjacent_inputs=list(seen.values()),commands=edges))
 result=dict(status='EXACT_L091_SELECTED_JOIN_AND_NATIVE_INPUTS',selected=selected,native=native,
              scope='The unchanged ledger_check and controls functions only; no call to the old verifier main, no scientific search, no absent optional expected-groups file may be silently skipped.')
 (P/'selected_inputs.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(selected=len(selected),selected_bytes=sum(r['bytes'] for r in selected),native_mains=len(native),adjacent_occurrences=sum(len(r['adjacent_inputs']) for r in native))))
if __name__=='__main__':main()
