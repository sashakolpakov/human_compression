from pathlib import Path
import json,hashlib,shutil
W=Path(__file__).resolve().parent;P=W.parent;S=P.parents[1];C=P/'higher_source_synthesis02'
if C.exists():raise SystemExit('fresh destination required')
C.mkdir();(C/'proofs').mkdir()
def pin(p,base=None):
 b=p.read_bytes();return dict(path=str(p.relative_to(base) if base else p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def dump(n,d):(C/n).write_text(json.dumps(d,indent=2)+'\n')
entries=[('principal_boundary',S/'corpus106_L110_subfield_boundary_v1/subfield_boundary'),('prime_extensions',P/'prime_residue_extensions/extensions'),('higher_obstructions',P/'higher_obstructions/obstructions'),('split_families',P/'higher_split_family/split_families')]
for stem in ['descent','torus_families','pure_mixed','diagrams']:entries.append((stem,P/'higher_families'/stem))
entries.append(('local_geometry',P/'local_geometry_v1/local_geometry'))
entries += [('split_necessity',P/'split_extension_necessity/necessity'),('torus_necessity',P/'torus_extension_necessity_v2/necessity')]
for stem in ['preliminary','prime_degree','restrictions','patterns','principal','nonthin8','nonthin32','local_rank','scalar_subspaces','common_preliminaries','normalizer_families','subfield_families']:entries.append((stem,P/'source_synthesis/proofs'/stem))
entries.append(('realizations',P/'source_synthesis/realizations'))
imports=[]
for name,stem in entries:
 for ext in ['.tex','.pdf']:
  src=stem.with_suffix(ext);dest=C/'proofs'/(name+ext);shutil.copyfile(src,dest);imports.append(dict(source=pin(src),destination=pin(dest,C),mode='EXACT'))
for f in ['completion.tex','claims.json','make_claims.py']:shutil.copyfile(W/f,C/f)
roots=[S/'corpus106_L110_subfield_boundary_v1',S/'corpus106_L110_subfield_boundary_root_adoption']
for name in ['prime_residue_extensions','prime_residue_extensions_root_review','higher_obstructions','higher_obstructions_independent_review','higher_split_family','higher_split_family_independent_review','higher_families','higher_families_root_review','local_geometry_v1','local_geometry_root_review','source_synthesis','source_synthesis_root_review']:roots.append(P/name)
roots += [P/x for x in ['split_extension_necessity','split_extension_necessity_root_review','torus_extension_necessity_v2','torus_extension_necessity_independent_review','torus_extension_necessity_root_adoption']]
deps={};gates=[]
def add(r):
 r={k:r[k] for k in ['path','bytes','sha256']}
 if pin(Path(r['path']))!=r:raise ValueError('changed dependency '+r['path'])
 deps[r['path']]=r
for root in roots:
 mf=root/'manifest.json';obj=json.loads(mf.read_text());add(pin(mf))
 if 'review' in root.name or 'adoption' in root.name:gates.append(dict(manifest=pin(mf),status=obj['status']))
 for row in obj['exports']:add(dict(row,path=str(root/row['path'])))
 df=root/'dependencies.json'
 if df.exists():
  add(pin(df))
  for row in json.loads(df.read_text()):add(row)
for r in imports:add(r['source'])
for p in [W/'completion.tex',W/'claims.json',W/'make_claims.py',W/'prepare_synthesis.py']:add(pin(p))
for f in ['manifest.json','review.json','dependencies.json']:
 p=P/'higher_source_review01'/f
 if p.is_file():add(pin(p))
add(pin(P/'higher_source_synthesis/manifest.json'))
dump('imports.json',imports);dump('dependencies.json',[deps[k] for k in sorted(deps)]);dump('gates.json',gates)
dump('edition_deltas.json',dict(accepted_proofs_modified=False,new_source_overview='completion.tex',exact_accepted_proofs=len(entries),stronger_geometry_proof='proofs/local_geometry.tex separately accepted; old conservative local_rank.tex unchanged',prior_held_assembly=pin(P/'higher_source_synthesis/manifest.json'),prior_hold=pin(P/'higher_source_review01/manifest.json'),conditional_necessity_repaired=['R7','R9','R10','R11','R13'],source_scope='Source p5 expressly excludes Sz2 from Suzuki type',historical_progress_sentences='The opening overview and current claim ledger supersede prior unfinished-scope sentences in exact imported proofs.'))
order=['completion','proofs/principal_boundary','proofs/prime_extensions','proofs/higher_obstructions','proofs/split_families','proofs/split_necessity','proofs/torus_necessity','proofs/descent','proofs/torus_families','proofs/pure_mixed','proofs/diagrams','proofs/local_geometry','proofs/preliminary','proofs/prime_degree','proofs/restrictions','proofs/patterns','proofs/realizations','proofs/principal','proofs/nonthin8','proofs/nonthin32','proofs/local_rank','proofs/scalar_subspaces','proofs/common_preliminaries','proofs/normalizer_families','proofs/subfield_families']
dump('order.json',order)
print(json.dumps(dict(dependencies=len(deps),gates=len(gates),imports=len(imports),parts=len(order))))
