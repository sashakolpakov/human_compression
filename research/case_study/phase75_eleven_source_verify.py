#!/usr/bin/env python3
"""Check the reviewed eleven-source assembly and optionally run Petrial controls.

Uses distributed artifacts only. Private primary-source spans are covered by
the written reviews, not checked here. This is not a proof-text checker.
"""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

BOUND = {
    'phase65_petrial_integration_manifest.json': '1636904c041cf0540ae452adbc962eb0ef914c3cab83f250a9b92bdfbe3bbc34',
    'phase70_petrial_integration_recent_audit_manifest.json': 'ba777b77ab246ee40b654c6cdce65e34b7523a3d63d6b5bb413e2578e892eed1',
    'phase45_ten_source_manuscript.md': 'f7d66e2b0b67da95e1d345fd47cd9e86c03a4309ca38ab9c8b18dd58a0f475fa',
    'phase45_ten_source_adapter_map.json': '544d8c9f80b4fa04b5c6bd1650bb0c52d54cd8a1a36194599079c3c5a5366d80',
    'phase45_ten_source_errata.json': 'b5aecfb1fbda630fa4d3c8d9cd91258c3f6c98a5f7039efe6daa5beee3d02f6a',
}
PROGRAMS = ['phase37_compress_twogroups_census.g',
            'phase40_compress_operations_check.g',
            'phase40_compress_operations_exhaustive.g',
            'phase41_chiral_cover_check.g',
            'phase65_petrial_integration_check.py']
OLD_REFERENCE = 'Recognition lemma O1.1 supplies the content needed from its quoted Theorem O2.2.'
NEW_REFERENCE = "Recognition lemma O1.1 supplies the content needed from N013's quoted Theorem 2.2."


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return sha256(data).hexdigest()


def sections(text):
    heads = list(re.finditer(r'^## (\d+)\. ', text, re.M))
    numbers = [int(h.group(1)) for h in heads]
    require(len(numbers) == len(set(numbers)), 'Duplicate numbered section')
    return {n: text[h.start():heads[i+1].start() if i+1 < len(heads)
                    else text.index('## Appendix A.', h.start())]
            for i, (n, h) in enumerate(zip(numbers, heads))}


