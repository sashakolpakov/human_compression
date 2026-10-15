"""Produce and independently read complete weight-orbit certificates."""
import argparse
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from verify_weights import matrices, require, verify
from central_matrices import verify as verify_centers


def compute(output):
    source = Path(__file__).resolve().parent
    require(not output.exists(), 'output must be fresh')
    output.mkdir(parents=True)
    build = subprocess.run(['clang++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Werror',
                            str(source / 'weight_orbits.cpp'), '-o', str(output / 'weight_orbits')],
                           capture_output=True, timeout=60)
    (output / 'compile.stdout').write_bytes(build.stdout)
    (output / 'compile.stderr').write_bytes(build.stderr)
    require(build.returncode == 0 and not build.stderr, 'compilation')
    results = []
    for n in (7, 8):
        c, b, _ = matrices(n)
        for k in range(n):
            stem = 'E%d_%d' % (n, k)
            inp = output / (stem + '.input')
            inp.write_text(f'{n} {k}\n' + '\n'.join(' '.join(map(str, row)) for row in c + b) + '\n')
            cert = output / (stem + '.txt')
            child = subprocess.run([str(output / 'weight_orbits'), str(inp), str(cert), '60'],
                                   capture_output=True, timeout=70)
            (output / (stem + '.stdout')).write_bytes(child.stdout)
            (output / (stem + '.stderr')).write_bytes(child.stderr)
            require(child.returncode == 0 and not child.stderr, 'complete producer ' + stem)
            record = verify(cert, n, k)
            require(child.stdout.decode().strip() == f'COMPLETE {n} {k} {record["vectors"]}', 'producer count')
            compressed = gzip.compress(cert.read_bytes(), compresslevel=9, mtime=0)
            (output / (stem + '.txt.gz')).write_bytes(compressed)
            record['certificate_sha256'] = hashlib.sha256(cert.read_bytes()).hexdigest()
            record['gzip_sha256'] = hashlib.sha256(compressed).hexdigest()
            results.append(record)
            print(json.dumps(record), flush=True)
    center = verify_centers()
    (output / 'central_matrices.json').write_text(json.dumps(center, indent=2) + '\n')
    # Damage a small orbit in ways that target mathematical coverage, not just hashes.
    original = (output / 'E7_6.txt').read_text().splitlines()
    controls = {}
    for label in ['missing_vector', 'changed_coordinate', 'wrong_header']:
        lines = original.copy()
        if label == 'missing_vector':
            del lines[2]
            fields = lines[0].split()
            fields[-1] = str(int(fields[-1]) - 1)
            lines[0] = ' '.join(fields)
        elif label == 'changed_coordinate':
            fields = lines[2].split()
            fields[0] = '31'
            lines[2] = ' '.join(fields)
        else:
            lines[0] = lines[0].replace('ORBIT 7 6', 'ORBIT 7 5')
        damaged = output / (label + '.txt')
        damaged.write_text('\n'.join(lines) + '\n')
        try:
            verify(damaged, 7, 6)
        except ValueError as error:
            controls[label] = str(error)
        else:
            raise ValueError('accepted damaged certificate ' + label)
    bad_input = output / 'bad.input'
    fields = (output / 'E7_6.input').read_text().split()
    fields[2] = '3'
    bad_input.write_text(' '.join(fields) + '\n')
    child = subprocess.run([str(output / 'weight_orbits'), str(bad_input), str(output / 'bad.txt'), '60'],
                           capture_output=True, timeout=15)
    require(child.returncode != 0 and b'wrong Cartan matrix' in child.stderr, 'producer malformed input')
    controls['wrong_cartan'] = child.stderr.decode().strip()
    report = {'status': 'COMPLETE_L033_SPHERICAL_FINITE_CERTIFICATES', 'orbits': results,
              'vectors': sum(x['vectors'] for x in results),
              'reflection_checks': sum(x['reflection_checks'] for x in results),
              'central_matrix_types': [x['type'] for x in center], 'damaged_controls': controls,
              'whole_original_credit': 0, 'new_question_credit': 0, 'new_Lean': 0,
              'written_proof_and_distinct_review_required': True}
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(compute(args.out.resolve())))
