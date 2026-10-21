"""Check the single-original F006 registration and its public evidence."""
from pathlib import Path
import argparse
import ast
import copy
import hashlib
import json

AUD = 'audit/science74/v1'
REC = 'audit/recoveries/F006/v1'


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
    need(set(current['admitted_original_ids']) == set(old['admitted_original_ids']) | {'F006'}, 'only F006 added')
    need(len(current['admitted_original_ids']) == current['admitted_principal_originals'] == 74, '74 unique recoveries')
    need(set(current['accessible_pending_original_ids']) == set(old['accessible_pending_original_ids']) - {'F006'} and len(current['accessible_pending_original_ids']) == current['accessible_pending_complete_recovery'] == 30, 'only F006 removed from pending')
    need(set(current['handled_mathematical_original_ids']) == set(old['handled_mathematical_original_ids']) | {'F006'} and len(current['handled_mathematical_original_ids']) == current['handled_mathematical_originals'] == 75, '75 handled originals')
    for key in ('measurement_pending_original_ids','scientific_unmeasured_original_ids'):
        need(set(current[key]) == set(old[key]) | {'F006'} and len(current[key]) == 21, 'twenty-one unmeasured originals')
    for key in ('active_original_ids','archived_original_ids','measured_original_ids','added_measurements','current_topic_replacements','editorial_original_ids','refuted_principal_originals','refuted_principal_original_ids','principal_refutation_admissions','all_mathematical_originals_handled'):
        need(current[key] == old[key], 'unchanged scope, refutation or measurement: '+key)
    need(current['currently_measured_originals']==53 and current['originals']==106 and current['editorial_originals']==1, 'fixed corpus')
    need(admission['source_ids']==['F006'] and admission['principal_originals_added']==1 and admission['whole_original_credit']==0, 'one proposed recovery; final credit requires root gate')
    need(not admission['literal_principal_theorem_recovered'] and admission['complete_principal_contract_recovered'] and not admission['all_original_assertions_claimed'], 'corrected principal scope')
    need(admission['corrected_literal_cases']==['I2(m), m=2 modulo4','H3','E7'] and admission['strict_warning_receipts_preserved'], 'exact disconnected corrections and warning boundary')
    need(set(admission['component_acceptance'])=={'complete'} and all(set(c)=={'author','distinct_review','root_adoption'}for c in admission['component_acceptance'].values()), 'complete review chains')
    need(len(scope['rows'])==24 and len({r['id']for r in scope['rows']})==24, 'twenty-four source routes')
    need(admission['finite_subset_pairs']==14050496 and admission['physical_pages']==21 and admission['exceptional_ordered_tuples']==32603 and admission['printed_source_cells']==42 and len(admission['retained_inputs'])==5, 'complete stated evidence')
    need(admission['compression_factor'] is admission['software_inclusive_factor'] is None and admission['new_question_credit']==admission['new_Lean_declarations']==admission['new_measurements']==0 and not admission['whole_source_formalized'] and not admission['measured'], 'no new factor or formal claim')


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
        if before['original_id'] != 'F006':
            need(before == after, 'another original changed')
        else:
            for key in set(before) - {'current_principal_recovery','next_obligation'}:
                need(before[key] == after[key], 'F006 historical data changed')
            recovery = after['current_principal_recovery']
            need(recovery['historical_admission_evidence'] == before['current_principal_recovery'] and
                 recovery['principal_contract_admitted'] and not recovery['measured'],
                 'F006 recovery and historical boundary')
    reg = load(root, current['current_science_registration']['path'])
    need(reg['source_ids'] == ['F006'] and reg['previous_registration'] == old['current_science_registration'],
         'one registration with exact predecessor')
    for row in reg['admissions']:
        bind(root,row)
    for component in ad['component_acceptance'].values():
        for row in component.values():
            bind(root,row)
    for key in ['dependency_locator_correction','source_routes','portable_report','portable_checker','portable_review']:
        bind(root,ad[key])
    for row in load(root,ad['portable_review']['path'])['bindings'].values():
        bind(root,row)
    for row in ad['complete_acquired_proofs'].values():
        bind(root,row)
    for entry in ad['new_native_manuscripts']:
        bind(root,entry['tex']); bind(root,entry['pdf'])
    t = load(root, REC + '/transport.json')
    need(sha(root / (REC+'/transport.json')) == ad['portable_transport']['sha256'] and
         t['logical_files'] == 476 and len(t['packets']) == 8, 'complete exact transport')
    unique = {r['public_path']:r for r in t['files'] if 'public_path' in r}
    for path,row in unique.items():
        bind(root,dict(row,path=path))
    need(len(unique) == 412, 'all public payloads')
    replay = load(root, AUD + '/reports/portable.json')
    need(replay['status']=='PASS_PUBLIC_F006_RESTORATION_AND_RECEIPTS' and replay['transport_sha256']==ad['portable_transport']['sha256'] and not replay['private_proof_fallback'] and not replay['source_content_reread'] and replay['original_warning_receipts_unchanged'] and replay['author_evidence']['exceptional_ordered_tuples']==32603 and replay['author_evidence']['printed_cells']==42 and len(replay['warning_controls'])==13, 'complete portable evidence replay')
    previous = load(root, history['papers/catalogue_corrected_unmeasured.json']['path'])
    native = load(root, 'papers/catalogue_corrected_unmeasured.json')
    need(native['entries'][:-9] == previous['entries'] and
         native['original_ids'] == previous['original_ids'] + ['F006'] and
         native['existing_comparison_topic_count'] == 19 and native['new_measurements'] == 0,
         'unchanged prior science and measurements')
    need([e['physical_pages'] for e in native['entries'][-9:]] == [2,3,3,3,2,2,1,3,2],
         'nine complete immediate proof documents')
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
    added = {'check_previous_science74', 'check_science74'}
    need(set(newf)-set(oldf)==added, 'only two new verifier functions')
    def preserved_nodes(tree, exclusions):
        return [ast.dump(n,include_attributes=False) for n in tree.body
                if not (isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name in exclusions)]
    need(preserved_nodes(oldtree,{'main'}) == preserved_nodes(newtree,{'main'}|added),
         'imports, constants or other original top-level code changed')
    controls=[]
    for label,edit in [
        ('duplicate original',lambda c,a,s:c['admitted_original_ids'].append('F006')),
        ('extra pending removed',lambda c,a,s:c['accessible_pending_original_ids'].pop()),
        ('invent factor',lambda c,a,s:a.update(compression_factor=2)),
        ('auxiliary overclaim',lambda c,a,s:a.update(all_original_assertions_claimed=True)),
        ('missing route',lambda c,a,s:s['rows'].pop()),
        ('missing review',lambda c,a,s:a['component_acceptance']['complete'].pop('distinct_review'))]:
        c,a,s=copy.deepcopy((current,ad,scope));edit(c,a,s)
        try: semantics(c,old,a,s)
        except (ValueError,KeyError): controls.append(label)
        else: raise ValueError('invalid registration accepted: '+label)
    if require_root:
        gate=load(root,AUD+'/root_integration.json')
        need(gate['status']=='ROOT_ACCEPTED_SCIENCE74_PUBLICATION' and
             gate['source_ids']==['F006'] and gate['whole_original_credit']==1,
             'root publication acceptance supplies final whole-original credit')
        for row in gate['bindings']:
            bind(root,row)
        need(load(root,AUD+'/registration_review/review.json')['status']=='ACCEPTED_F006_REGISTRATION','distinct registration review')
    return dict(status='PASS_SCIENCE74_PUBLICATION',counts=dict(active=106,
        corrected_recoveries=74,refuted=1,handled=75,measured=53,unmeasured=21,mathematical_pending=30,
        editorial=1,archived=55,comparison_topics=19),source_ids=['F006'],
        old_verifier_functions_preserved=len(oldf),public_payloads=len(unique),controls=controls)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--preflight',action='store_true');a=p.parse_args()
    print(json.dumps(verify(a.repo,require_root=not a.preflight)))
