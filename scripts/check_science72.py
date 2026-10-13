"""Check the single-original L071 registration and its public evidence."""
from pathlib import Path
import argparse
import ast
import copy
import hashlib
import json

AUD = 'audit/science72/v1'
REC = 'audit/recoveries/L071/v1'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''):
            h.update(b)
    return h.hexdigest()


def load(root, name):
    return json.loads((root / name).read_text())


def bind(root, row):
    p = root / row['path']
    need(not Path(row['path']).is_absolute() and p.resolve().is_relative_to(root.resolve()),
         'binding escapes public repository')
    need(p.is_file() and sha(p) == row.get('stored_sha256', row['sha256']),
         'public binding changed: ' + row['path'])
    size = row.get('stored_bytes', row.get('bytes'))
    if size is not None:
        need(p.stat().st_size == size, 'public binding size changed')


def semantics(current, old, admission, scope):
    need(set(current['admitted_original_ids']) == set(old['admitted_original_ids']) | {'L071'},
         'only L071 added')
    need(len(current['admitted_original_ids']) == current['admitted_principal_originals'] == 72,
         '72 unique recovered originals')
    need(set(current['accessible_pending_original_ids']) ==
         set(old['accessible_pending_original_ids']) - {'L071'} and
         len(current['accessible_pending_original_ids']) == current['accessible_pending_complete_recovery'] == 33,
         'only L071 removed from pending')
    for key in ('measurement_pending_original_ids', 'scientific_unmeasured_original_ids'):
        need(set(current[key]) == set(old[key]) | {'L071'} and len(current[key]) == 19,
             'nineteen unmeasured originals')
    for key in ('active_original_ids', 'archived_original_ids', 'measured_original_ids',
                'added_measurements', 'current_topic_replacements', 'editorial_original_ids'):
        need(current[key] == old[key], 'unchanged scope or measurements: ' + key)
    need(current['currently_measured_originals'] == 53 and current['originals'] == 106 and
         current['editorial_originals'] == 1, 'fixed partition')
    need(admission['source_ids'] == ['L071'] and admission['principal_originals_added'] == 1 and
         admission['whole_original_credit'] == 0,
         'one proposed recovery, final credit granted by root publication gate')
    need(not admission['literal_theorem_sets_equivalent'] and
         not admission['all_original_assertions_claimed'], 'corrections remain explicit')
    need([x['id'] for x in admission['explicit_corrections']] ==
         ['COMPATIBLE_ACTION', 'H3_DISCONNECTED'], 'both source corrections')
    need(set(admission['component_acceptance']) ==
         {'compatible_actions', 'alternating', 'Co3', 'remaining_censuses'}, 'all four components')
    need(all(set(c) == {'author', 'distinct_review', 'root_adoption'}
             for c in admission['component_acceptance'].values()), 'complete review chains')
    need(len(scope['routes']) == 15 and len({r['id'] for r in scope['routes']}) == 15,
         'fifteen source dispositions')
    evidence = admission['finite_evidence']
    need([evidence[k] for k in ('alternating_ordered_classes', 'Co3_ordered_classes',
         'remaining_ordered_tuples', 'source_markings', 'Co3_source_cells')] ==
         [12904,22908,6868,6047,824], 'complete finite coverage')
    need(evidence['comparison_total_counts_alone_insufficient'] is True,
         'actual source bijections required')
    need(admission['compression_factor'] is admission['software_inclusive_factor'] is None and
         admission['new_question_credit'] == admission['new_Lean_declarations'] == 0 and
         not admission['whole_source_formalized'] and not admission['measured'], 'no added measurement or formal credit')


