"""Prepared portable saved-certificate reader; no discovery or SAT solver.

Default --describe is metadata only. --reconstruct and --check require a
separately reviewed resource owner; this module does not release itself.
"""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time
from types import SimpleNamespace

if sys.flags.optimize:
    raise RuntimeError('ordinary Python required')
sys.dont_write_bytecode = True

RUNTIME_SHA256 = 'e76919bf176912ac7b655a01fd3c4bc051ebb2c1d14db7a94a09658207ff5799'
source = Path(__file__).with_name('runtime.py')
if source.is_symlink() or hashlib.sha256(source.read_bytes()).hexdigest() != RUNTIME_SHA256:
    raise ValueError('Exact acquired package transport')
spec = importlib.util.spec_from_file_location('f012_saved_transport', source)
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)
need = R.need
INDICES = (0,1,4,5,13,16,27,28,30,31,33,34,35,36,37,38,40,41,42,44,47,48,56,59)
DIGESTS = ('fixed_paths_sha256','cycle_catalogue_sha256','term_catalogue_sha256',
           'cut_catalogue_sha256','unique_clause_sequence_sha256')


def normalized(value):
    return json.loads(json.dumps(value))


def source_module(rt, work, key, name):
    need(rt.files[key]['role'] == 'source', 'Declared scientific source')
    path = rt.resolve(key, work)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixed_obstruction_check(tools,n,base):
    cycles = tools.fixed_cycles(n,base)
    ownership = Counter(tuple(sorted((a,b))) for cycle in cycles if len(cycle) == 6
                        for a,b in zip(cycle,cycle[1:]+cycle[:1]))
    need(not any(len(cycle) < 6 for cycle in cycles) and max(ownership.values(),default=0) <= 1,
         'Recomputed fixed graph has no short cycle or shared-hexagon edge')
    return cycles


def check_transports(rt, work, case, program):
    """Rebuild all seventy domains, then call the unchanged literal map checker."""
    def path(ref):
        key,item = rt.entry(ref['path'])
        need(set(ref) == {'path','bytes','sha256'} and key in case['inputs']
             and (item['bytes'],item['sha256']) == (ref['bytes'],ref['sha256']),
             'Exact complete transport input')
        return rt.resolve(key,work)

    def data(ref):
        return json.loads(path(ref).read_bytes())

    accepted = data(case['setup_acceptance'])
    gate = data(case['transport_acceptance'])
    candidate = data(case['certificate'])
    setup = data(accepted['result'])
    need(accepted['status'] == 'ROOT_ACCEPTED_F012_SEVENTY_T6_MODELS_AND_NECESSARY_CNFS'
         and accepted['models'] == 70 and accepted['host_summaries'] == setup['records']
         and candidate['acceptance'] == case['setup_acceptance']
         and candidate['setup'] == accepted['result']
         and candidate['status'] == 'COMPLETE_DOMAIN_ISOMORPHISM_CANDIDATE'
         and gate['certificate'] == case['certificate']
         and gate['setup_acceptance'] == case['setup_acceptance']
         and tuple(candidate['representatives']) == INDICES,
         'Original complete domain setup and exact acquired map certificate')
    encoder = source_module(rt,work,program['sources']['t6_encoder'],'portable_transport_encoder')
    checker = source_module(rt,work,program['sources']['transport'],'portable_literal_transports')
    H = source_module(rt,work,program['sources']['literal'],'portable_transport_literals')
    fixed = source_module(rt,work,program['sources']['t4_two_encoder'],'portable_fixed_graph_tools')
    need(len(encoder.records()) == len(setup['records']) == 70, 'All seventy declared parent records')
    domains = []
    for i,record in enumerate(setup['records']):
        need(encoder.records()[i] == {k:record[k] for k in ('row','parents')},
             'Raw-domain index, colour and actual parent assignment')
        raw,metadata = encoder.encode(record['row'],record['parents'])
        model = path(record['model'])
        need(raw.encode('ascii') == model.read_bytes(), 'Whole regenerated raw-domain bytes')
        n,base,allowed = H.read_model(model,4096)
        need(n == 54 and len(base) == 66 and len(allowed) <= 261
             and normalized(sorted(base)) == normalized(metadata['fixed_edges'])
             and normalized(sorted(allowed)) == normalized(metadata['allowed_edges']),
             'Complete actual fixed/optional edge domain')
        fixed_obstruction_check(fixed,n,base)
        domains.append((set(base),set(allowed)))
    checker.verify_rows(candidate['assignments'],domains,setup['records'],candidate['representatives'])
    groups = [dict(index=j,row=setup['records'][j]['row'],parents=setup['records'][j]['parents'],
        model=setup['records'][j]['model'],covers=[r['index'] for r in candidate['assignments']
                                                if r['representative'] == j]) for j in INDICES]
    need(groups == gate['representatives'], 'Entire original twenty-four-cover ledger')
    return dict(status='CHECKED_PORTABLE_SEVENTY_DOMAIN_TRANSPORTS',domains=70,
        representatives=groups,exact_models_rebuilt=70,nauty_calls=0,solver_calls=0,
        proof_reads=0,source_credit=0,whole_source_credit=0)


