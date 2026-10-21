#!/usr/bin/env python3
"""Verify the private continuous extension and replay its exact Petrial controls.

This is an integrity/finite-control runner, not a mathematical proof checker.
Earlier GAP programs are verified unchanged, not rerun by this program.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
BASE = 'phase45_ten_source_manuscript.md'
BASE_SHA = 'f7d66e2b0b67da95e1d345fd47cd9e86c03a4309ca38ab9c8b18dd58a0f475fa'
NAME = 'phase65_petrial_integration_manuscript.md'
MANUSCRIPT_SHA = '6d302a2e7c696c916de97d2deef409c3053879999539be99a3fe72c9506205a1'
SHA = lambda b: hashlib.sha256(b).hexdigest()
PROGRAMS = ['phase37_compress_twogroups_census.g',
            'phase40_compress_operations_check.g',
            'phase40_compress_operations_exhaustive.g',
            'phase41_chiral_cover_check.g',
            'phase65_petrial_integration_check.py']


def sections(text):
    points = list(re.finditer(r'^## (\d+)\. ', text, re.M))
    result = {}
    for i, point in enumerate(points):
        end = points[i+1].start() if i+1 < len(points) else text.index('## Appendix A.', point.start())
        result[int(point.group(1))] = text[point.start():end]
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-dir', type=Path, required=True)
    ap.add_argument('--run-petrial', action='store_true')
    args = ap.parse_args()
    if os.path.lexists(args.output_dir):
        ap.error('Refusing existing output directory')
    base = (ROOT / BASE).read_text()
    text = (ROOT / NAME).read_text()
    assert SHA(base.encode()) == BASE_SHA
    assert SHA(text.encode()) == MANUSCRIPT_SHA
    ledger = json.loads((ROOT / 'phase65_petrial_integration_ledger.json').read_text())
    assembly = json.loads((ROOT / 'phase65_petrial_integration_assembly.json').read_text())
    manifest_path = ROOT / 'phase65_petrial_integration_manifest.json'
    manifest_checked = False
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        for filename, binding in manifest['files'].items():
            assert SHA((ROOT/filename).read_bytes()) == binding['sha256'], filename
        manifest_checked = True
    source_ids = ['N001','N003','N008','L032','L035','F013','F016','L088','N013','N016','L108']
    assert ledger['candidate_source_ids'] == source_ids
    assert len(ledger['contracts']) == 87
    for row in ledger['contracts']:
        span = row['integrated_proof_span']
        snippet = text[span['start_codepoint']:span['end_codepoint_exclusive']]
        assert SHA(snippet.encode()) == span['sha256_utf8'], row['integration_id']
        if row.get('paper') == 'L108':
            original = (ROOT/row['source_file']).read_text()
            span = row['source_span']
            assert SHA(original[span['start_codepoint']:span['end_codepoint_exclusive']].encode()) == span['sha256_utf8']
    old_sections, new_sections = sections(base), sections(text)
    assert list(new_sections) == list(range(1,26))
    for key, expected in assembly['hash_preserved_sections'].items():
        n = int(key)
        assert old_sections[n] == new_sections[n]
        assert SHA(new_sections[n].encode()) == expected
    tags = re.findall(r'\\tag\{([^}]+)\}', text)
    assert len(tags) == len(set(tags))
    for tag in ['Kc1','Kc2','Kc3','O0','P1','P2','P3','P4']:
        assert tag in tags
    codes = []
    for lang in ['gap','python']:
        codes.extend((b+'\n').encode() for b in re.findall('```'+lang+r'\n(.*?)\n```',text,re.S))
    assert len(codes) == 5
    for code, filename, row in zip(codes, PROGRAMS, assembly['code_appendices']):
        assert code == (ROOT/filename).read_bytes(), filename
        assert SHA(code) == row['sha256'] and len(code) == row['bytes']
    assert 'L108 remains excluded' not in text
    assert "Recognition lemma O1.1 supplies the content needed from N013's quoted Theorem 2.2." in text
    assert 'Theorem O2.2.' not in text
    args.output_dir.mkdir(parents=False)
    report = {'status':'structural_pass','mathematical_proof_check':False,
              'manuscript_sha256':MANUSCRIPT_SHA,'manifest_checked':manifest_checked,
              'source_count_admitted':False,'ratio':None,'contract_rows':87,
              'hash_preserved_sections':list(assembly['hash_preserved_sections']),
              'old_contract_spans_byte_unchanged':len(assembly['earlier_contract_spans_byte_unchanged']),
              'old_contract_spans_only_approved_erratum':len(assembly['earlier_contract_spans_only_approved_erratum_applied']),
              'all_five_complete_programs_byte_exact':True,
              'earlier_GAP_programs_reexecuted':False,'petrial_controls_executed':False}
    if args.run_petrial:
        script=args.output_dir/'petrial_check.py'
        script.write_bytes(codes[-1])
        output=(args.output_dir/'petrial_results.json').resolve()
        result=subprocess.run([sys.executable,str(script.resolve()),'--output',str(output)],capture_output=True,text=True)
        (args.output_dir/'petrial.stdout.txt').write_text(result.stdout)
        (args.output_dir/'petrial.stderr.txt').write_text(result.stderr)
        assert result.returncode == 0 and output.is_file(), result.stderr
        controls=json.loads(output.read_text())
        assert controls['checker_sha256']==SHA(codes[-1])
        assert controls['summary']=={'examples':7,'nonfaithful_petrial_actions':2,'original_chambers':188,'thin_petrials':4}
        for case in controls['cases']:
            assert case['action_kernel_order']==case['computed_core_order']==(2 if case['face_marker_central'] else 1)
        report.update(status='structural_and_exact_Petrial_controls_pass',petrial_controls_executed=True,
                      petrial_summary=controls['summary'],petrial_result_sha256=SHA(output.read_bytes()))
    with (args.output_dir/'report.json').open('x') as stream:
        json.dump(report,stream,indent=2);stream.write('\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
