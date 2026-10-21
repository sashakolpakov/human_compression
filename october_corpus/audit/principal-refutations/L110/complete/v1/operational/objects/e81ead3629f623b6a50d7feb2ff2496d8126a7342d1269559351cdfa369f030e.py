from pathlib import Path
import copy,json,hashlib
W=Path(__file__).resolve().parent;P=W.parent
old=P/'higher_source_synthesis/claims.json'
d=json.loads(old.read_text());by={r['label']:r for r in d['claims']}
by['Definitions: left cosets, algebraic residues, RWPRI and local2T']['qualification'] += ' Source p5 defines Suzuki type as simple and expressly excludes Sz(2); residue Suzuki labels use that convention, so their simple bottom has parameter at least8.'
for i in [4,5,6,8]:
 r=by[f'Section3.3 extension branch R{i}'];r['qualification']='The full prescribed input residue is impossible; this is separate from the false global exhaustion and from existence of other bare parabolic types.'
by['Section3.3 extension branch R12']['qualification']='Every embedding with the prescribed mixed parabolic and pair intersections has a proper scalar intermediate overgroup, so RWPRI fails.'
for i in [7,9,10,11,13]:
 r=by[f'Section3.3 extension branch R{i}'];r['status']='CONDITIONAL_EXTENSION_NECESSITY_PROVED_WITH_SOURCE_CORRECTIONS';r['proof']='proofs/split_necessity.tex' if i in [7,9] else 'proofs/torus_necessity.tex'
 r['qualification']='Every rank4 RWPRI extension of this exact prescribed residue with its simple parabolic maximal has the stated corrected full lattice. This does not prove the false global branch-list exhaustion. Source p5 simple-Suzuki convention retained.'
 if i==7:r['qualification']+=' Correct p13 G4 to G3 and new-prime divisor to (sprime-1)/(t-1).'
 if i==10:r['qualification']+=' Correct p14 later interchange of G2/G3 to match the opening lattice.'
 if i==11:r['qualification']+=' Distinct input primes and their field-degree identities are derived; the full torus complement is essential.'
r=by['Section3.3.2 same R7/R8 branches'];r.update(status='CONDITIONAL_BRANCHES_DISPOSED_GLOBAL_EXHAUSTION_REFUTED',proof='proofs/split_necessity.tex; proofs/higher_obstructions.tex; proofs/principal.tex',qualification='Every extension of the exact R7 residue has the proved corrected lattice; R8 has no realization. Neither local result restores the exhaustive two-branch assertion.')
d['new_assembly_mathematics'] += ['Necessity for every extension of the exact R7/R9 residues using field-generating complements','Necessity for the exact R10/R11/R13 residues using full torus complements, input-degree derivation and divisor valuations']
d['source_scope_conventions']={'printed_page':5,'Suzuki_type':'The source defines Suzuki type as simple and explicitly excludes Sz(2); this convention governs Suzuki groups in the prescribed residues.'}
d['prior_review_hold']={'path':str(P/'higher_source_review01/manifest.json'),'sha256':hashlib.sha256((P/'higher_source_review01/manifest.json').read_bytes()).hexdigest(),'reason':'Canonical existence and a false global classification did not dispose of local conditional extension necessity. This edition imports the two subsequently accepted necessity proofs.'}
(W/'claims.json').write_text(json.dumps(d,indent=2)+'\n')
print(len(d['claims']))
