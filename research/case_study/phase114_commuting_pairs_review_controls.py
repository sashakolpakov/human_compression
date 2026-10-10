#!/usr/bin/env python3
"""Independent semantic span and refusal controls; frozen inputs are read-only."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

P = 'phase110_commuting_pairs_integration_'
R = 'phase114_commuting_pairs_review_'


def require(ok, why):
    if not ok:
        raise RuntimeError(why)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    require(not args.output_dir.exists(), 'Refusing existing controls directory')
    checker = Path(__file__).with_name(R+'check.py')
    spec = importlib.util.spec_from_file_location('independent_review114', checker)
    review = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(review)
    base = args.base.resolve()
    text = (base/(P+'manuscript.md')).read_text()
    oldtext = (base/'phase78_n009_integration_manuscript.md').read_text()
    ledger = json.loads((base/review.CORRECTED_LEDGER).read_text())
    oldledger = json.loads((base/'phase78_n009_integration_ledger.json').read_text())
    review.audit_contract(text, oldtext, ledger, oldledger)
    args.output_dir.mkdir(parents=True)
    cases = []

    def reject(label, changed):
        try:
            review.audit_contract(text, oldtext, changed, oldledger)
        except RuntimeError as exc:
            cases.append(dict(name=label, rejected=True, reason=str(exc)))
        else:
            raise RuntimeError('Accepted semantic mutation: '+label)

    reject('original_hash_consistent_ledger', json.loads((base/(P+'ledger.json')).read_text()))
    for name, item, mode in [('one_character_hash_consistent_span', 7, 'empty'),
                             ('missing_final_subsection_hash_consistent_span', 0, 'truncate'),
                             ('wrong_full_subsection_hash_consistent_span', 7, 'redirect')]:
        changed = copy.deepcopy(ledger)
        row = changed['contracts'][120+item]
        span = row['integrated_proof_span']
        bounds = review.section_boundaries(text)
        if mode == 'empty':
            span['end_codepoint_exclusive'] = span['start_codepoint']+1
        elif mode == 'truncate':
            span['end_codepoint_exclusive'] = bounds['25.3'][0]
        else:
            span['start_codepoint'], span['end_codepoint_exclusive'] = bounds['25.1']
        span['sha256_utf8'] = sha(text[span['start_codepoint']:span['end_codepoint_exclusive']].encode())
        reject(name, changed)
    changed = copy.deepcopy(ledger)
    changed['contracts'][0]['review_control_injected_claim'] = 'Changed mathematical contract'
    reject('retained_contract_changed_without_changing_span', changed)
    changed = copy.deepcopy(ledger)
    changed['contracts'][127]['principal'] = False
    reject('principal_theorem_demotion', changed)
    code_text = text.replace('# Full finite exceptional census.', '# Altered finite exceptional census.', 1)
    require(code_text != text, 'Executable mutation did not change text')
    try:
        review.audit_continuity(base, code_text, oldtext)
    except RuntimeError as exc:
        cases.append(dict(name='printed_executable_diverges', rejected=True, reason=str(exc)))
    else:
        raise RuntimeError('Accepted altered executable appendix')
    occupied = args.output_dir/'occupied'
    occupied.mkdir()
    sentinel = occupied/'sentinel'
    sentinel.write_bytes(b'REVIEW114 DO NOT OVERWRITE\n')
    before = sha(sentinel.read_bytes())
    result = subprocess.run([sys.executable, '-B', '-O', str(checker), '--base', str(base),
                             '--output-dir', str(occupied)], capture_output=True, text=True)
    require(result.returncode != 0 and 'Refusing existing output directory' in result.stderr,
            'Review checker failed occupied-output refusal')
    require(sha(sentinel.read_bytes()) == before and list(occupied.iterdir()) == [sentinel],
            'Occupied output changed')
    cases.append(dict(name='occupied_output', rejected=True, returncode=result.returncode,
                      sentinel_sha256=before))
    report = dict(status='PASS',semantic_rejections=7,occupied_output_refusals=1,cases=cases,
                  scope='Semantic tests recompute mutated span hashes; rejection is not merely a manifest-hash mismatch')
    (args.output_dir/'controls.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',semantic_rejections=7,occupied_output_refusals=1)))


if __name__ == '__main__':
    main()
