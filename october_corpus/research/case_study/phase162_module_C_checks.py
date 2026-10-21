#!/usr/bin/env python3
"""Independent frozen Module C binding/span/log/portable checks, not a new census.

Uses exported files only unless --primary-check is requested. The exact outer
manifest is pinned. New output directory required; no original is altered.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

MANIFEST = 'phase150_module_C_manifest.json'
MANIFEST_SHA = '790b07f4607ba00f21690984e84231463b6b6a3d27a2445cd0033ca097cc4181'


def require(test, message):
    if not test:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(path.read_text())


def audit(root, primary=False):
    require(digest((root / MANIFEST).read_bytes()) == MANIFEST_SHA, 'Frozen outer manifest changed')
    manifest = load(root / MANIFEST)
    records = manifest['files'] + manifest['required_shared_inputs']
    if primary:
        records += manifest['private_primary_bindings']
    require(len({r['path'] for r in records}) == len(records), 'Duplicate binding')
    for row in records:
        p = Path(row['path'])
        require(not p.is_absolute() and '..' not in p.parts, 'Unsafe bound path')
        data = (root / p).read_bytes()
        require(len(data) == row['bytes'] and digest(data) == row['sha256'], 'Changed binding: ' + str(p))
    require(set(manifest['export_allowlist']) == {r['path'] for r in manifest['files']} | {MANIFEST}, 'Wrong export closure')
    ledger = load(root / 'phase150_module_C_ledger.json')
    body = (root / ledger['manuscript']['path']).read_text()
    legs = ledger['proof_legs']
    require(len(legs) == 29, 'Wrong proof node count')
    scope = ledger['scope_records']
    expected = {'J'+str(i) for i in range(1, 12)} | {'N'+str(i) for i in range(1, 17)} | {'P'+str(i) for i in range(1, 9)}
    require(len(scope) == 35 and {r['id'] for r in scope} == expected, 'Wrong source-contract closure')
    for name, node in legs.items():
        binding = node['binding']
        piece = body[binding['start_char']:binding['end_char']].encode()
        require(len(piece) == binding['bytes'] and digest(piece) == binding['sha256'], 'Wrong full proof span: ' + name)
    complete = set(legs) | set(ledger['exact_U_interfaces']) | {'certificate.construction', 'certificate.exhaustive'}
    seen, active = set(), set()

    def visit(name):
        require(name in complete, 'Unknown proof dependency: ' + name)
        if name not in legs or name in seen:
            return
        require(name not in active, 'Circular proof dependency')
        active.add(name)
        for dep in legs[name]['dependencies']:
            visit(dep)
        active.remove(name)
        seen.add(name)

    for name in legs:
        visit(name)
    for row in scope:
        require(row['complete_proof_ids'], 'Empty source-contract attachment')
        require(set(row['complete_proof_ids']) == set(row['final_new_proof_spans']), 'Wrong attached span set')
        for name in row['complete_proof_ids']:
            require(row['final_new_proof_spans'][name] == legs[name]['binding'], 'Detached source-contract span')
        if row['id'] in {'P'+str(i) for i in range(1, 7)}:
            require('adapter' not in row and 'proof_sections' not in row, 'Unqualified historical Petrial locator')
    require('excludes digonal rank-two sections' in body, 'Missing lattice/digon clarification')
    costs = load(root / 'phase150_module_C_costs.json')
    def subtotal(rows):
        for row in rows:
            data = (root / row['path']).read_bytes()
            require(len(data) == row['bytes'] and digest(data) == row['sha256'], 'Wrong cost binding')
        return sum(row['bytes'] for row in rows)
    program_bytes = subtotal(costs['required_programs'])
    require(program_bytes == 15578 == costs['required_program_bytes'], 'Wrong required program cost')
    core = costs['manuscript']['bytes'] + costs['umbrella']['bytes'] + program_bytes
    support = subtotal(costs['support_infrastructure'])
    require(core == 146126 == costs['U_plus_C_plus_programs_bytes'], 'Wrong complete core cost')
    require(support == 294854 == costs['support_infrastructure_bytes'], 'Wrong support cost')
    require(core + support == costs['charged_core_plus_support_bytes'] == 440980, 'Wrong combined cost')
    require(costs['ratio'] is None and not costs['full_source_Lean'], 'Unsupported cost/formal claim')
    replay = load(root / 'phase44_operations_recent_audit_replay.json')
    construction = (root / 'phase44_operations_recent_audit_construction.log').read_text()
    census = (root / 'phase44_operations_recent_audit_census.log').read_text()
    for execution, logname in zip(replay['runs'], ['phase44_operations_recent_audit_construction.log', 'phase44_operations_recent_audit_census.log']):
        require(digest((root/logname).read_bytes()) == execution['log_sha256'], 'Wrong historical execution log')
        require(digest((root / execution['script']).read_bytes()) == execution['sha256'], 'Different executed program')
    g = re.findall(r'^GEOMETRY (\d+) PAIRS (\[[^\n]+?\]) PARABOLICS (\[[^\n]+?\]) TYPES .* IP_MEETS (\d+) HELLY_ROWS (\d+) PASS$', construction, re.M)
    require([int(x[0]) for x in g] == list(range(1, 7)), 'Wrong construction list')
    pair_orders = [[5,2,2,3,2,5],[5,2,2,6,2,5],[5,2,2,3,3,5],[5,3,2,3,2,5],[5,3,3,3,3,5],[5,6,2,6,2,5]]
    par_orders = [[120,20,20,60],[120,20,20,660],[120,20,60,60],[120,120,20,60],[120,120,60,60],[120,120,20,660]]
    require([json.loads(x[1]) for x in g] == pair_orders, 'Wrong pair-order table')
    require([json.loads(x[2]) for x in g] == par_orders, 'Wrong parabolic table')
    require(all(int(x[3]) == 256 and int(x[4]) == 16 for x in g), 'Incomplete recorded geometry checks')
    negatives = re.findall(r'^NEGATIVE (\d+) IP_FAILURES (\d+) PANELS (\[[^\n]+\]) PASS$', construction, re.M)
    require([(int(a),int(b),json.loads(c)) for a,b,c in negatives] == [(1,8,[2,4,2,2]),(2,8,[2,2,2,4])], 'Wrong counterexamples')
    stages = [list(map(int,x)) for x in re.findall(r'^STAGE_TOTAL (\d+) TESTED (\d+) ACCEPTED (\d+)$', census, re.M)]
    require(stages == [[4,100016,40],[5,21352,0]] == replay['census']['stage_totals'], 'Wrong complete census stages')
    require('RANK4_CLASSES 6 RANK5_CLASSES 0' in census and census.rstrip().endswith('COMPRESS_C_EXHAUSTIVE_PASS'), 'Incomplete census log')
    require(digest((root/'phase40_compress_operations_exhaustive_classes.json').read_bytes()) == replay['census']['classes_sha256'], 'Wrong class certificate')
    return {'status':'PASS_BINDINGS_SPANS_AND_RECORDED_EVIDENCE', 'manifest_sha256':MANIFEST_SHA,
            'checked_bindings':records, 'private_primary_check':primary, 'source_contracts':35,
            'proof_nodes':29, 'dependency_graph_acyclic':True, 'required_program_bytes':program_bytes,
            'core_bytes':core, 'support_bytes':support, 'recorded_census_stages':stages,
            'recorded_construction_meets':1536, 'recorded_Helly_rows':96,
            'fresh_GAP_census':False, 'fresh_Lean_compile':False,
            'mathematical_proof_review':'Separate human-style review, not established by this script.'}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--inputs',type=Path,default=Path(__file__).resolve().parent)
    ap.add_argument('--output-dir',type=Path,required=True)
    ap.add_argument('--primary-check',action='store_true')
    args=ap.parse_args()
    require(not os.path.lexists(args.output_dir), 'Refusing existing output path')
    report=audit(args.inputs,args.primary_check)
    args.output_dir.mkdir(parents=True)
    public=args.output_dir/'portable'/'research'/'case_study'
    m=load(args.inputs/MANIFEST)
    for row in m['files']+m['required_shared_inputs']:
        dest=public/row['path'];dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(args.inputs/row['path'],dest)
    shutil.copyfile(args.inputs/MANIFEST,public/MANIFEST)
    require(not (public/'sources').exists(), 'Primary files copied')
    portable=audit(public)
    call=[sys.executable,'-B','-O',str(public/'phase150_module_C_verify.py'),'--output',str(args.output_dir/'portable.json')]
    run=subprocess.run(call,capture_output=True,text=True,timeout=30)
    require(run.returncode==0 and 'MODULE_C_STRUCTURAL_BINDINGS_PASS' in run.stdout, 'Portable author verifier failed')
    own_cases=[]
    for name in [MANIFEST,'phase150_module_C_manuscript.md','phase138_umbrella_v3.md',
                 'phase40_compress_operations_check.g','phase40_compress_operations_exhaustive.g',
                 'phase44_operations_recent_audit_replay.json','phase44_operations_recent_audit_census.log',
                 'phase40_compress_operations_exhaustive_classes.json']:
        p=public/name;before=p.read_bytes();p.write_bytes(before+b'\n')
        try:
            audit(public)
        except RuntimeError as exc:
            own_cases.append({'mutated':name,'rejected':True,'message':str(exc)})
        else:
            raise RuntimeError('Mutation was accepted: '+name)
        finally:
            p.write_bytes(before)
    require(audit(public)==portable, 'Portable inputs not restored')
    report.update(portable_pass=True,private_sources_copied=False,own_mutation_cases=own_cases,
                  author_public_stdout=run.stdout,author_public_stderr=run.stderr,
                  portable_tree=str(public),checker_sha256=digest(Path(__file__).read_bytes()))
    (args.output_dir/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PHASE162_PASS',len(report['checked_bindings']),'bindings;',len(own_cases),'independent mutations')


if __name__=='__main__':
    main()