def rebuild(rt, work, case, program):
    """Reconstruct explicit model/state; invoke literal acquired build methods."""
    def path(ref):
        need(type(ref) is dict and set(ref) == {'path','bytes','sha256'}, 'Exact original input pin')
        key, item = rt.entry(ref['path'])
        need((item['bytes'],item['sha256']) == (ref['bytes'],ref['sha256']), 'Same accepted original identity')
        need(key in case['inputs'], 'Per-case closed runtime input roster')
        return rt.resolve(key, work)

    def data(ref):
        return json.loads(path(ref).read_bytes())

    def load(name):
        return source_module(rt, work, program['sources'][name], 'portable_acquired_' + name)

    def same_source(ref, name):
        path(ref)
        need(rt.entry(ref['path'])[0] == program['sources'][name],
             'Original source reference matches the actual imported source: '+name)

    H = load('literal')
    C = H.C
    encoder = load(case['model_encoder'])
    family = case['family']
    if family == 't6':
        need(type(case['index']) is int and case['index'] in INDICES, 'One acquired t6 representative')
        need(encoder.records()[case['index']] == {'row':case['row'],'parents':case['parents']},
             'Exact literal raw-domain index, colour row and actual parents')
        model_bytes, generated = encoder.encode(case['row'],case['parents'])
    elif family == 't5':
        need(case['host'] in ('P0','P1','P2'), 'One acquired t5 host')
        model_bytes, generated = encoder.encode(case['host'])
    else:
        need(family in ('t4_two','t4_three'), 'Declared t4 family')
        model_bytes, generated = encoder.encode()
    need(model_bytes.encode('ascii') == path(case['model']).read_bytes(),
         'Whole regenerated fixed/optional graph-domain bytes')
    n,base,allowed = H.read_model(path(case['model']),4096)
    need(n == 54 and normalized(sorted(base)) == normalized(generated['fixed_edges'])
         and normalized(sorted(allowed)) == normalized(generated['allowed_edges']),
         'Entire literal fixed and optional edge sets, not only dimensions')
    fixed_cycles = fixed_obstruction_check(load('t4_two_encoder'),n,base)
    witnesses = [json.loads(line) for line in path(case['cuts']).read_text().splitlines()]
    need(len(witnesses) == case['expected']['witnesses']
         and len({C.witness_edges(w,n,base,allowed) for w in witnesses}) == len(witnesses),
         'Every actual lazy/universal witness is valid; exact count and distinct clauses')
    evidence = {'family': family, 'model_regenerated': True, 'witnesses': len(witnesses),
                'fixed_cycles':fixed_cycles,'fixed_obstruction_found':False}

    if family in ('t6','t5'):
        selector = data(case['selector'])
        sizing = data(case['sizing_report'])
        metadata = data(case['metadata'])
        need(metadata['model'] == case['model'] and metadata['formula'] == case['original_formula']
             and normalized(metadata['fixed_edges']) == normalized(sorted(base))
             and normalized(metadata['allowed_edges']) == normalized(sorted(allowed)),
             'Acquired original model, metadata and original formula join')
        need(metadata['fixed_obstruction_found'] is False and metadata['fixed_cycles'] == fixed_cycles,
             'Actual fixed-obstruction setup premise independently recomputed')
        K = load(family + '_catalogue')
        provider = load(family + '_provider')
        if family == 't6':
            context = data(selector['context'])
            for field,name in (('provider','t6_provider'),('file_tools','file_tools'),
                    ('catalogue_program','t6_catalogue'),('fixed_predicates','t5_catalogue'),
                    ('literal_tools','literal'),('cnf_program','cnf')):
                same_source(context[field],name)
            setup = data(context['setup_acceptance'])
            transport = data(context['transport_acceptance'])
            catalogue_gate = data(case['catalogue_gate'])
            need(set(selector) == {'schema','index','context','report'}
                 and selector['schema'] == 'F012_FIXED_T6_REQUIRED_HEXAGON_FORMULA_V1'
                 and context['schema'] == 'F012_REMAINING_T6_CATALOGUES_AND_FORMULA_CONTEXT_V1'
                 and setup['status'] == 'ROOT_ACCEPTED_F012_SEVENTY_T6_MODELS_AND_NECESSARY_CNFS'
                 and setup['models'] == len(setup['host_summaries']) == 70
                 and transport['status'] == 'ROOT_ACCEPTED_F012_SEVENTY_TO_TWENTY_FOUR_DOMAINS'
                 and transport['setup_acceptance'] == context['setup_acceptance']
                 and tuple(r['index'] for r in context['records']) == INDICES
                 and tuple(r['index'] for r in transport['representatives']) == INDICES
                 and catalogue_gate['transport_acceptance'] == context['transport_acceptance']
                 and catalogue_gate['status'] == 'ROOT_ACCEPTED_ALL_TWENTY_FOUR_T6_REQUIRED_CATALOGUES_AND_FORMULA_SELECTORS'
                 and tuple(r['index'] for r in catalogue_gate['formula_cases']) == INDICES,
                 'Exact acquired 24-domain catalogue schedule')
            for record, representative in zip(context['records'],transport['representatives']):
                need({k:v for k,v in record.items() if k != 'index'} == setup['host_summaries'][record['index']]
                     and all(record[k] == representative[k] for k in ('index','row','parents','model')),
                     'Entire original 70-model setup to exact 24-selector metadata join')
            selected = next(r for r in catalogue_gate['formula_cases'] if r['index'] == case['index'])
            row = next(r for r in context['records'] if r['index'] == case['index'])
            need(selected['formula_case'] == case['selector'] and selected['report'] == case['sizing_report']
                 and selector['report'] == case['sizing_report'] and selector['index'] == case['index']
                 and all(row[k] == case[k] for k in ('index','row','parents','model','metadata'))
                 and row['formula'] == case['original_formula']
                 and metadata['row'] == case['row'] and metadata['parent_states'] == case['parents']
                 and row['fixed_obstruction_found'] is False and metadata['fixed_obstruction_found'] is False,
                 'Literal selected report and full actual-parent setup joins')
            need(all(normalized(metadata[k]) == normalized(v) for k,v in generated.items()),
                 'Every regenerated t6 skeleton field equals actual setup metadata')
            need(sizing['status'] == 'COMPLETE_NECESSARY_T6_CATALOGUE_AND_FORMULA_NO_EXCLUSION'
                 and sizing['complete'] is True and sizing['original_formula'] == row['formula']
                 and all(sizing[k] == row[k] for k in ('index','row','parents','model','metadata')),
                 'Exact selected complete catalogue report')
            required = tuple(sorted(e for e in base if 18 <= e[0] < 24 and 24 <= e[1] < 30))
            orientations = tuple((t,z) for z,t in required)
            need(sizing['required'] == normalized(required) and sizing['orientations'] == normalized(orientations)
                 and context['limits'] == K.LIMITS, 'All twelve oriented T-Z requirements and exact finite limits')
            cat = K.catalogue(n,base,allowed,required,orientations,K.LIMITS)
            state = SimpleNamespace(n=n,base=base,allowed=allowed,K=K,C=C,H=H,
                row=row,sizing=sizing,cat=cat,seeds=list(cat['cuts']),last_build=None)
        else:
            index = ('P0','P1','P2').index(case['host'])
            for field,name in (('catalogue_program','t5_catalogue'),('literal_tools','literal'),('cnf_program','cnf')):
                same_source(selector[field],name)
            setup = data(selector['setup_acceptance'])
            sizing_case = data(selector['sizing_case'])
            sizing_result = data(selector['sizing_result'])
            gate = data(selector['sizing_acceptance'])
            need(selector['schema'] == 'F012_FIXED_T5_REQUIRED_HEXAGON_FORMULA_V1'
                 and setup['status'] == 'ROOT_ACCEPTED_F012_THREE_T5_HOST_MODELS_AND_NECESSARY_CNFS'
                 and gate['status'] == 'ROOT_ACCEPTED_F012_THREE_T5_NECESSARY_CATALOGUE_SIZING'
                 and gate['result'] == selector['sizing_result'] and gate['host_reports'] == selector['reports']
                 and gate['helper'] == selector['catalogue_program']
                 and sizing_result['status'] == 'PASS_THREE_T5_UNIVERSAL_CATALOGUES_AND_CONTROLS'
                 and sizing_result['case'] == selector['sizing_case']
                 and len(selector['reports']) == len(setup['host_summaries'])
                     == len(sizing_case['hosts']) == len(sizing_result['hosts']) == 3
                 and selector['reports'][index] == case['sizing_report']
                 and selector['host'] == case['host']
                 and all(selector[k] == case[k] for k in ('model','metadata')),
                 'Exact acquired t5 selector and setup/sizing report joins')
            for name in ('catalogue_program','literal_tools','cnf_program','setup_acceptance'):
                need(sizing_case[name] == selector[name], 'Exact t5 declared source/premise join')
            for j,ref in enumerate(selector['reports']):
                report,actual,declared,original = (data(ref),sizing_result['hosts'][j],
                    sizing_case['hosts'][j],setup['host_summaries'][j])
                need(report['host'] == ('P0','P1','P2')[j] and actual['report'] == ref
                     and report['complete'] is True and report['counts'] == actual['counts']
                     and report['digests'] == actual['digests']
                     and all(report[k] == declared[k] == original[k] for k in ('host','model','metadata'))
                     and report['required'] == declared['required']
                     and report['orientations'] == declared['orientations'], 'Exact three-host report joins')
            row = setup['host_summaries'][index]
            need(all(sizing[k] == row[k] == case[k] for k in ('host','model','metadata'))
                 and row['formula'] == case['original_formula'] and sizing['complete'] is True
                 and sizing_result['hosts'][index]['report'] == case['sizing_report']
                 and sizing['counts'] == sizing_result['hosts'][index]['counts']
                 and sizing['digests'] == sizing_result['hosts'][index]['digests']
                 and sizing_case['catalogue_limits'] == K.LIMITS,
                 'Same actual t5 report, entire host and original CNF')
            need(all(normalized(metadata[k]) == normalized(v) for k,v in generated.items()),
                 'Every regenerated t5 skeleton field equals actual setup metadata')
            required = tuple(sorted(e for e in base if 18 <= e[0] < 23 and 23 <= e[1] < 28))
            orientations = tuple((t,z) for z,t in required)
            need(len(required) == 10 and sizing['required'] == normalized(required)
                 and sizing['orientations'] == normalized(orientations), 'All actual ten T-Z requirements')
            cat = K.catalogue(n,base,allowed,required,orientations,K.LIMITS)
            state = SimpleNamespace(n=n,base=base,allowed=allowed,K=K,C=C,H=H,
                original=case['original_formula'],cat=cat,seeds=list(cat['cuts']),last_build=None)
        need(cat['complete'] is True and cat['counts'] == sizing['counts']
             and {k:cat[k] for k in DIGESTS} == sizing['digests'],
             'Whole recomputed catalogue and all five exact digests')
        need(len(state.seeds) == cat['counts']['unique_shortcut_cuts']
             and tuple(C.witness_edges(w,n,base,allowed) for w in state.seeds) == cat['cut_edges'],
             'Every universal seed is a valid literal witness in its exact catalogue order')
        # This is the original method object from the authenticated source;
        # no predicate/loop/clause-order code is copied or replaced.
        f,variables = provider.RequiredHexagonFormula.build(state,n,base,allowed,degree=4,cuts=witnesses)
        evidence.update(catalogue=cat['counts'],digests={k:cat[k] for k in DIGESTS},
                        original_formula=case['original_formula'],universal_prefix=len(state.seeds))
    elif family == 't4_three':
        stable = data(case['selector'])
        mixed = data(case['mixed_selector'])
        same_source(stable['mixed_formula_program'],'mixed_provider')
        for field,name in (('filtered_catalogue','filtered_catalogue'),('catalogue_program','literal'),
                           ('cnf_program','cnf'),('base_formula_program','file_tools')):
            same_source(mixed[field],name)
        sizing = data(mixed['sizing_result'])
        negative = data(case['negative_sizing'])
        negative_gate = data(stable['forbidden_acceptance'])
        K = load('filtered_catalogue')
        provider = load('t4_three_provider')
        need(stable['schema'] == 'F012_FIXED_STABLE_REQUIRED_HEXAGON_FORMULA_V1'
             and stable['mixed_formula_case'] == case['mixed_selector']
             and stable['forbidden_result'] == case['negative_sizing']
             and negative_gate['result'] == case['negative_sizing']
             and negative['inputs']['positive_sizing'] == mixed['sizing_result']
             and negative['inputs']['positive_acceptance'] == mixed['sizing_acceptance']
             and negative['inputs']['catalogue'] == mixed['filtered_catalogue']
             and negative['inherited_inputs']['cuts'] == sizing['inputs']['cuts']
             and negative['saved_cuts'] == sizing['saved_cuts']
             and (n,len(base),len(allowed)) == (54,62,260) and mixed['model'] == case['model']
             and sizing['inputs']['model'] == case['model']
             and sizing['status'] == 'PASS_MIXED_REQUIRED_HEXAGON_SIZING_AND_CUT_VALIDATION',
             'Exact three-colour host and acquired positive formula context')
        seed_path = path(sizing['inputs']['cuts'])
        need(seed_path.read_bytes() == path(case['cuts']).read_bytes()
             and H.validate_cuts(seed_path,n,base,allowed,maximum_bytes=3*2**20,maximum_records=40000)
                 == sizing['saved_cuts'] and len(witnesses) == 39071,
             'Entire actual t4 seed/cut journal revalidated, no omission')
        required = tuple(sorted(e for e in base if 18 <= e[0] < 22 and 22 <= e[1] < 26))
        need(len(required) == 8 and normalized(required) == sizing['required_edges'],
             'All eight actual fixed T-Z edges require a mixed hexagon')
        cat = K.catalogue(n,base,allowed,sizing['required_edges'],sizing['work_bounds'],K.mixed_cycle)
        forbidden = K.catalogue(n,base,allowed,sizing['required_edges'],sizing['work_bounds'],
                                lambda cycle: not K.mixed_cycle(cycle))
        need(cat['counts'] == sizing['catalogue']
             and all(cat[k] == sizing[k] for k in ('cycle_catalogue_sha256','term_catalogue_sha256')),
             'Complete positive mixed-cycle catalogue')
        negative_clauses = tuple(tuple(-i for i in term) for term in forbidden['terms'])
        need(negative['status'] == 'PASS_FORBIDDEN_REQUIRED_HEXAGON_SIZING_AND_CUT_VALIDATION'
             and {k:v for k,v in forbidden['counts'].items() if not k.startswith('additional_')} == negative['catalogue']
             and all(forbidden[k] == negative[k] for k in ('cycle_catalogue_sha256','term_catalogue_sha256'))
             and H.digest_rows(negative_clauses) == negative['negative_clause_sha256']
             and len(negative_clauses) == negative['negative_clauses'] == 8160
             and sum(map(len,negative_clauses)) == negative['negative_literals'] == 31952
             and not any(not c for c in negative_clauses), 'All exact necessary forbidden-cycle clauses')
        state = SimpleNamespace(n=n,base=base,allowed=allowed,C=C,H=H,cat=cat,
            seeds=witnesses,forbidden=forbidden,negative_clauses=negative_clauses)
        f,variables = provider.RequiredHexagonFormula.build(state,n,base,allowed,degree=4,cuts=witnesses)
        evidence.update(positive_catalogue=cat['counts'],negative_catalogue=forbidden['counts'])
    else:
        need((n,len(base),len(allowed)) == (54,70,196), 'Exact two-colour t4 domain')
        f,variables = C.build(n,base,allowed,degree=4,cuts=witnesses)

    raw = f.dimacs().encode('ascii')
    if family in ('t6','t5'):
        need(metadata['variable_map'] == [[u,v,index] for (u,v),index in variables.items()],
             'Entire original primary-edge variable map')
    need(raw == path(case['formula']).read_bytes(), 'Entire reconstructed DIMACS byte equality')
    need((f.variables,len(f.clauses),len(raw)) ==
         (case['expected']['variables'],case['expected']['clauses'],case['formula']['bytes']),
         'Exact acquired formula dimensions')
    evidence.update(exact_dimacs_equal=True,variables=f.variables,clauses=len(f.clauses),
                    formula_bytes=len(raw),primary_variables=len(variables))
    return evidence


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--cases-sha256', required=True)
    parser.add_argument('--case', required=True)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--compiler', type=Path)
    action = parser.add_mutually_exclusive_group()
    action.add_argument('--describe', action='store_true')
    action.add_argument('--reconstruct', action='store_true')
    action.add_argument('--check', action='store_true')
    args = parser.parse_args()
    raw = R.regular(args.root,'data/edge_girth_regular_graphs/saved_refutation_cases.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == args.cases_sha256, 'Exact external saved-case manifest')
    program = json.loads(raw)
    need(program['schema'] == 'F012_PORTABLE_SAVED_REFUTATIONS_V1', 'Saved-refutation schema')
    rt = R.Runtime(args.root,program['runtime_manifest'],program['runtime_manifest_sha256'])
    transport = args.case == 't6_transport'
    case = program['transport'] if transport else program['cases'][args.case]
    need(len(case['inputs']) == len(set(case['inputs'])) and all(k in rt.files for k in case['inputs']),
         'Explicit unique per-case logical inputs')
    if not args.reconstruct and not args.check:
        print(json.dumps({'status':'DECLARED_SAVED_REFUTATION_NOT_EXECUTED','case':case,
                          'whole_source_credit':0},indent=2))
        return
    need(args.out is not None and not args.out.exists() and not args.out.is_symlink(), 'Fresh output')
    args.out = args.out.absolute()
    if args.check:
        need(not transport, 'Transport is a literal reconstruction mode, with no native proof checker')
        need(args.compiler is not None and args.compiler.is_absolute(), 'Explicit source-build compiler')
    rt.verify(case['inputs'])
    args.out.mkdir()
    work = args.out/'inputs'
    rt.materialize(case['inputs'],work)
    if transport:
        result = check_transports(rt,work,case,program)
        for key in case['inputs']:
            rt.resolve(key,work)
        rt.verify(case['inputs'])
        (args.out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({'status':result['status'],'whole_source_credit':0}))
        return
    result = rebuild(rt,work,case,program)
    result.update(case=args.case,solver_calls=0,proof_production_calls=0,source_credit=0,
                  historical_executable_used=False,whole_source_credit=0)
    (args.out/'cnf_checked.json').write_text(json.dumps(result,indent=2)+'\n')
    if args.check:
        binary = args.out/'fresh_rup_checker'
        plan = rt.build_plan(case['build_recipe'],work,str(args.compiler),binary.absolute())
        with (args.out/'compile.stdout').open('xb') as stdout,(args.out/'compile.stderr').open('xb') as stderr:
            compiled = subprocess.run(plan['command'],stdout=stdout,stderr=stderr,timeout=60)
        need(compiled.returncode == 0 and (args.out/'compile.stderr').stat().st_size == 0,
             'Clean fresh build of exact acquired C++ sources')
        formula = rt.resolve(case['formula']['path'],work)
        proof = rt.resolve(case['proof']['path'],work)
        start = time.monotonic()
        with (args.out/'checker.stdout').open('xb') as stdout,(args.out/'checker.stderr').open('xb') as stderr:
            returned = subprocess.run([str(binary),str(formula),str(proof)],stdout=stdout,stderr=stderr,timeout=600)
        need(returned.returncode == 0 and (args.out/'checker.stderr').stat().st_size == 0
             and (args.out/'checker.stdout').stat().st_size <= 65536, 'Clean bounded strict RUP return')
        checked = json.loads((args.out/'checker.stdout').read_text())
        need(checked['status'] == case['checker_status'] and checked['variables'] == result['variables']
             and checked['input_clauses'] == result['clauses']
             and type(checked['additions']) is int and checked['additions'] >= 1,
             'Strict acquired checker validates the empty clause on the reconstructed formula')
        result.update(status='CHECKED_PORTABLE_EXACT_DOMAIN_REFUTATION',checked=checked,
                      checker_seconds=time.monotonic()-start,fresh_binary=R.digest(binary))
    else:
        result['status'] = 'RECONSTRUCTED_PORTABLE_EXACT_CNF_PROOF_NOT_READ'
    for key in case['inputs']:
        rt.resolve(key,work)
    rt.verify(case['inputs'])
    (args.out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'case':args.case,'whole_source_credit':0}))


if __name__ == '__main__':
    main()
