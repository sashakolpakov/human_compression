#!/usr/bin/env python3
"""Correct the frozen phase110 proof-span ledger without changing its manuscript.

This is structural verification, not a substitute for mathematical review.
All heading positions refer to the complete Unicode manuscript.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
P = 'phase110_commuting_pairs_integration_'
MANIFEST_SHA = 'ed62d34e741342ee2da07485a76bea4e3b172fb373a2cb5ad1319fad3cd54c9c'
CORRECTED = 'phase116_commuting_pairs_corrected_ledger.json'
# First/last complete subsection, followed by required mathematical text.
TARGETS = [
    (2, 3, ('\\tag{CPI7}', '\\tag{CPI12}', 'five under Aut(S₆)')),
    (2, 3, ('\\tag{CPI9}', '\\tag{CPI12}', 'one under Aut(A₆)')),
    (1, 1, ('\\tag{CPI2}', 'centralizer structure')),
    (2, 2, ('\\tag{CPI5}', 'source Lemma 3.2')),
    (2, 2, ('printed inference', 'reversal fixes the ordered class')),
    (2, 4, ('printed inference', 'a middle generator must also be preserved')),
    (3, 3, ('all 64 ordered pairs of subsets', 'string C-group')),
    (3, 3, ('\\tag{CPI11}', 'computational proof of the exceptional classification')),
    (4, 4, ('Remark 3.7 is historical attribution', 'Leemans–Vauthier')),
    (1, 1, ('kernel has index two', 'source Propositions 3.1 and 4.1')),
    (2, 2, ('\\tag{CPI9}', 'source Lemma 4.2')),
    (3, 3, ('unique Aut(A₆) orbit', 'source Lemma 4.3')),
    (3, 4, ('no A₆ regular polyhedron', 'regular-polyhedron context')),
    (4, 4, ('fourteen printed rows', '|50|6774|1795|')),
    (3, 3, ('\\tag{CPI12}', 'Only the second and fourth endpoint orbits')),
    (2, 2, ('even/odd degree pairing', 'N=6 and N=7 differ')),
]


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()


def original_inputs():
    raw = (ROOT / (P + 'manifest.json')).read_bytes()
    need(sha(raw) == MANIFEST_SHA, 'Frozen original manifest mismatch')
    manifest = json.loads(raw)
    for row in manifest['files']:
        data = (ROOT / row['path']).read_bytes()
        need(len(data) == row['bytes'] and sha(data) == row['sha256'],
             'Frozen original binding mismatch: ' + row['path'])
    intake = json.loads((ROOT / (P + 'intake.json')).read_text())
    for row in intake['retained_input_bindings']:
        need(sha((ROOT / row['path']).read_bytes()) == row['sha256'],
             'Retained binding mismatch: ' + row['path'])
    spec = importlib.util.spec_from_file_location('frozen_phase110_builder', ROOT / (P + 'build.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for name, text in module.build().items():
        need((ROOT / name).read_bytes() == text.encode(), 'Original reconstruction differs: ' + name)
    return (ROOT / (P + 'manuscript.md')).read_text(), json.loads((ROOT / (P + 'ledger.json')).read_text())


def corrected(text, original):
    # Scan the whole file: never start a search inside a heading's hash prefix.
    headings = list(re.finditer(r'^#{1,3} [^\n]*(?:\n|$)', text, re.M))
    sections = {}
    for i in range(1, 5):
        selected = [h for h in headings if h.group().startswith(f'### 25.{i}. ')]
        need(len(selected) == 1, 'Nonunique complete subsection heading')
        h = selected[0]
        later = [n.start() for n in headings if n.start() > h.start()]
        need(later, 'Missing following heading')
        sections[i] = (h.start(), min(later))
    result = copy.deepcopy(original)
    changed = []
    for row in result['contracts']:
        if row['paper'] != 'L066':
            continue
        number = int(row['integration_id'].split('.')[1])
        first, last, phrases = TARGETS[number - 1]
        start, end = sections[first][0], sections[last][1]
        chunk = text[start:end]
        need(end - start > 1000, 'Empty or truncated proof span')
        for phrase in phrases:
            need(phrase in chunk, 'Required proof text absent: ' + row['integration_id'] + ': ' + phrase)
        row['integrated_proof_span'] = dict(start_codepoint=start,
            end_codepoint_exclusive=end, sha256_utf8=sha(chunk.encode()))
        changed.append(row['integration_id'])
    need(len(changed) == 16 and len(set(changed)) == 16, 'Complete sixteen-row correction')
    need([r for r in result['contracts'] if r['paper'] != 'L066'] ==
         [r for r in original['contracts'] if r['paper'] != 'L066'], 'Inherited row changed')
    result['schema'] = 'thirteen_source_commuting_pair_extension_contract_v2_corrected_spans'
    result['proof_span_correction'] = dict(
        original_ledger=P + 'ledger.json',
        original_ledger_sha256=sha((ROOT / (P + 'ledger.json')).read_bytes()),
        original_manifest_sha256=MANIFEST_SHA,
        corrected_rows=changed, manuscript_changed=False,
        reason='Global heading boundaries replace a search that began inside the final heading prefix.',
        status='Root-authored correction; independent phase114 review required')
    return result, sections


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    modes = ap.add_mutually_exclusive_group(required=True)
    modes.add_argument('--build-dir', type=Path)
    modes.add_argument('--output', type=Path)
    ap.add_argument('--expected-ledger', type=Path, default=ROOT / CORRECTED)
    args = ap.parse_args()
    target = args.build_dir or args.output
    need(not os.path.lexists(target), 'Fresh output required')
    text, original = original_inputs()
    ledger, sections = corrected(text, original)
    raw = encode(ledger)
    if args.build_dir:
        args.build_dir.mkdir(parents=True, exist_ok=False)
        with (args.build_dir / CORRECTED).open('xb') as stream:
            stream.write(raw)
        print(json.dumps(dict(status='BUILT', corrected_ledger_sha256=sha(raw))))
    else:
        need(args.expected_ledger.read_bytes() == raw, 'Corrected proof ledger mismatch')
        report = dict(status='PASS', kind='Complete proof-span structural correction; mathematical review remains separate',
            original_manifest_sha256=MANIFEST_SHA, manuscript_sha256=sha(text.encode()),
            corrected_ledger_sha256=sha(raw), program_sha256=sha(Path(__file__).read_bytes()),
            complete_subsection_intervals=sections, corrected_L066_rows=16,
            inherited_120_rows_identical=True, original_manuscript_unchanged=True,
            complete_programs=11, source_admission=False, new_Lean_claim=False, ratio=None,
            private_primary_assets_required=False)
        with args.output.open('xb') as stream:
            stream.write(encode(report))
        print(json.dumps(report))


if __name__ == '__main__':
    main()
