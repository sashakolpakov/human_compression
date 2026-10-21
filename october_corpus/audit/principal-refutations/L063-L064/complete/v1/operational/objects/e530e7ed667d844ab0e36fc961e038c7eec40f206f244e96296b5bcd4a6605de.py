"""Freeze two readable proof applications; no group computation or public write."""
from pathlib import Path
import hashlib
import json
import shutil

P = Path(__file__).resolve().parents[1]
S = P.parents[1]


def pin(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def write(p, value):
    p.write_text(json.dumps(value, indent=2) + '\n')


def closure(roots):
    result = {}
    pending = list(roots)
    while pending:
        p = pending.pop().resolve()
        if str(p) in result:
            continue
        result[str(p)] = {'path': str(p), **pin(p)}
        if p.name == 'manifest.json':
            m = json.loads(p.read_text())
            for r in m.get('exports', []):
                q = p.parent / r['path']
                if pin(q) != {k: r[k] for k in ('bytes', 'sha256')}:
                    raise ValueError('changed export ' + str(q))
                pending.append(q)
        elif p.name == 'dependencies.json':
            rows = json.loads(p.read_text())
            if not isinstance(rows, list):
                raise ValueError('unexpected dependencies format ' + str(p))
            for r in rows:
                q = Path(r['path'])
                if not q.is_absolute():
                    candidates = [p.parent / q, S / q]
                    matches = [c for c in candidates if c.is_file() and pin(c) == {k: r[k] for k in ('bytes', 'sha256')}]
                    if not matches:
                        raise ValueError('unresolved exact relative dependency ' + str(p) + ': ' + str(q))
                    q = matches[0]
                if pin(q) != {k: r[k] for k in ('bytes', 'sha256')}:
                    raise ValueError('changed dependency ' + str(q))
                pending.append(q)
    return [result[k] for k in sorted(result)]


def freeze(name, stem, pages, source_pages, gates, scope):
    a = P / name
    if a.exists():
        raise ValueError('fresh application required')
    a.mkdir()
    work = P / (name + '_work')
    native = work / 'native04'
    if (work / (stem + '.tex')).read_bytes() != (native / (stem + '.tex')).read_bytes():
        raise ValueError('current proof differs from native build')
    shutil.copytree(native, a / 'native')
    for ext in ('tex', 'pdf'):
        shutil.copyfile(native / (stem + '.' + ext), a / (stem + '.' + ext))
    (a / 'source').mkdir()
    joins = []
    for label in source_pages:
        for ext in ('pdf', 'png'):
            shutil.copyfile(P / 'source_scope_pages' / (label + '.' + ext), a / 'source' / (label + '.' + ext))
        sid, page = label.split('-')
        joins.append({'source': sid, 'physical_page': int(page), 'extracted_pdf': 'source/' + label + '.pdf', 'native_image': 'source/' + label + '.png', 'original': str(S / 'sources' / ('catalogue_' + sid + '.pdf'))})
    write(a / 'source_joins.json', joins)
    scope['common_interface'] = {'manifest': str(P/'overgroups_root_adoption/manifest.json'), 'sha256': 'e3cd3802509769f5ef8e8a0ce05f3e1b2cdef499107bf97f0d88149685fc3871', 'status': 'ROOT_ADOPTED_L063_L064_COMMON_TWO_TRANSITIVE_OVERGROUPS'}
    scope.update(new_group_searches=0, new_principal_refutation_credit=0, whole_original_credit=0, lean_credit=0, compression_measurement=None)
    write(a/'scope.json', scope)
    write(a/'native_review.json', {'author_directly_viewed_all_pages': True, 'pages': pages, 'resolution_dpi': 105, 'history': 'All native03 pages were directly viewed; changed native04 pages were then directly viewed, with unchanged pages matched byte for byte.', 'overfull_lines': 0})
    (a/'development.rst').write_text('This is an author application awaiting distinct mathematical and source review. The common representation interface has its own accepted distinct review and root adoption. No group census was run. The coordinate and normalizer arguments are written in full; previously accepted scalar, geometry and graph-group proofs remain separately attributed. Earlier draft/native editions remain in the private working directory.\n')
    checker = (P/'cyclic_three/check.py').read_text()
    checker = checker.replace('pairs.tex', stem+'.tex').replace('pairs.pdf', stem+'.pdf')
    checker = checker.replace('!= 4', '!= '+str(pages)).replace('native_pages=4', 'native_pages='+str(pages))
    checker = checker.replace('source_claim_groups=7', 'source_claim_groups='+str(len(scope['source_claims'])))
    checker = checker.replace('PASS_CYCLIC_THREE_EXACT_NATIVE_REPLAY', 'PASS_'+name.upper()+'_EXACT_NATIVE_REPLAY')
    checker = checker.replace('    out.mkdir(parents=True)\n', '''    joins = json.loads((A/'source_joins.json').read_text())
    for row in joins:
        original = PdfReader(row['original']).pages[row['physical_page']-1]
        extracted = PdfReader(A/row['extracted_pdf']).pages[0]
        if original.get_contents().get_data() != extracted.get_contents().get_data():
            raise ValueError('different original page stream')
        if original.extract_text() != extracted.extract_text():
            raise ValueError('different original page text')
    out.mkdir(parents=True)
''')
    (a/'check.py').write_text(checker)
    roots = [P/g/'manifest.json' for g in gates]
    roots += [S/'sources'/('catalogue_'+sid+'.'+ext) for sid in ('L063','L064') for ext in ('pdf','txt')]
    roots += [Path(__file__), Path('/opt/homebrew/bin/pdflatex').resolve(), Path('/opt/homebrew/bin/gs').resolve()]
    for line in (native/(stem+'.fls')).read_text().splitlines():
        if line.startswith('INPUT '):
            q = Path(line[6:])
            if q.is_absolute() and q.is_file() and not q.is_relative_to(native):
                roots.append(q)
    write(a/'dependencies.json', closure(roots))
    exports = [{'path': str(q.relative_to(a)), **pin(q)} for q in sorted(a.rglob('*')) if q.is_file()]
    write(a/'manifest.json', {'status': 'L063_L064_'+name.upper()+'_AWAITING_DISTINCT_REVIEW', 'exports': exports})
    print(name, pin(a/'manifest.json')['sha256'], 'dependencies', len(json.loads((a/'dependencies.json').read_text())), 'exports',len(exports))


subfield_scope = {
    'sources': ['L063', 'L064'],
    'source_claims': [
        {'claims': 'L063 Lemma 5.11, Proposition 5.12, Table 4 row 1; L064 Lemma 21, Proposition 22', 'disposition': 'CORRECTED_COMPLETE_AFFINE_FAMILY', 'qualification': 'Published m=2 restriction and appendix Proposition22 exhaustivity false; appendix Lemma21 already states the affine type. Fixed-Borel uniqueness and all affine covers proved; existing scalar counts reused.'},
        {'claims': 'Table 4 rows 2--4', 'disposition': 'RECOVERED', 'result': 'The three q=4 configurations each have one inner and one automorphism class.'},
        {'claims': 'Table 4 row 5 = Table 1 row 1', 'disposition': 'RECOVERED_WITH_PARAMETER_REDUCTION', 'result': 'Unique A5,D30,D10 configuration; prime exponent condition reduces to q=16.'},
        {'claims': 'L063 Lemmas 5.13--5.15 and Proposition 5.16; L064 Lemmas 23--25 and Proposition 26', 'disposition': 'COMPLETE_ODD_SUBFIELD_EXCLUSION_WITH_PREVIOUS_COUNT_CORRECTION', 'qualification': 'Odd prime extension degree; s=3 is the sole surviving case, whose unordered counts are reused from scalar_orbits.'},
        {'claims': 'L063 Lemma 5.18 / Proposition 5.21; L064 Lemma 28 / Proposition 30; Table 6 row 1', 'disposition': 'RECOVERED', 'result': 'Two inner and one automorphism class of quadratic affine configurations.'},
        {'claims': 'L063 Lemmas 5.19--5.20; L064 Lemma 29; Table 6 row 2', 'disposition': 'RECOVERED', 'result': 'Unique same-type projective overgroup; q=9 A5 exception has two inner and one automorphism class; q=25 S4 intersection has no second parabolic.'},
        {'claims': 'L063 Lemma 5.17, L064 Lemma 27 and Table 6 row 3', 'disposition': 'REUSED_ACCEPTED_Q9_GEOMETRY', 'qualification': 'The separately accepted full q9 proof supplies the configuration and graph group.'},
        {'claims': 'L064 proof of Lemma 24, item 2, physical page14', 'disposition': 'AUXILIARY_ASSERTION_CORRECTED', 'result': 'PGL2(3) and PGL2(3^m) do embed in PSL2(3^(2m)); the actual A5 exclusion follows from the representation interface and order.'}
    ],
    'classical_premises': ['Dickson subgroup types and subfield embeddings', 'Maximal subfield groups and their conjugacy classes', 'Small exceptional normalizers and class fusion', 'Elementary A5 subgroup lattice'],
    'contributions': ['Literal affine coordinates and complete cover argument', 'Pointwise Frobenius descent for transporters, with centralizer proof', 'Uniform uniqueness of projective overgroups and exact source joins'],
    'collaboration': 'The parent reviewed the draft and requested the explicit distinction between pointwise K-definition and setwise Frobenius stability, and the odd-characteristic scope of the centralizer paragraph.'
}

exceptional_scope = {
    'sources': ['L063', 'L064'],
    'source_claims': [
        {'claims': 'Table 1 rows 5--8 and 15; Table 3 rows 1--8', 'disposition': 'RECOVERED', 'result': 'Normalizer parity gives all equal-type inner counts; unique cyclic rotations give all mixed dihedral counts. Every automorphism count is one.'},
        {'claims': 'Table 1 rows 9--11 and 16--17; Table 3 row 9; Table 6 row 2', 'disposition': 'RECOVERED_WITH_EMPTY_ALTERNATIVES_IDENTIFIED', 'result': 'A4 normalizer proof gives equal and mixed exceptional counts; q=-1 mod40 alternative is empty in square-field rows16--17.'},
        {'claims': 'Table 1 rows 12--14 and 18', 'disposition': 'EMPTY_PARAMETER_BRANCHES', 'result': 'The common hypotheses q=p^2=-1 mod5 imply q=9 mod40; each listed extra condition is impossible. No numerical counterexample is claimed.'},
        {'claims': 'L063 Proposition 5.5', 'disposition': 'FULL_NORMALIZER_COUNT_JOIN_WITH_REUSE', 'qualification': 'Rows1--4 and characteristic-five odd-degree exclusions are supplied by the separate subfield and accepted scalar proofs.'},
        {'claims': 'L063 Proposition 5.10; L064 Proposition 20', 'disposition': 'RECOVERED_COMPLETE_COUNTS', 'qualification': 'Full graph automorphism identifications remain supplied by their separately accepted components.'}
    ],
    'classical_premises': ['Exceptional maximal-subgroup conjugacy and outer fusion', 'Cyclic torus and dihedral normalizer structure', 'A4 ambient normalizers and conjugacy', 'Small A5 and S4 subgroup lattices'],
    'contributions': ['One transporter argument for both equal-type class patterns', 'Explicit torus-normalizer parity calculation', 'A4 mixed-pair normalizer orbit and empty-parameter audit']
}

if __name__ == '__main__':
    freeze('subfield_configurations', 'subfields', 7,
           ['L063-18','L063-19','L063-20','L064-11','L064-12','L064-13','L064-14','L064-18','L064-19','L064-20','L064-21'],
           ['overgroups_root_adoption','scalar_orbits_root_review','q9_geometry_root_adoption'], subfield_scope)
    freeze('exceptional_pairs', 'exceptional', 4,
           ['L063-15','L063-16','L064-05','L064-06','L064-07','L064-08','L064-09','L064-10'],
           ['overgroups_root_adoption','scalar_orbits_root_review','s4_automorphisms_root_adoption','subdivision_automorphisms_root_adoption','subfield_configurations'], exceptional_scope)
