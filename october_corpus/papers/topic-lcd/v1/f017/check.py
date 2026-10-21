#!/usr/bin/env python3
"""Portable binding/render review for the F017 application.

This is an author integrity checker, not an independent mathematical review.
Default finite checks are optional small models. --programs deliberately
replays the complete accepted association and Paley certificates.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def load(path):
    return json.loads(path.read_text())


def pin(path):
    b = path.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def exact(path, row):
    actual = pin(path)
    need(all(actual[k] == row[k] for k in actual), 'binding: '+str(path))


def validate(scope, contract, dependencies):
    rows = contract['rows']; ids = [r['id'] for r in rows]
    need(len(rows) == 104 and len(set(ids)) == len(rows), 'complete source row set')
    need(contract['source']['sha256'] == '22296f2e3915fda096a03946af29fd8bbd1bd1606a5a1848b6d2e78c541476ce', 'source edition')
    need(contract['physical_pages'] == 17, 'full primary pages')
    need(scope['source_rows'] == len(rows), 'source row count')
    need(scope['new_original_credit'] == scope['new_question_credit'] == 0 and scope['ratio'] is None, 'no admission or ratios')
    need(scope['new_Lean_declarations'] == 0 and scope['reused_partial_Lean_declarations'] == 9
         and scope['formal_full_source'] is False, 'limited formal scope')
    need(scope['required_programs'] == ['certificates/association/check_association_counts.py',
       'certificates/paley/check_paley_codes.py','certificates/paley/enumerate_sparse_messages.c'], 'whole required files')
    need(scope['required_data'] == ['certificates/association/counts.json','certificates/paley/finite_records/'], 'complete data')
    need(scope['optional_validation'] == ['check_local_bridges.py','finite_subset_rows.json'], 'optional role')
    need(dependencies['common']['full_common_paid'] is True and dependencies['common']['whole_pages'] == 14, 'full common')
    need(dependencies['common']['root_adoption_sha256'] == 'bd3cbb1d290568255d5dd693ec9f1550109c2e7d1f9896ea75b0a33b1ea6dc32', 'accepted common edition')
    need(scope['application_pages'] == 12, 'complete application extent')
    need(dependencies['no_sibling_application_premise'] is True, 'no sibling free proof')
    need(all(v is None for v in dependencies['external_unknowns'].values()), 'unknown external costs')
    indexed = {r['id']: r for r in rows}
    need(indexed['F017.Section6.odd_graph']['disposition'] == 'corrected_formula_and_uniform_proof', 'odd formula correction')
    need(indexed['F017.Result4.weights']['disposition'] == 'corrected_and_proved', 'fiber correction')
    need(indexed['F017.Conclusion.further_classes']['disposition'] == 'historical_context_and_unresolved_beyond_explicit_families', 'question boundary')
    need(indexed['F017.Section6.ternary_triples']['retained_inputs'] == ['ternary_Prop18_memberships'], 'retained ternary membership')
    need(indexed['F017.Result3.k3.3']['retained_inputs'] == ['earlier_distances'], 'ternary distance not proved by rank')
    need(len([x for x in ids if x.startswith('F017.Computational.')]) == 16, 'sixteen findings')
    need(len([x for x in ids if x.startswith('F017.Table1.')]) == 12, 'whole twelve rows')
    for row in rows:
        need(row['application_file'].startswith('sections/') and (HERE/row['application_file']).is_file(), 'proof route')
        need(all(x in dependencies['retained_classical_inputs'] for x in row['retained_inputs']), 'known retained input')


def controls(scope, contract, dep):
    tests = []
    mutations = [
      ('missing_source_row', lambda s,c,d: c['rows'].pop()),
      ('source_edition', lambda s,c,d: c['source'].update(sha256='0'*64)),
      ('source_page_omission', lambda s,c,d: c.update(physical_pages=15)),
      ('admission_not_reviewed', lambda s,c,d: s.update(new_original_credit=1)),
      ('full_formal_overclaim', lambda s,c,d: s.update(formal_full_source=True)),
      ('required_program_demoted', lambda s,c,d: s['required_programs'].pop()),
      ('required_records_omitted', lambda s,c,d: s['required_data'].pop()),
      ('free_common', lambda s,c,d: d['common'].update(full_common_paid=False)),
      ('unknown_as_zero', lambda s,c,d: d['external_unknowns'].update(historical_software=0)),
      ('ternary_distance_free', lambda s,c,d: next(r for r in c['rows'] if r['id']=='F017.Result3.k3.3').update(retained_inputs=[])),
      ('question_solved', lambda s,c,d: next(r for r in c['rows'] if r['id']=='F017.Conclusion.further_classes').update(disposition='solved')),
      ('odd_formula_uncorrected', lambda s,c,d: next(r for r in c['rows'] if r['id']=='F017.Section6.odd_graph').update(disposition='literal_source_proved'))]
    for name, mutate in mutations:
        s,c,d=copy.deepcopy((scope,contract,dep)); mutate(s,c,d)
        try: validate(s,c,d)
        except (RuntimeError,KeyError): tests.append({'name':name,'rejected':True})
        else: raise RuntimeError('mutation accepted: '+name)
    return tests


def command(args, cwd, log):
    run = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    log.write_text(run.stdout+run.stderr)
    need(run.returncode == 0, 'command failed: '+str(log))


def render(out, xelatex):
    from pypdf import PdfReader
    render = out/'render'; render.mkdir()
    for i in range(2):
        command([xelatex,'-interaction=nonstopmode','-halt-on-error','-output-directory='+str(render),
                 'application.tex'], HERE, out/f'render_pass{i+1}.log')
    diagnostics=[line for line in (render/'application.log').read_text().splitlines()
                 if any(k in line for k in ('Warning','Overfull','Missing character','! '))]
    need(not diagnostics, 'render diagnostics: '+repr(diagnostics))
    new=[p.extract_text() for p in PdfReader(render/'application.pdf').pages]
    old=[p.extract_text() for p in PdfReader(HERE/'application.pdf').pages]
    need(new == old, 'all rendered page texts')
    return {'pages':len(new),'all_page_texts_identical':True,'diagnostics':diagnostics,
            'text_sha256':[hashlib.sha256(p.encode()).hexdigest() for p in new]}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--study-root',type=Path)
    parser.add_argument('--render',action='store_true')
    parser.add_argument('--programs',action='store_true')
    parser.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex')
    parser.add_argument('--cc',default='cc')
    args=parser.parse_args()
    need(not args.out.exists(),'fresh output directory required');args.out.mkdir(parents=True)
    manifest=load(HERE/'manifest.json')
    for row in manifest['exports']: exact(HERE/row['path'],row)
    scope,contract,dep=(load(HERE/name) for name in ('scope.json','source_contract.json','dependencies.json'))
    validate(scope,contract,dep)
    for row in dep['exact_copies']: exact(HERE/row['copy'],row)
    proof=load(HERE/'proof_map.json')
    actual_ids=[]
    for row in proof['full_contexts']:
        exact(HERE/row['path'],row);actual_ids.extend(row['source_rows'])
        need(len((HERE/row['path']).read_text().splitlines()) == row['last_line'], 'proof span lines')
    need(sorted(actual_ids)==sorted(r['id'] for r in contract['rows']), 'exact full row routes')
    labels=load(HERE/'common/interface_labels.json')
    for row in contract['rows']: need(all(x in labels for x in row['common_interfaces']), 'common labels')
    source_checked=False
    if args.study_root:
        exact(args.study_root/contract['source']['path'],contract['source'])
        for row in dep['accepted_prior_packets']: exact(args.study_root/row['path'],row)
        for row in dep['exact_copies']: exact(args.study_root/row['origin'],row)
        source_checked=True
    command([sys.executable,'-B','-O',str(HERE/'check_local_bridges.py'),'--out',str(args.out/'local_bridges.json')],
            HERE,args.out/'local_bridges.log')
    program_report={'replayed':False,'accepted_prior_replays_bound':True}
    if args.programs:
        command([sys.executable,'-B','-O',str(HERE/'certificates/association/check_association_counts.py'),
                 '--out',str(args.out/'association.json')],HERE,args.out/'association.log')
        need(load(args.out/'association.json')==load(HERE/'certificates/association/counts.json'),'association exact output')
        binary=args.out/'enumerate_sparse_messages'
        command([args.cc,'-O3','-std=c11','-Wall','-Wextra','-Werror',str(HERE/'certificates/paley/enumerate_sparse_messages.c'),
                 '-o',str(binary)],HERE,args.out/'compiler.log')
        command([sys.executable,'-B','-O',str(HERE/'certificates/paley/check_paley_codes.py'),
                 '--enumerator',str(binary),'--out',str(args.out/'paley')],HERE,args.out/'paley.log')
        new=load(args.out/'paley/report.json');old=load(HERE/'certificates/paley/finite_records/report.json')
        new.pop('enumerator_sha256');old.pop('enumerator_sha256')
        need(new==old,'Paley complete semantic report')
        for p in (HERE/'certificates/paley/finite_records').glob('*'):
            if p.name!='report.json': need(p.read_bytes()==(args.out/'paley'/p.name).read_bytes(),'Paley exact record: '+p.name)
        program_report={'replayed':True,'association_exact_output':True,'paley_cases':12,
                        'exact_distances':16,'minimum_sets':5,'large_pairs_upper_bounds_only':4}
    report={'status':'PASS_AUTHOR_BINDINGS_SCOPE_AND_LOCAL_MODELS',
            'author_manifest':pin(HERE/'manifest.json'),'exports':len(manifest['exports']),
            'source_rows':len(contract['rows']),'proof_contexts':len(proof['full_contexts']),
            'exact_inherited_copies':len(dep['exact_copies']),'source_and_prior_files_checked':source_checked,
            'controls':controls(scope,contract,dep),'local_models':load(args.out/'local_bridges.json'),
            'required_programs':program_report,'formal_fresh_replay':False,
            'formal_scope':'Nine inherited generic declarations only; source-specific claims unformalized.',
            'render':render(args.out,args.xelatex) if args.render else None,
            'distinct_mathematical_acceptance':False,'new_original_credit':0,'ratio':None}
    (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','exports':report['exports'],'source_rows':report['source_rows'],
                      'controls':len(report['controls']),'required_programs_replayed':args.programs,
                      'render_pages':report['render']['pages'] if report['render'] else None}))


if __name__=='__main__':
    main()
