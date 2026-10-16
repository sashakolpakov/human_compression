"""Create the private shared source assembly from exact accepted proofs."""
from pathlib import Path
import importlib.util,json,shutil,subprocess

W=Path(__file__).resolve().parent
P=W.parent
S=P.parents[1]
C=P/'source_synthesis'
spec=importlib.util.spec_from_file_location('exact_closure',P/'application_freeze_work/prepare.py')
helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)

def write(name,data): (C/name).write_text(json.dumps(data,indent=2)+'\n')
def binding(p,base=None):return {'path':str(p.relative_to(base) if base else p),**helper.pin(p)}

if C.exists():raise ValueError('fresh synthesis required')
C.mkdir();(C/'proofs').mkdir();(C/'source').mkdir()
for name in ['completion.tex','make_claims.py','L063_claims.json','L064_claims.json','build.py','check.py']:
    shutil.copyfile(W/name,C/name)
shutil.copyfile(P/'arc_actions/source_rows.json',C/'source_arc_rows.json')

routes={
 'omitted_affine':('The omitted affine configurations',S/'corpus106_PSL2_subfield_planes_v1/subfield_planes.tex',S/'corpus106_PSL2_subfield_planes_v1/subfield_planes.pdf'),
 'overgroups':('Two-transitive coset actions in dimension two',P/'overgroups/overgroups.tex',P/'overgroups/overgroups.pdf'),
 'scalar':('Subfield planes and unordered pairs of parabolics',P/'scalar_orbits/orbits.tex',P/'scalar_orbits/orbits.pdf'),
 'cyclic_three':('Counting configurations above a cyclic subgroup of order three',P/'cyclic_three/pairs.tex',P/'cyclic_three/pairs.pdf'),
 'exceptional':('Exceptional parabolics from their common normalizers',P/'exceptional_pairs/exceptional.tex',P/'exceptional_pairs/exceptional.pdf'),
 'subfields':('Subfield parabolics and affine overgroups',P/'subfield_configurations/subfields.tex',P/'subfield_configurations/subfields.pdf'),
 'arcs':('Local arc transitivity from small stabilizers',P/'arc_actions/arcs.tex',P/'arc_actions/native01/arcs.pdf'),
 'subdivision':('Full automorphisms of the dihedral subdivision family',P/'full_automorphisms/subdivision.tex',P/'full_automorphisms/native01/subdivision.pdf'),
 's4_pairs':('Pairs of symmetric parabolics and their full graph groups',P/'s4_automorphisms/s4_pairs.tex',P/'s4_automorphisms/s4_pairs.pdf'),
 'q9':('The order-nine geometry from pairs and matchings',P/'q9_geometry/doily.tex',P/'q9_geometry/doily.pdf')
}
imports=[];order=[{'path':'completion','title':'Source treatment, corrected formulas and attribution'}]
for key,(title,tex,pdf) in routes.items():
    for src in [tex,pdf]:
        dst=C/'proofs'/(key+src.suffix);shutil.copyfile(src,dst)
        imports.append(dict(source=binding(src),destination=binding(dst,C),mode='EXACT'))
    order.append(dict(path='proofs/'+key,title=title))
write('imports.json',imports);write('order.json',order)
write('proof_routes.json',{key:dict(title=v[0],tex='proofs/'+key+'.tex',pdf='proofs/'+key+'.pdf') for key,v in routes.items()})
gatepaths=[S/'corpus106_L076_projective_line_root_adoption/manifest.json',S/'corpus106_PSL2_subfield_planes_root_adoption/manifest.json']
gatepaths += [P/g/'manifest.json' for g in ['overgroups_root_adoption','scalar_orbits_root_review','cyclic_three_root_adoption','exceptional_pairs_root_adoption','subfield_configurations_root_adoption','arc_actions_root_adoption','subdivision_automorphisms_root_adoption','s4_automorphisms_root_adoption','q9_geometry_root_adoption']]
write('gates.json',[dict(manifest=binding(p),status=json.loads(p.read_text())['status']) for p in gatepaths])
for label in ['L063-05','L063-06','L063-07','L063-08','L063-09','L063-10','L064-14','L064-19','L064-20','L064-21']:
    for ext in ['pdf','png']:shutil.copyfile(P/'source_scope_pages'/(label+'.'+ext),C/'source'/(label+'.'+ext))
(C/'README.rst').write_text('Complete shared proof collection for the two fixed Part II originals\n==================================================================\n\nThe opening completion.pdf gives the classification and all corrections. The two source-specific ledgers preserve different published and appendix wording. complete.pdf includes the full exact accepted proofs once. No public registration is performed by this packet. Run check.py --out FRESH --render to verify all exact inputs, ledgers, proof imports, assembled page streams and glyph programs, and the new native build. General proofs still require distinct mathematical review.\n')
write('edition_deltas.json',dict(accepted_proofs_modified=False,exact_accepted_proofs=10,new_manuscript='completion.tex',old_scope_statements='preserved exactly; opening manuscript supplies final joins',source_ledgers=['L063_claims.json','L064_claims.json'],new_markdown_files=0))
run=subprocess.run(['/Users/sasha/.venvs/global/bin/python',str(C/'build.py')],capture_output=True,timeout=90)
(C/'build.stdout').write_bytes(run.stdout);(C/'build.stderr').write_bytes(run.stderr)
if run.returncode:raise ValueError(run.stderr.decode()+run.stdout.decode())
roots=gatepaths+[Path(__file__),W/'completion.tex',W/'make_claims.py',W/'check.py',W/'build.py',P/'application_freeze_work/prepare.py']
roots += [src for title,tex,pdf in routes.values() for src in [tex,pdf]]
roots += [S/'sources'/('catalogue_'+sid+'.'+ext) for sid in ['L063','L064'] for ext in ['pdf','txt']]
for fls in C.glob('*.fls'):
    for line in fls.read_text().splitlines():
        if line.startswith('INPUT '):
            p=Path(line[6:])
            if p.is_absolute() and p.is_file() and not p.is_relative_to(C):roots.append(p)
write('dependencies.json',helper.closure(roots))
print(run.stdout.decode().strip())
print('Prepared private assembly; native author view and manifest sealing remain.')
