"""Acquire the accepted evidence and check the complete L091 occurrence join.

No subgroup, geometry, or automorphism search is run.  The named group
conclusions are acquired from reviewed proofs; numeric orders alone are
not used to infer abstract group names.  Fresh native compilation is of
the synthesis, with the accepted proof PDFs appended unchanged.
"""
from pathlib import Path
import argparse, collections, copy, hashlib, json, re, shutil, subprocess, time

P = Path(__file__).resolve().parent
H = P.parent
S = H.parent.parent


def load(p):
    return json.loads(Path(p).read_text())


def need(condition, message):
    if not condition:
        raise ValueError(message)


def pin(p):
    p = Path(p)
    h = hashlib.sha256()
    size = 0
    with p.open('rb') as f:
        for data in iter(lambda: f.read(1 << 20), b''):
            size += len(data)
            h.update(data)
    return {'path': str(p), 'bytes': size, 'sha256': h.hexdigest()}


def same_content(a, b):
    return a['bytes'] == b['bytes'] and a['sha256'] == b['sha256']


def write(p, value):
    p.write_text(json.dumps(value, indent=2) + '\n')


def ledger_check(catalogue, corrections, claims, gates, registry):
    rows = catalogue['rows']
    expected_labels = {f'{r}.{i}' for r, n in [(2, 6), (3, 30), (4, 41), (5, 8), (6, 1)]
                       for i in range(1, n + 1)}
    need(len(rows) == 86 and {r['label'] for r in rows} == expected_labels,
         'all 86 original diagram labels exactly once')
    need(sorted(r['representative'] for r in rows) == list(range(1, 87)),
         'bijection with every actual representative')
    profiles = {r['label']: r for r in load(H/'supplement_source_audit_v1/full_diagram_transcription.json')['profiles']}
    coordinates = {r['label']: r for r in load(H/'source_coordinates_v1/joins.json')['rows']}
    local_source = load(H/'local_structure_atoms_v1/source_joins.json') + load(H/'local_structure_compound_v1/source_joins.json')
    locals_by_key = {r['key']: r for r in local_source}
    par_source = load(H/'parabolic_structure_frozen01/source_join/source_joins.json')['rows']
    pars_by_key = {r['key']: r for r in par_source}
    need(len(locals_by_key) == 398 and len(pars_by_key) == 312, 'accepted occurrence domains')
    gate_by_folder = {Path(g['folder']).name: g for g in gates}
    seen_local, seen_par = set(), set()
    computed_groups, blanks = [], []
    counts = collections.Counter()
    for r in rows:
        label, rep, rank = r['label'], r['representative'], r['rank']
        src, coord = profiles[label], coordinates[label]
        need(r['original'] == src and r['coordinate_join'] == coord, 'unaltered source and coordinate records')
        need(r['physical_page'] == src['page'] and rank == int(label.split('.')[0]), 'literal source coordinates')
        need(rep == coord['representative'] and r['source_to_model_types'] == coord['source_to_model_types'], 'exact source-to-model map')
        need(sorted(r['source_to_model_types']) == list(range(1, rank + 1)), 'type map is a bijection')
        need(len(r['local_structures']) == rank + 1 and len(r['parabolic_structures']) == rank, 'every local and parabolic slot')
        want_local = {f'{rep}:B'} | {f'{rep}:K{i}' for i in range(1, rank + 1)}
        want_par = {f'{rep}:P{i}' for i in range(1, rank + 1)}
        need({x['key'] for x in r['local_structures']} == want_local, 'all Borel and kernel keys')
        need({x['key'] for x in r['parabolic_structures']} == want_par, 'all parabolic keys')
        for x in r['local_structures']:
            need(x['key'] not in seen_local and x == locals_by_key[x['key']], 'unchanged unique local proof occurrence')
            need(x['label'] == label and x['page'] == r['physical_page'], 'local source label')
            if x['source_type'] is not None:
                need(x['model_type'] == r['source_to_model_types'][x['source_type'] - 1], 'kernel source type transport')
            seen_local.add(x['key'])
        for x in r['parabolic_structures']:
            need(x['key'] not in seen_par and x == pars_by_key[x['key']], 'unchanged unique parabolic proof occurrence')
            need(x['label'] == label and x['page'] == r['physical_page'], 'parabolic source label')
            need(x['model_type'] == r['source_to_model_types'][x['source_type'] - 1], 'parabolic source type transport')
            need(x['kernel'] == locals_by_key[f"{rep}:K{x['model_type']}"], 'same actual distinguished kernel')
            need(x['orders']['P'] == x['orders']['K'] * x['orders']['Q'], 'exact extension order')
            seen_par.add(x['key'])
        g = r['actual_full_groups']
        need(g['review'] in gate_by_folder, 'accepted full-group review gate')
        need((H/g['proof']/'manifest.json').exists(), 'actual full-group proof packet')
        changes = []
        for field in ['Aut', 'Cor']:
            item = dict(label=label, page=src['page'], field=field, printed=src['printed_'+field],
                        proved=g[field], proof=g['proof'], review=g['review'])
            if item['printed'] == 'BLANK':
                blanks.append(item)
            elif item['printed'] != item['proved']:
                computed_groups.append(item)
                changes.append(item)
        need(r['group_changes'] == changes, 'all printed full-group differences')
        counts[rank] += 1
    need(seen_local == set(locals_by_key) and seen_par == set(pars_by_key), 'complete occurrence coverage')
    need(counts == {2: 6, 3: 30, 4: 41, 5: 8, 6: 1}, 'source rank partition')
    batches = catalogue['full_group_batches']
    need(len(batches) == 10, 'eight batches and two exceptional pairs')
    covered = []
    byrep = {r['representative']: r for r in rows}
    for b in batches:
        need(b['review'] in gate_by_folder, 'every group batch accepted')
        for i in b['representatives']:
            need(byrep[i]['actual_full_groups']['proof'] == b['proof'] and
                 byrep[i]['actual_full_groups']['review'] == b['review'], 'full-group assignment and review')
            covered.append(i)
    need(sorted(covered) == list(range(1, 87)), 'full-group batches are exhaustive and disjoint')
    order = {'HS': 44352000, 'Aut(HS)': 88704000, 'HS x 2': 88704000,
             'HS x 2^2': 177408000, 'Aut(HS) x 2': 177408000}
    for b in batches:
        expected = H/b['proof']/'expected_groups.json'
        if expected.exists():
            actual = load(expected)
            need(sorted(x[0] for x in actual) == b['representatives'], 'group-order source covers exact batch')
            for x in actual:
                g = byrep[x[0]]['actual_full_groups']
                need([order[g['Aut']], order[g['Cor']]] == x[4:6], 'acquired full-group orders')
    need(corrections['full_group_fields'] == computed_groups and len(computed_groups) == 8, 'eight changed full-group fields')
    need(corrections['blank_metadata_completed'] == blanks and len(blanks) == 2 and
         {b['label'] for b in blanks} == {'3.10'}, 'two blank fields, not source errors')
    numeric = []
    for r in rows:
        c = r['coordinate_join']
        if c['type_size_correction']:
            numeric.append(dict(label=r['label'], page=r['physical_page'], kind='type_size', detail=c['type_size_correction']))
        numeric.extend(dict(label=r['label'], page=r['physical_page'], kind=d['kind'], detail=d)
                       for d in c['diagram_differences'])
    need(numeric == corrections['numerical_diagrams'] and len(numeric) == 8 and
         len({x['label'] for x in numeric}) == 6, 'all eight numerical clauses on six diagrams')
    lc = load(H/'local_structure_atoms_v1/corrections.json') + load(H/'local_structure_compound_v1/corrections.json')
    pc = load(H/'parabolic_structure_frozen01/source_join/corrections.json')
    need(corrections['local_occurrences'] == lc and len(lc) == 11, 'eleven acquired local corrections')
    need(corrections['parabolic_occurrences'] == pc and len(pc) == 26, 'twenty-six corrected parabolic slots')
    alias, other = [], []
    for r in pc:
        for c in r['corrections']:
            if c['kind'] == 'ACQUIRED_KERNEL_CORRECTION':
                need(c['acquired_key'] in {q['key'] for q in lc}, 'parabolic correction aliases existing kernel')
                alias.append(dict(parabolic_slot=r['key'], label=r['label'], kernel_slot=c['acquired_key']))
            else:
                other.append(dict(slot=r['key'], label=r['label'], page=r['page'], source_type=r['source_type'],
                                  printed=r['raw_label'], correction=c))
    need(corrections['parabolic_existing_kernel_links'] == alias and len(alias) == 5, 'five aliases, no double count')
    need(corrections['parabolic_additional_clauses'] == other and len(other) == 22, 'twenty-two further structural clauses')
    need(len(corrections['doubling_qualifications']) == 3 and len(corrections['documentary_repairs']) == 3,
         'operation qualifications and our mistakes remain separate')
    multiplicities = collections.Counter(r['original']['printed_family_multiplicity'] for r in rows)
    need(multiplicities == {1: 42, 2: 44}, 'all individual parenthetic multiplicities')
    flags = load(H/'source_flags_component_v1/claims.json')
    need(len(flags['conjugacy']) == 24 and sum(c['printed_conjugate_in_HS'] for c in flags['conjugacy']) == 11,
         'all conjugacy assertions and negatives')
    need(sum(r['all_residue_primitive_inclusions'] for r in flags['rpri']) == 56, 'all stronger primitivity interfaces')
    first = load(H/'table_one_join_component_v1/result01.json')['rows']
    final = load(H/'j3_table_join_v1/source_join.json')
    need(set(first) == {'M11', 'M12', 'J1', 'M22', 'J2', 'M23', 'HS', 'J3'}, 'all eight comparison rows')
    need(final['conditional_corrected_rank_counts'] == [5, 19, 0, 0, 0] and
         not final['global_coverage_reproved'] and not final['no_higher_rank_reproved'] and
         final['retained_reference'] == 'L091 [9] = L097', 'J3 finite answer and explicit retained coverage')
    need(corrections['auxiliary_J3_not_L091_new_claims'] == final['auxiliary_corrections_retained'], 'auxiliary corrections keep their own scope')
    need([x['group'] for x in corrections['main_comparison']] == ['M12', 'J3'], 'comparison corrections separated')
    need(claims['whole_original_credit'] == claims['new_question_credit'] == claims['new_Lean'] == 0 and
         claims['measurement'] is None and claims['principal_HS_counts_unchanged'], 'intake does not assign subsequent credits')
    need(claims['status'] == 'COMPLETE_SOURCE_DISPOSITION_PENDING_DISTINCT_PRINCIPAL_REVIEW', 'distinct whole-original review is still required')
    need(len(claims['claims']) == 19 and len({c['id'] for c in claims['claims']}) == 19, 'every source-claim interface')
    proof_ids = {r['id'] for r in registry}
    for c in claims['claims']:
        need(c['source_locator'] and c['statement'] and c['proof_chapters'] and
             set(c['proof_chapters']) <= proof_ids, 'each source claim points to complete acquired arguments')
    lookup = {c['id']: c for c in claims['claims']}
    need(lookup['Table1.geometry']['disposition'] == 'QUALIFIED_CORRECTED_COMPARISON' and
         'L091[9]' in lookup['Table1.geometry']['qualification'], 'comparison is not silently strengthened')
    need(lookup['HS.doublings']['disposition'] == 'FIVE_PROVED_THREE_OPERATION_QUALIFICATIONS', 'doubling scope is explicit')
    need(lookup['HS.extension_problem']['disposition'] == 'RECOVERED_OLD_PARTIAL_RESULT', 'old partial problem answer is not a new solution')
    return {'source_diagrams': 86, 'local_occurrences': 398, 'parabolic_occurrences': 312,
            'full_groups': 86, 'claim_interfaces': 19, 'comparison_rows': 8,
            'group_corrections': 8, 'blank_fields_completed': 2,
            'numerical_diagrams_corrected': 6, 'numerical_clauses_corrected': 8,
            'local_corrections': 11, 'parabolic_slots_corrected': 26,
            'existing_kernel_aliases': 5, 'additional_parabolic_clauses': 22}


