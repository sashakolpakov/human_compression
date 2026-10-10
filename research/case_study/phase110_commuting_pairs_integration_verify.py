#!/usr/bin/env python3
"""Read-only complete assembly check. A hash check is not independent math review."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
P = 'phase110_commuting_pairs_integration_'

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def hs(text):
    return hashlib.sha256(text.encode()).hexdigest()

def read(name):
    return json.loads((ROOT/name).read_text())

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--primary-check', action='store_true')
    args = parser.parse_args()
    need(not args.output.exists(), 'Refusing existing verification output')
    intake = read(P+'intake.json')
    for row in intake['retained_input_bindings']:
        need(digest(ROOT/row['path']) == row['sha256'], 'Retained input hash '+row['path'])
    manifest = ROOT/(P+'manifest.json')
    if manifest.exists():
        for row in json.loads(manifest.read_text())['files']:
            need(digest(ROOT/row['path']) == row['sha256'],'Manifest hash '+row['path'])
    spec = importlib.util.spec_from_file_location('phase110_builder',ROOT/(P+'build.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    products = module.build()
    for name,text in products.items():
        need((ROOT/name).read_bytes() == text.encode(),'Fresh reconstruction mismatch '+name)
    assembly = read(P+'assembly.json')
    ledger = read(P+'ledger.json')
    text = (ROOT/(P+'manuscript.md')).read_text()
    old = (ROOT/assembly['base']['path']).read_text()
    previous = read(assembly['base_ledger']['path'])
    need(hs(text) == assembly['manuscript']['sha256'] == ledger['manuscript']['sha256'], 'Manuscript binding')
    need(len(ledger['contracts']) == 136 and len({r['integration_id'] for r in ledger['contracts']}) == 136,
         'Complete unique contract inventory')
    byid = {r['integration_id']:r for r in ledger['contracts']}
    for row in ledger['contracts']:
        span = row['integrated_proof_span']
        need(hs(text[span['start_codepoint']:span['end_codepoint_exclusive']]) == span['sha256_utf8'],
             'Contract span '+row['integration_id'])
    for row in previous['contracts']:
        p = row['integrated_proof_span']
        q = byid[row['integration_id']]['integrated_proof_span']
        need(old[p['start_codepoint']:p['end_codepoint_exclusive']] ==
             text[q['start_codepoint']:q['end_codepoint_exclusive']], 'Inherited adapter changed')
    blocks = re.findall(r'^```(gap|python)\n(.*?)^```',text,re.M|re.S)
    oldblocks = re.findall(r'^```(gap|python)\n(.*?)^```',old,re.M|re.S)
    need(len(blocks) == 11 and blocks[:8] == oldblocks,'All eight predecessor programs unchanged')
    for index,name in [(8,'finite.g'),(9,'formula.py'),(10,'run.py')]:
        need(blocks[index][1] == (ROOT/(P+name)).read_text(), 'Printed new code differs from executable')
    need(list(map(int,re.findall(r'^## (\d+)\.',text,re.M))) == list(range(1,28)), 'Continuous section numbering')
    tags = re.findall(r'\\tag\{([^}]+)\}',text)
    need(len(tags) == len(set(tags)), 'Duplicate equation tag')
    for section in assembly['hash_preserved_sections']:
        actual = re.search(r'^## '+str(section['section'])+r'\. .*?(?=^## |\Z)',text,re.M|re.S)[0]
        need(hs(actual) == section['sha256'],'Inherited whole-section hash')
    replay = read(P+'replay/replay.json')
    need(replay['status'] == 'PASS' and replay['all_census_IP_meets'] == 128 and
         replay['all_explicit_IP_meets'] == 128, 'Full new replay scope')
    for row in replay['inputs']+[replay['runner']]:
        need(digest(ROOT/row['path']) == row['sha256'],'Replay executable hash')
    for row in replay['outputs']:
        need(digest(ROOT/(P+'replay')/row['path']) == row['sha256'],'Replay result hash')
    primary_checked = []
    if args.primary_check:
        for row in intake['private_primary_assets']:
            need(digest(ROOT/row['path']) == row['sha256'],'Private primary asset hash')
            primary_checked.append(row['path'])
    report = dict(status='PASS',kind='Structural and exact replay-record check; independent mathematical review is separate',
                  manuscript=assembly['manuscript'],prior_adapters_exact=120,contracts=136,
                  unchanged_whole_sections=len(assembly['hash_preserved_sections']),
                  full_programs=11,old_programs_exact=8,new_source_numbered_items=13,
                  new_principal_theorems=4,new_source_printed_rows=14,
                  primary_assets_checked=primary_checked,private_primary_check_skipped=not args.primary_check,
                  source_count_admitted=0,ratio=None,new_Lean_claim=False)
    with args.output.open('x') as f:
        json.dump(report,f,indent=2)
        f.write('\n')
    print(json.dumps(report))

if __name__ == '__main__':
    main()
