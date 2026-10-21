#!/usr/bin/env python3
"""Independent binding/scope audit; mathematical review is recorded separately."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PIN = '4bf824fbe8413e48bd3d96a6453466205cadd65a0db06eb843fb392fa7e37200'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def need(condition, message):
    if not condition:
        raise RuntimeError('L068_REVIEW_REJECT: ' + message)

def binding(root, row, key='path'):
    p = Path(row[key])
    need(not p.is_absolute() and '..' not in p.parts, 'unsafe path')
    f = root / p
    need(f.stat().st_size == row['bytes'] and sha(f) == row['sha256'], str(p))

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for name in ['author', 'public-root', 'out']:
        ap.add_argument('--' + name, type=Path, required=True)
    a = ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(), 'fresh output')
    a.out.mkdir(parents=True)
    need(sha(a.author / 'manifest.json') == PIN, 'author edition')
    manifest = json.loads((a.author / 'manifest.json').read_text())
    for row in manifest['exports']:
        binding(a.author, row)
    ledger = json.loads((a.author / 'source_clause_map.json').read_text())
    need(len(ledger['rows']) == 17 and len(ledger['new_spans']) == 9, 'complete scope')
    for row in ledger['new_spans'].values():
        b = b''.join((a.author / row['path']).read_bytes().splitlines(keepends=True)
                     [row['start_line'] - 1:row['end_line']])
        need(len(b) == row['bytes'] and hashlib.sha256(b).hexdigest() == row['sha256'], 'span')
    need(not ledger['literal_Q_recovered'] and ledger['literal_P_recovered'] and
         ledger['corrected_Q_recovered'], 'literal/corrected distinction')
    need(all(not row['open_conjecture_solution'] for row in ledger['rows']), 'question scope')
    deps = json.loads((a.author / 'dependency_map.json').read_text())
    for row in deps['common_papers'][0]['bindings']:
        binding(a.author, row)
        binding(a.public_root, row, 'public_path')
    binding(a.public_root, deps['common_papers'][0]['prior_public_admission'])
    need(len(deps['required_programs']) == 2 and not deps['archived_manuscript_proof_premises'],
         'complete current dependency boundary')
    for row in deps['required_programs']:
        binding(a.author, row)
        need(not row['pruned'], 'whole program')
    review = json.loads((ROOT / 'review.json').read_text())
    replay = json.loads((ROOT / 'fresh_author_replay.json').read_text())
    need(review['author_manifest_sha256'] == PIN and
         review['status'] == 'ACCEPT_COMPLETE_CORRECTED_PRINCIPAL_CONTRACT', 'review edition')
    need(replay['status'] == 'PASS' and len(replay['incidence_rows']) == 12 and
         len(replay['Lean_axioms']) == 3 and len(replay['controls']) == 3 and
         all(c['rejected'] for c in replay['controls']), 'fresh full evidence')
    need([p['pages'] for p in replay['render']['papers'].values()] == [2, 6, 8] and
         all(p['old_page_text_equal'] for p in replay['render']['papers'].values()), 'complete PDFs')
    report = {'status': 'PASS', 'author_exports': len(manifest['exports']),
              'source_clauses': 17, 'proof_spans': 9, 'whole_required_programs': 2,
              'literal_Q_recovered': False, 'corrected_Q_recovered': True,
              'literal_P_recovered': True, 'new_question_credit': 0,
              'new_formal_credit': 0, 'whole_source_formalized': False,
              'compression_factor': None,
              'scope': 'Binding audit and adoption of recorded written review; no independent reimplementation of GAP.'}
    (a.out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))

if __name__ == '__main__':
    main()
