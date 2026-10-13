"""Extract the bounded numeric records used by the reviewed L059 recovery.

This acquisition utility uses the private primary files. The separate public
replay consumes only its numeric output and the retained derived graph data.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys

if sys.flags.optimize:
    raise RuntimeError('optimized Python is unsupported')

def need(ok, message):
    if not ok:
        raise ValueError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sources', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(exist_ok=False)
    pins = {
        'CAT_lcf.txt': 'ed659ec12aaab934021ed1174ddec14b2177d47ee126171da7616f01b678354d',
        'CSS_lcf.txt': '283db343ed4c7cfeadc08b4ae4a1611ae0b67f21bab34ef5e182bbc399e526ad',
    }
    records = []
    counts = {}
    for prefix, cutoff in [('CAT', 2048), ('CSS', 768)]:
        path = args.sources / (prefix + '_lcf.txt')
        need(sha(path) == pins[path.name], 'exact primary edition ' + path.name)
        identifiers = set()
        selected = 0
        for number, line in enumerate(path.read_text().splitlines(), 1):
            match = re.fullmatch(r'([!?]) (\d+) (\d+): \[(-?\d+(?:,-?\d+)*)\]\^(\d+)', line)
            missing = re.fullmatch(r'# (\d+) (\d+):', line)
            need(match is not None or missing is not None, 'primary grammar')
            if match:
                marker, ns, ix, shifts, power = match.groups()
                shifts = [int(x) for x in shifts.split(',')]
                power = int(power)
            else:
                ns, ix = missing.groups()
                marker, shifts, power = '#', None, None
            n = int(ns)
            name = f'{prefix}_{n}_{int(ix)}'
            need(name not in identifiers, 'duplicate primary identifier')
            identifiers.add(name)
            if shifts is not None:
                need(len(shifts) * power == n, 'LCF repetition')
            if n > cutoff:
                continue
            need(shifts is not None or name in {'CAT_10_1', 'CAT_28_1'}, 'unknown placeholder')
            records.append({'id': name, 'n': n, 'index': int(ix), 'marker': marker,
                            'lcf': shifts, 'power': power, 'primary_line': number,
                            'primary_line_sha256': hashlib.sha256(line.encode()).hexdigest(),
                            'construction': ('lcf' if shifts is not None else
                                             'petersen' if n == 10 else 'coxeter')})
            selected += 1
        counts[prefix] = {'full_primary_records': len(identifiers), 'selected': selected,
                          'cutoff': cutoff}
    need(counts['CAT']['full_primary_records'] == 3815 and
         counts['CSS']['full_primary_records'] == 1043 and
         counts['CAT']['selected'] == 796 and counts['CSS']['selected'] == 43,
         'exact scope')
    old_path = args.sources / 'cubic_source_verification.json'
    old_report = json.loads(old_path.read_text())
    old = {row['id']: row for row in old_report['graphs']}
    need(old_report['status'] == 'PASS' and len(old) == 839, 'reviewed input report')
    for row in records:
        need(old[row['id']]['primary_line'] == row['primary_line'] and
             old[row['id']]['primary_line_sha256'] == row['primary_line_sha256'],
             'reviewed primary record')
    reuse = [{key: row[key] for key in ['id', 'n', 'retained_id', 'isomorphism']}
             for row in old_report['graphs'] if 'retained_id' in row]
    need(len(reuse) == 261, 'exact reused input count')
    for name, value in [('numeric_roster.json', records), ('reuse_isomorphisms.json', reuse)]:
        (args.output / name).write_text(json.dumps(value, separators=(',', ':')) + '\n')
    provenance = {'status': 'EXTRACTED_BOUNDED_NUMERIC_INPUTS', 'scope': counts,
                  'primary_files': [{'filename': name, 'sha256': value,
                                     'bytes': (args.sources/name).stat().st_size}
                                    for name, value in pins.items()],
                  'reviewed_report_sha256': sha(old_path),
                  'extractor_sha256': sha(Path(__file__)),
                  'derived_inputs': [{'path': name, 'sha256': sha(args.sources/name)}
                                     for name in ['cubic_2048_bipartite.json',
                                                  'cubic_2048_nonbipartite.json',
                                                  'cubic_markings/inputs.json']],
                  'outputs': [{'path': name, 'sha256': sha(args.output/name)}
                              for name in ['numeric_roster.json', 'reuse_isomorphisms.json']],
                  'classification_completeness': 'unchanged borrowed primary census premise'}
    (args.output/'extraction_provenance.json').write_text(json.dumps(provenance, indent=2)+'\n')
    print('PASS_EXTRACTED_839_NUMERIC_RECORDS_261_REUSE_MAPS')

if __name__ == '__main__':
    main()
