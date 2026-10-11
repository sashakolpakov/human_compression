#!/usr/bin/env python3
"""Bind both reviewed F005 editions and replay independently constructed models.

Source reading and mathematical review are recorded in review.json. This
program checks their exact inputs; it does not replace those reviews.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MAIN = '794ae902e7e06a7eacc7af6da5ed853a39182b8e94efb4695de253902b8c454a'
EXCEPTIONAL = '488d97e76d1bc640886f16bf83e65668657aa51a31ff61ce3c5c143ae8e06690'
SOURCE = '5ab33b1c08dc33cb6543d85c84db7a2d37016381fb0a47aad85d6d8321dfc63f'


def need(value, message):
    if not value:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')


def exports(directory, expected):
    manifest = directory / 'manifest.json'
    need(sha(manifest) == expected, 'changed reviewed edition')
    rows = read(manifest)['exports']
    need(len({r['path'] for r in rows}) == len(rows), 'duplicate exports')
    for row in rows:
        relative = Path(row['path'])
        need(not relative.is_absolute() and '..' not in relative.parts, 'unsafe export')
        path = directory / relative
        need(path.stat().st_size == row['bytes'] and sha(path) == row['sha256'],
             'changed complete export: ' + row['path'])
    return len(rows)


def contexts(directory):
    scope = read(directory / 'scope.json')
    for row in scope['proof_contexts']:
        passage = (directory / row['path']).read_text()[row['start']:row['end']]
        need(hashlib.sha256(passage.encode()).hexdigest() == row['sha256'],
             'changed written proof context: ' + row['id'])
    return scope


def command(args, log, success=True):
    result = subprocess.run(list(map(str, args)), capture_output=True, text=True, timeout=180)
    output = result.stdout + result.stderr
    log.write_text(output)
    if success:
        need(result.returncode == 0, 'failed replay: ' + log.name)
    else:
        need(result.returncode != 0 and 'ValueError:' in output and 'SyntaxError' not in output,
             'corruption accepted or failed for an unrelated reason: ' + log.name)
    return result


def models(out, gap):
    for name, script in [('coordinates', 'check_coordinates.py'),
                         ('exceptional', 'check_exceptional.py')]:
        command([sys.executable, '-B', '-O', ROOT / script, '--out', out / (name + '.json')],
                out / (name + '.log'))
    coordinate = read(out / 'coordinates.json')
    exceptional = read(out / 'exceptional.json')
    need(coordinate['status'] == 'PASS_DISTINCT_SIX_COORDINATE_RECONSTRUCTION'
         and coordinate['input_IP_identities'] == 552960
         and coordinate['mixed_end_IP_identities'] == 138240
         and coordinate['actual_automorphism_lifts'] == 360
         and coordinate['good_intersection'] == 18
         and coordinate['bad_intersection'] == 54
         and coordinate['marked_middle'] == 18
         and coordinate['both_actual_witness_words'], 'incomplete coordinate validation')
    need(exceptional['status'] == 'PASS_DISTINCT_EXCEPTIONAL_AFFINE_MODEL'
         and exceptional['input_IP_identities'] == 36864
         and exceptional['mix_IP_identities'] == 663552
         and exceptional['actual_mix_automorphisms'] == 2592
         and exceptional['all_six_embedded_fibers']
         and exceptional['Cor610_literal_failure']
         and exceptional['Cor615_2_reversed_arguments_literal_failure'],
         'incomplete exceptional validation')
    result = command([gap, '-q', '-b', '--quitonbreak', ROOT / 'check_coprime.g'],
                     out / 'coprime.log')
    need(not result.stderr and ''.join(result.stdout.split()) ==
         'PASSindependentfixed16pointinputs_IP_pairs=512mixed_end_intersection=60middle=30actual_witness=(1,3)(2,4)(5,7)(6,9)',
         'incomplete required finite input reconstruction')
    changes = [
        ('middle_vector', 'check_coordinates.py', 'v=(1,1,2,2,1,2);', 'v=(1,1,2,2,1,1);'),
        ('voltage', 'check_coordinates.py', 'u=[Z,(2,2,0,1,0,1),Z,Z]', 'u=[Z,(2,2,0,1,0,0),Z,Z]'),
        ('good_root', 'check_coordinates.py', 'gstar=mul(mul(s[1],s[2]),s[3]);',
         'gstar=mul(mul(s[0],s[2]),s[3]);'),
        ('affine_center', 'check_exceptional.py', 'b=affine(lambda x,y:(x,1-y));',
         'b=affine(lambda x,y:(x,-y));'),
        ('identify_fibers', 'check_exceptional.py', 'C1={one,affine(lambda x,y:(-x,1-y))}', 'C1=Ty'),
        ('wrong_literal_word', 'check_exceptional.py', 'for i in [1,2,1,2]:q=medges[q][i]',
         'for i in [1,2,1,1]:q=medges[q][i]')]
    for name, source, old, new in changes:
        text = (ROOT / source).read_text()
        need(text.count(old) == 1, 'nonunique semantic control')
        copy = out / (name + '.py')
        copy.write_text(text.replace(old, new))
        command([sys.executable, '-B', '-O', copy, '--out', out / (name + '.json')],
                out / (name + '.log'), success=False)
    return [name for name, _, _, _ in changes]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--main', type=Path, required=True)
    parser.add_argument('--exceptional', type=Path, required=True)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--run-models', action='store_true')
    parser.add_argument('--gap', default='/opt/homebrew/bin/gap')
    args = parser.parse_args()
    need(not args.out.exists(), 'fresh output directory required')
    args.out.mkdir(parents=True)
    counts = [exports(args.main, MAIN), exports(args.exceptional, EXCEPTIONAL)]
    need(counts == [39, 23], 'incomplete reviewed editions')
    original = contexts(args.main)
    addition = contexts(args.exceptional)
    need(len(original['source_rows']) == 38 and len(original['proof_contexts']) == 15
         and len(addition['proof_contexts']) == 4, 'incomplete source/proof scope')
    need([r['main_row'] for r in addition['additive_source_dispositions']] == ['R23', 'R29']
         and addition['main_manifest_sha256'] == MAIN, 'incorrect additive corrections')
    questions = [r for r in original['source_rows'] if r['id'].startswith('Q')]
    need([r['id'] for r in questions] == ['Q1', 'Q2', 'Q3']
         and all(r['status'] == 'outside_contract_no_answer_claim' for r in questions),
         'final problems incorrectly promoted')
    if args.source:
        need(sha(args.source) == SOURCE, 'changed primary source edition')
    if (ROOT / 'manifest.json').exists():
        exports(ROOT, sha(ROOT / 'manifest.json'))
    controls = models(args.out, args.gap) if args.run_models else []
    report = dict(status='PASS_DISTINCT_COMPLETE_F005_SCIENCE',
                  author_manifests=[MAIN, EXCEPTIONAL], exports=counts,
                  source_rows=38, corrected_principal_and_background_rows=35,
                  written_proof_contexts=19, additive_rows=['R23', 'R29'],
                  source_rechecked=args.source is not None,
                  models_replayed=args.run_models, rejected_controls=controls,
                  author_model_imports=False, finite_validation_is_not_general_proof=True,
                  generic_Lean_declarations_previously_replayed=2,
                  new_Lean_declarations_in_this_replay=0, full_source_formalized=False,
                  unanswered_final_problems=[1, 2, 3], new_original_credit=0,
                  new_question_credit=0, compression_factor=None)
    dump(args.out / 'report.json', report)
    print(json.dumps(report))


if __name__ == '__main__':
    main()