def controls(catalogue, corrections, claims, gates, registry):
    mutations = [
        ('omitted diagram', lambda a, b, c: a['rows'].pop()),
        ('duplicated actual representative', lambda a, b, c: a['rows'][0].update(representative=a['rows'][1]['representative'])),
        ('wrong source type transport', lambda a, b, c: a['rows'][0].update(source_to_model_types=[1, 2])),
        ('omitted actual kernel', lambda a, b, c: a['rows'][0]['local_structures'].pop()),
        ('wrong parabolic kernel', lambda a, b, c: a['rows'][0]['parabolic_structures'][0]['orders'].update(K=2)),
        ('duplicated full-group case', lambda a, b, c: a['full_group_batches'][0]['representatives'].append(14)),
        ('blank counted as source error', lambda a, b, c: b['full_group_fields'].append(b['blank_metadata_completed'][0])),
        ('kernel correction counted twice', lambda a, b, c: b['parabolic_existing_kernel_links'].pop()),
        ('unqualified global J3 claim', lambda a, b, c: next(x for x in c['claims'] if x['id']=='Table1.geometry').update(disposition='PROVED_GLOBAL_CENSUS')),
        ('old partial answer called new', lambda a, b, c: next(x for x in c['claims'] if x['id']=='HS.extension_problem').update(disposition='NEW_CONJECTURE_SOLVED')),
    ]
    results = []
    for name, mutate in mutations:
        a, b, c = copy.deepcopy((catalogue, corrections, claims))
        mutate(a, b, c)
        try:
            ledger_check(a, b, c, gates, registry)
        except (ValueError, KeyError, IndexError) as e:
            results.append({'damage': name, 'rejected': True, 'reason': str(e)})
        else:
            raise ValueError('unrejected damage: ' + name)
    return results