def verify(root, require_root=True):
    root = Path(root).resolve()
    history = load(root, AUD + '/history_routes.json')['routes']
    for row in history.values():
        bind(root, row)
    old = load(root, history['audit/corpus/latest.json']['path'])
    current = load(root, 'audit/corpus/latest.json')
    ad = load(root, REC + '/admission.json')
    scope = load(root, REC + '/scope_routes.json')
    semantics(current, old, ad, scope)
    for k in ('active_catalogue', 'snapshot', 'current_science_registration'):
        bind(root, current[k])
    need(load(root,current['snapshot']['path']) ==
         {k:v for k,v in current.items() if k != 'snapshot'}, 'exact current snapshot')
    cat = load(root, current['active_catalogue']['path'])
    oldcat = load(root, old['active_catalogue']['path'])
    need(len(cat['entries']) == len(oldcat['entries']) == 106, 'fixed original catalogue')
    for before, after in zip(oldcat['entries'],cat['entries']):
        if before['original_id'] != 'L071':
            need(before == after, 'another original changed')
        else:
            for key in set(before) - {'current_principal_recovery','next_obligation'}:
                need(before[key] == after[key], 'L071 historical data changed')
            recovery = after['current_principal_recovery']
            need(recovery['historical_admission_evidence'] == before['current_principal_recovery'] and
                 recovery['principal_contract_admitted'] and not recovery['measured'],
                 'L071 recovery and historical boundary')
    reg = load(root, current['current_science_registration']['path'])
    need(reg['source_ids'] == ['L071'] and reg['previous_registration'] == old['current_science_registration'],
         'one registration with exact predecessor')
    for row in reg['admissions']:
        bind(root,row)
    for component in ad['component_acceptance'].values():
        for row in component.values():
            bind(root,row)
    for row in ad['complete_acquired_proofs'].values():
        bind(root,row)
    for entry in ad['new_native_manuscripts']:
        bind(root,entry['tex']); bind(root,entry['pdf'])
    t = load(root, REC + '/transport.json')
    need(sha(root / (REC+'/transport.json')) == ad['portable_transport']['sha256'] and
         t['logical_files'] == 1057 and len(t['packets']) == 21, 'complete exact transport')
    unique = {r['public_path']:r for r in t['files'] if 'public_path' in r}
    for path,row in unique.items():
        bind(root,dict(row,path=path))
    need(len(unique) == 688, 'all public payloads')
    replay = load(root, AUD + '/reports/portable.json')
    need(replay['status'] == 'PASS_PUBLIC_RESTORATION_AND_COMPLETED_RECEIPT_CHECKS' and
         replay['transport_sha256'] == ad['portable_transport']['sha256'] and
         not replay['private_proof_fallback'] and not replay['source_content_reread'] and
         replay['checks'] == ['alternating','co3','remaining','source_comparison'], 'portable executed checks')
    for code in replay['programs']:
        bind(root,dict(code,path=REC+'/checker/'+code['path']))
    previous = load(root, history['papers/catalogue_corrected_unmeasured.json']['path'])
    native = load(root, 'papers/catalogue_corrected_unmeasured.json')
    need(native['entries'][:-5] == previous['entries'] and
         native['original_ids'] == previous['original_ids'] + ['L071'] and
         native['existing_comparison_topic_count'] == 19 and native['new_measurements'] == 0,
         'unchanged prior science and measurements')
    need([e['physical_pages'] for e in native['entries'][-5:]] == [2,2,2,3,2],
         'five complete application documents')
    paper = load(root,'papers/latest_catalogue.json')
    oldpaper = load(root,history['papers/latest_catalogue.json']['path'])
    for k in set(oldpaper)-{'status','active_source_catalogue','corrected_unmeasured_scientific_catalogue'}:
        need(paper[k] == oldpaper[k], 'prior paper routing changed')
    need(paper['active_source_catalogue'] == current['active_catalogue'], 'current paper routing')
    bind(root,paper['corrected_unmeasured_scientific_catalogue'])
    oldtree = ast.parse((root/history['scripts/verify_snapshot.py']['path']).read_text())
    newtree = ast.parse((root/'scripts/verify_snapshot.py').read_text())
    def functions(tree):
        return {n.name:ast.dump(n,include_attributes=False) for n in tree.body
                if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name != 'main'}
    oldf,newf=functions(oldtree),functions(newtree)
    need(all(newf.get(k)==v for k,v in oldf.items()), 'old verifier functions changed')
    added = {'check_previous_science72', 'check_science72'}
    need(set(newf)-set(oldf)==added, 'only two new verifier functions')
    def preserved_nodes(tree, exclusions):
        return [ast.dump(n,include_attributes=False) for n in tree.body
                if not (isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name in exclusions)]
    need(preserved_nodes(oldtree,{'main'}) == preserved_nodes(newtree,{'main'}|added),
         'imports, constants or other original top-level code changed')
    controls=[]
    for label,edit in [
        ('duplicate original',lambda c,a,s:c['admitted_original_ids'].append('L071')),
        ('extra pending removed',lambda c,a,s:c['accessible_pending_original_ids'].pop()),
        ('invent factor',lambda c,a,s:a.update(compression_factor=2)),
        ('literal equivalence',lambda c,a,s:a.update(literal_theorem_sets_equivalent=True)),
        ('missing route',lambda c,a,s:s['routes'].pop()),
        ('missing review',lambda c,a,s:a['component_acceptance']['Co3'].pop('distinct_review'))]:
        c,a,s=copy.deepcopy((current,ad,scope));edit(c,a,s)
        try: semantics(c,old,a,s)
        except (ValueError,KeyError): controls.append(label)
        else: raise ValueError('invalid registration accepted: '+label)
    if require_root:
        gate=load(root,AUD+'/root_integration.json')
        need(gate['status']=='ROOT_ACCEPTED_SCIENCE72_PUBLICATION' and
             gate['source_ids']==['L071'] and gate['whole_original_credit']==1,
             'root publication acceptance supplies final whole-original credit')
        for row in gate['bindings']:
            bind(root,row)
    return dict(status='PASS_SCIENCE72_PUBLICATION',counts=dict(active=106,
        corrected_recoveries=72,measured=53,unmeasured=19,mathematical_pending=33,
        editorial=1,archived=55,comparison_topics=19),source_ids=['L071'],
        old_verifier_functions_preserved=len(oldf),public_payloads=len(unique),controls=controls)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--preflight',action='store_true');a=p.parse_args()
    print(json.dumps(verify(a.repo,require_root=not a.preflight)))