def proof_span(text, row):
    span = row['integrated_proof_span']
    a, b = span['start_codepoint'], span['end_codepoint_exclusive']
    require(0 <= a < b <= len(text), 'Invalid proof span')
    value = text[a:b]
    require(digest(value.encode()) == span['sha256_utf8'], 'Changed proof span: ' + row['integration_id'])
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--run-petrial', action='store_true')
    parser.add_argument('--timeout', type=float, default=120)
    args = parser.parse_args()
    root, output = args.input_root.resolve(), args.output_dir.absolute()
    if os.path.lexists(output):
        parser.error('Refusing existing output directory')
    if not args.timeout > 0:
        parser.error('Timeout must be positive')
    bindings = dict(BOUND)
    for name, expected in BOUND.items():
        require(digest((root/name).read_bytes()) == expected, 'Frozen input changed: ' + name)
    for name in list(BOUND)[:2]:
        manifest = json.loads((root/name).read_text())
        for path, bound in manifest['files'].items():
            data = (root/path).read_bytes()
            require(digest(data) == bound['sha256'] and len(data) == bound['bytes'], 'Manifest mismatch: ' + path)
            if path in bindings:
                require(bindings[path] == bound['sha256'], 'Conflicting input binding')
            bindings[path] = bound['sha256']
    text = (root/'phase65_petrial_integration_manuscript.md').read_text()
    base = (root/'phase45_ten_source_manuscript.md').read_text()
    ledger = json.loads((root/'phase65_petrial_integration_ledger.json').read_text())
    old = json.loads((root/'phase45_ten_source_adapter_map.json').read_text())
    assembly = json.loads((root/'phase65_petrial_integration_assembly.json').read_text())
    require(ledger['candidate_source_ids'] == ['N001','N003','N008','L032','L035','F013','F016','L088','N013','N016','L108'], 'Intake mismatch')
    require(len(ledger['contracts']) == 87 and len(old['contracts']) == 79, 'Contract counts changed')
    current = {r['integration_id']: proof_span(text, r) for r in ledger['contracts']}
    require(len(current) == 87, 'Duplicate contract identifier')
    same, corrected = [], []
    for row in old['contracts']:
        identifier = row['integration_id']
        previous = proof_span(base, row)
        if previous == current[identifier]:
            same.append(identifier)
        else:
            require(previous.replace(OLD_REFERENCE, NEW_REFERENCE) == current[identifier], 'Unapproved old-proof change: ' + identifier)
            corrected.append(identifier)
    require(same == assembly['earlier_contract_spans_byte_unchanged'] and len(same) == 73, 'Unchanged proof list mismatch')
    require(corrected == assembly['earlier_contract_spans_only_approved_erratum_applied'] and len(corrected) == 6, 'Corrected proof list mismatch')
    old_sections, new_sections = sections(base), sections(text)
    require(list(new_sections) == list(range(1,26)), 'Numbered sections changed')
    require(len(assembly['hash_preserved_sections']) == 19, 'Preserved section count changed')
    for key, expected in assembly['hash_preserved_sections'].items():
        n = int(key)
        require(new_sections[n] == old_sections[n] and digest(new_sections[n].encode()) == expected, 'Old section changed')
    tags = re.findall(r'\\tag\{([^}]+)\}', text)
    require(len(tags) == len(set(tags)), 'Duplicate equation tag')
    require({'Kc1','Kc2','Kc3','O0','P1','P2','P3','P4'} <= set(tags), 'Missing new equation tag')
    code_blocks = re.findall(r'```(gap|python)\n(.*?)\n```', text, re.S)
    require([lang for lang, _ in code_blocks] == ['gap']*4+['python'], 'Program inventory changed')
    require(len(assembly['code_appendices']) == 5, 'Code binding inventory changed')
    codes = [(body+'\n').encode() for _, body in code_blocks]
    for code, name, bound in zip(codes, PROGRAMS, assembly['code_appendices']):
        require(code == (root/name).read_bytes(), 'Program differs from embedded source: ' + name)
        require(digest(code) == bound['sha256'] and len(code) == bound['bytes'], 'Program binding mismatch')
        bindings[name] = digest(code)
    require(NEW_REFERENCE in text and OLD_REFERENCE not in text, 'Required correction missing')
    output.mkdir(parents=True, exist_ok=False)
    report = {'date':'2026-10-10', 'status':'PASS_STRUCTURAL',
              'runner_sha256':digest(Path(__file__).read_bytes()), 'bound_inputs':bindings,
              'source_contracts_covered_by_written_review':11, 'contract_rows':87,
              'old_proof_spans_unchanged':73, 'old_proof_spans_only_approved_erratum':6,
              'whole_old_sections_unchanged':19, 'numbered_sections':25,
              'all_five_programs_byte_exact':True, 'earlier_GAP_programs_reexecuted':False,
              'primary_source_spans_checked_by_this_runner':False,
              'mathematical_proof_text_checked_by_this_runner':False,
              'petrial_controls_executed':False, 'ratio':None, 'new_Lean_build':False}
    passed = True
    if args.run_petrial:
        script = output/'petrial_check.py'
        script.write_bytes(codes[-1])
        started = time.monotonic()
        child_env = dict(os.environ)
        child_env['PYTHONOPTIMIZE'] = '0'
        try:
            result = subprocess.run([sys.executable, script.name, '--output', 'petrial_results.json'],
                                    cwd=output, env=child_env, capture_output=True, timeout=args.timeout)
            stdout, stderr, code = result.stdout, result.stderr, result.returncode
            timed_out = False
        except subprocess.TimeoutExpired as exc:
            stdout, stderr, code = exc.stdout or b'', exc.stderr or b'', None
            timed_out = True
        (output/'stdout.log').write_bytes(stdout)
        (output/'stderr.log').write_bytes(stderr)
        expected = 'fd3426fb348d4414fbcfb64af5b9432e65ad6f56f0cc05907250a4c5b02394ba'
        result_path = output/'petrial_results.json'
        actual = digest(result_path.read_bytes()) if result_path.is_file() else None
        passed = not timed_out and code == 0 and not stderr and actual == expected and script.read_bytes() == codes[-1]
        report.update(petrial_controls_executed=True, control_seconds=time.monotonic()-started,
                      exit_code=code, timed_out=timed_out, controls_sha256=actual,
                      controls_exact_match_to_independent_run=actual == expected,
                      stdout_sha256=digest(stdout), stderr_sha256=digest(stderr),
                      status='PASS_STRUCTURAL_AND_FINITE_CONTROLS' if passed else 'FAIL')
    unchanged = all(digest((root/n).read_bytes()) == h for n,h in bindings.items())
    passed = passed and unchanged
    report['all_bound_inputs_unchanged'] = unchanged
    if not passed:
        report['status'] = 'FAIL'
    (output/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if passed else 1)


if __name__ == '__main__':
    main()