def native(out, registry):
    from pypdf import PdfReader
    d = out/'native'
    d.mkdir()
    for name in ['synthesis.tex', 'complete.tex', 'manuscript_body.tex', 'class_table.tex', 'proof_index.tex']:
        shutil.copy2(P/name, d/name)
    (d/'proofs').symlink_to(P/'proofs', target_is_directory=True)
    for name in ['synthesis', 'complete']:
        for k in range(3):
            run = subprocess.run(['/opt/homebrew/bin/pdflatex', '-interaction=nonstopmode', '-halt-on-error', name+'.tex'],
                                 cwd=d, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
            (d/f'{name}_compile{k+1}.txt').write_bytes(run.stdout)
            need(run.returncode == 0, 'successful native compilation: ' + name)
        log = (d/(name+'.log')).read_text(errors='replace')
        need('Overfull' not in log and 'undefined references' not in log and 'Rerun to' not in log,
             'native layout and cross references: ' + name)
    chapter_pages = sum(len(PdfReader(P/r['copied_pdf']).pages) for r in registry)
    main_pages = len(PdfReader(d/'synthesis.pdf').pages)
    complete_pages = len(PdfReader(d/'complete.pdf').pages)
    need(complete_pages == main_pages + 1 + chapter_pages, 'every full accepted proof page appended')
    run = subprocess.run(['/opt/homebrew/bin/gs', '-q', '-dSAFER', '-dBATCH', '-dNOPAUSE',
                          '-sDEVICE=png16m', '-r100', '-sOutputFile='+str(d/'page%02d.png'), str(d/'synthesis.pdf')],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
    (d/'render.txt').write_bytes(run.stdout)
    need(run.returncode == 0 and len(list(d.glob('page*.png'))) == main_pages, 'all new manuscript pages rendered')
    return {'synthesis_pages': main_pages, 'unchanged_accepted_chapter_pages': chapter_pages,
            'complete_volume_pages': complete_pages, 'native_pages_directly_viewed': False}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', required=True, type=Path)
    args = ap.parse_args()
    out = args.out.resolve()
    need(not out.exists(), 'fresh output directory required')
    out.mkdir(parents=True)
    start = time.monotonic()
    dependencies = load(P/'dependencies.json')
    bypath = {}
    for r in dependencies:
        need(r['path'] not in bypath, 'flat dependency paths are unique')
        need(pin(r['path']) == r, 'changed acquired dependency: ' + r['path'])
        bypath[r['path']] = r
    print(json.dumps({'fresh_acquired_bindings': len(bypath)}), flush=True)
    gates, registry = load(P/'gates.json'), load(P/'proof_registry.json')
    need(len(gates) == 31 and len({g['folder'] for g in gates}) == 31, 'all 31 distinct gates and explicit addendum')
    for g in gates:
        need(bypath.get(g['manifest']['path']) == g['manifest'], 'review manifest is acquired')
        manifest = load(g['manifest']['path'])
        status = manifest.get('status')
        if status is None:
            status = load(Path(g['folder'])/'review.json').get('status', manifest.get('schema', 'MANIFEST_WITH_EXPLICIT_REVIEW'))
        need(status == g['status'], 'exact review status')
        if Path(g['folder']).name == 'parabolic_naming_addendum_v1':
            adoption = load(H/'parabolic_structure_root_adoption/dependencies.json')
            need(g['manifest'] in adoption, 'author naming addendum is actually adopted by the distinct root review')
        else:
            need('ACCEPTED' in status or status.startswith('ROOT_ADOPTED'), 'explicit accepted component gate')
        for e in manifest.get('exports', []):
            path = Path(e['path'])
            if not path.is_absolute():
                path = Path(g['folder'])/path
            need(str(path) in bypath and same_content(bypath[str(path)], e), 'exact review exports acquired')
    need([r['id'] for r in registry] == [f'{i:02d}' for i in range(1, 27)], 'all 26 accepted chapters')
    for r in registry:
        for key in ['source_tex', 'source_pdf', 'review']:
            need(bypath.get(r[key]['path']) == r[key], 'chapter proof and review acquired')
        need(same_content(pin(P/r['copied_tex']), r['source_tex']) and
             same_content(pin(P/r['copied_pdf']), r['source_pdf']) and r['unchanged'], 'unchanged accepted complete proof chapter')
    for src in load(P/'claims.json')['fixed_sources']:
        need(bypath.get(src['path']) == src, 'fixed source edition acquired')
    catalogue, corrections, claims = [load(P/n) for n in ['source_catalogue.json', 'corrections.json', 'claims.json']]
    joined = ledger_check(catalogue, corrections, claims, gates, registry)
    damaged = controls(catalogue, corrections, claims, gates, registry)
    rendering = native(out, registry)
    report = dict(status='PASS_COMPLETE_L091_SOURCE_JOIN_PENDING_DISTINCT_PRINCIPAL_REVIEW',
                  fresh_acquired_bindings=len(bypath), accepted_gates=30, adopted_named_addendum=1,
                  exact_unchanged_chapters=26, join=joined, damage_controls=damaged, native=rendering,
                  scientific_targets=0, new_question_credit=0, whole_original_credit=0, new_Lean=0,
                  measurement=None, seconds=time.monotonic()-start)
    write(out/'report.json', report)
    write(out/'inputs.json', [pin(P/n) for n in ['verify.py', 'source_catalogue.json', 'corrections.json', 'claims.json',
                                               'gates.json', 'proof_registry.json', 'dependencies.json',
                                               'synthesis.tex', 'complete.tex', 'manuscript_body.tex',
                                               'class_table.tex', 'proof_index.tex']])
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
