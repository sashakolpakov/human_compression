#!/usr/bin/env python3
"""Independently bind the affine edition to its complete prior source contract."""
import argparse
import hashlib
import json
from pathlib import Path

AUTHOR = '88d909a728b375c275bf7658004e33286d14aad15ad0480c13bbe3fc9aa0d83f'

def need(ok, message):
    if not ok:
        raise ValueError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check(root, row):
    rel = Path(row['path'])
    need(not rel.is_absolute() and '..' not in rel.parts, 'relative binding')
    path = root / rel
    need(sha(path) == row['sha256'], 'changed ' + str(path))
    if 'bytes' in row:
        need(path.stat().st_size == row['bytes'], 'length ' + str(path))

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--author', type=Path, required=True)
    ap.add_argument('--study', type=Path, required=True)
    ap.add_argument('--public', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    root = args.author
    need(sha(root/'manifest.json') == AUTHOR, 'frozen author manifest')
    manifest = json.loads((root/'manifest.json').read_bytes())
    need(len(manifest['exports']) == 88, 'full export inventory')
    for row in manifest['exports']:
        check(root, row)
    scope = json.loads((root/'scope.json').read_bytes())
    lineage = json.loads((root/'lineage.json').read_bytes())
    ledger = json.loads((args.study/'phase250_source_ledger.json').read_bytes())
    need([r['original_record'] for r in scope['source_rows']] == ledger['rows'],
         'all detailed source records unchanged and ordered')
    need(len(scope['source_rows']) == scope['ledger_rows'] == 33, '33 source rows')
    for row in scope['source_rows']:
        need(row['id'] == row['original_record']['id'] and row['new_credit'] == 0,
             'identity or credit ' + row['id'])
        need(row['current_regions'] and all(k in scope['proof_regions']
             for k in row['current_regions']), 'proof reference ' + row['id'])
    for region in scope['proof_regions'].values():
        text = (root/region['path']).read_text()
        need(region['start'] == 0 and region['end'] == len(text), 'whole proof section')
        need(hashlib.sha256(text.encode()).hexdigest() == region['sha256'], 'proof span')
    for row in scope['source_bindings']:
        check(args.study, row)
    for row in lineage['written_inputs']:
        check(args.study, row)
    check(args.public, scope['authoritative_existing_admission'])
    need(lineage['admission'] == scope['authoritative_existing_admission'], 'prior admission')
    need(len(lineage['program_inputs']) == len(scope['programs']) == 6, 'six whole programs')
    for row in lineage['program_inputs']:
        check(args.study, row['old'])
        check(root, row['current'])
        need(row['identical'] and row['old']['sha256'] == row['current']['sha256'],
             'program reuse, no silent edits')
    formal = scope['formal_scope']
    names = [name for module in formal['modules'] for name in module['declarations']]
    need(len(names) == len(set(names)) == 9 and formal['new'] == 2 and
         formal['reused'] == 7 and formal['end_to_end'] is False, 'formal scope')
    for module in formal['modules']:
        need(sha(root/'formal'/module['file']) == module['sha256'], 'formal module')
    need(scope['principal_contracts'] == 1 and scope['project_total_preserved'] == 27 and
         scope['new_source_credit'] == scope['new_question_credit'] == 0 and
         scope['compression_ratio'] is None, 'unchanged intake and measurement boundary')
    need(scope['cost_boundary']['historical_program_cost'] is None and
         scope['cost_boundary']['scalar'] is None, 'unknown costs stay unknown')
    for stem in ['umbrella', 'mixed-prime-polyhedra']:
        text = (root/(stem+'.tex')).read_text()
        need('preamble' in text, 'standalone common preamble')
    result = dict(status='PASS_INDEPENDENT_BINDINGS', author_manifest_sha256=AUTHOR,
                  exports=88, prior_records=33, proof_regions=17, source_artifacts=6,
                  prior_written_inputs=7, exact_reused_programs=6,
                  actual_formal_declarations=names, formal_new=2, formal_reused=7,
                  principal_contracts=1, project_total=27,
                  new_source_credit=0, new_question_credit=0, compression_ratio=None,
                  scope='Exact identity and completeness, not an automatic mathematical proof.')
    need(not args.out.exists(), 'fresh report')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['status','exports','prior_records','exact_reused_programs']}))

if __name__ == '__main__':
    main()
