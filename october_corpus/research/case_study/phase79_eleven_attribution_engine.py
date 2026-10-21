#!/usr/bin/env python3
"""Verify an attribution sidecar and generate readers without editing its proof.

The checks bind manually reviewed attribution judgments to exact text. They
do not establish mathematical truth, historical novelty, or complete Lean scope.
"""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / 'research/case_study'
DEFAULT = STUDY / 'phase61_ten_source_attribution.json'


def digest(data):
    return sha256(data).hexdigest()


def bound_file(binding):
    path = (STUDY / binding['path']).resolve()
    if not path.is_relative_to(STUDY.resolve()):
        raise ValueError('binding escapes study directory')
    data = path.read_bytes()
    if digest(data) != binding['sha256'] or len(data) != binding['bytes']:
        raise ValueError('stale binding: ' + binding['path'])
    return data


def validate(sidecar):
    original = bound_file(sidecar['manuscript'])
    text = original.decode('utf-8')
    for row in sidecar['evidence']:
        bound_file(row)
    ids = set()
    for row in sidecar['notes']:
        identifier = row['id']
        if not re.fullmatch(r'[A-Z0-9]+', identifier) or identifier in ids:
            raise ValueError('invalid/duplicate note identifier')
        ids.add(identifier)
        anchor = row['anchor']
        start, end = anchor['start_codepoint'], anchor['end_codepoint_exclusive']
        if not (0 <= start < end <= len(text)):
            raise ValueError('invalid span: ' + identifier)
        snippet = text[start:end]
        if digest(snippet.encode()) != anchor['sha256_utf8']:
            raise ValueError('stale span: ' + identifier)
        if not snippet.startswith(anchor['exact_prefix']):
            raise ValueError('stale prefix: ' + identifier)
        offset = row['insert_after_codepoint']
        if not (start < offset <= end):
            raise ValueError('insertion outside span: ' + identifier)
        codes = row['markers']
        if not codes or len(set(codes)) != len(codes) or set(codes) - set('BIRCVLMO'):
            raise ValueError('invalid markers: ' + identifier)
        if 'B' in codes and not row['borrowed_inputs']:
            raise ValueError('borrowed input missing: ' + identifier)
        if 'I' in codes and not row['repository_contribution']:
            raise ValueError('contribution missing: ' + identifier)
        if 'R' in codes and len(row['recovered_targets']) < 2:
            raise ValueError('multiple targets missing: ' + identifier)
        if 'V' in codes and not row['finite_evidence']:
            raise ValueError('finite evidence missing: ' + identifier)
        if 'C' in codes and not row['correction']:
            raise ValueError('correction missing: ' + identifier)
        for evidence in row['finite_evidence']:
            bound_file(evidence)
        if 'L' in codes:
            if not row['lean']:
                raise ValueError('Lean scope missing: ' + identifier)
            for certificate in row['lean']:
                source = bound_file(certificate['source'])
                report = json.loads(bound_file(certificate['report']))
                if report['exit_code'] != 0 or report['sha256'] != digest(source):
                    raise ValueError('stale Lean report: ' + identifier)
                if certificate['declaration'] not in report['stdout']:
                    raise ValueError('declaration absent from report')
                if 'sorryAx' in report['stdout'] or re.search(r'\b(sorry|admit)\b', source.decode()):
                    raise ValueError('placeholder in formal evidence')
                if not certificate['scope']:
                    raise ValueError('formal scope absent')
        if 'M' in codes:
            measure = row.get('measurement')
            if not measure or measure.get('status') != 'independently_reviewed':
                raise ValueError('measurement not reviewed')
            for key in ('numerator', 'denominator', 'metric', 'review'):
                if not measure.get(key):
                    raise ValueError('measurement evidence absent')
            bound_file(measure['review'])
        if 'O' in codes:
            resolution = row.get('open_conjecture')
            if not resolution or resolution.get('proof_status') != 'independently_reviewed' or resolution.get('priority_status') != 'verified_previously_open':
                raise ValueError('open-conjecture proof/priority not cleared')
            for key in ('proof_review', 'priority_review'):
                bound_file(resolution[key])
            if not resolution.get('exact_statement_and_version'):
                raise ValueError('exact conjecture missing')
    return original, text


def note_text(row):
    signs = ' '.join('[' + c + ']' for c in row['markers'])
    return '**' + signs + ' — ' + row['id'] + '.** ' + row['summary']


def ledger_text(sidecar):
    lines = ['# Attribution ledger for Compress_10', '',
             'Bound manuscript SHA-256: `' + sidecar['manuscript']['sha256'] + '`.', '',
             '[Legend and scope](../../ATTRIBUTION.md). These annotations add no proof premises or steps.', '',
             '**No ten-source measured factor or previously-open-conjecture claim is cleared.**', '']
    for row in sidecar['notes']:
        lines.extend(['## ' + row['id'] + ' — ' + row['label'], '', note_text(row), ''])
        if row['borrowed_inputs']:
            lines.extend(['Borrowed: ' + '; '.join(row['borrowed_inputs']) + '.', ''])
        if row['repository_contribution']:
            lines.extend(['Repository contribution: ' + row['repository_contribution'], '',
                          'Historical novelty: ' + row['historical_novelty'] + '.', ''])
        if row['recovered_targets']:
            lines.extend(['Targets: ' + '; '.join(row['recovered_targets']) + '.', ''])
        if row['correction']:
            lines.extend(['Correction/scope: ' + row['correction'], ''])
        for cert in row['lean']:
            lines.extend(['Lean: `' + cert['declaration'] + '`. ' + cert['scope'], ''])
        for evidence in row['finite_evidence']:
            lines.extend(['Finite evidence: [' + evidence['path'] + '](' + evidence['path'] + ').', ''])
    return '\n'.join(lines)


def insert_notes(text, notes, pandoc=False):
    parts, cursor = [], 0
    for row in sorted(notes, key=lambda r: (r['insert_after_codepoint'], r['id'])):
        offset = row['insert_after_codepoint']
        parts.append(text[cursor:offset])
        if pandoc:
            addition = ('\n\n::: {.audit-margin data-note="' + row['id']
                        + '" data-codes="' + ' '.join(row['markers']) + '"}\n'
                        + note_text(row) + '\n:::\n')
        else:
            addition = '\n\n> ' + note_text(row) + '\n'
        parts.append(addition)
        cursor = offset
    parts.append(text[cursor:])
    # The odd-indexed pieces are the only inserted material. This checks that
    # rendering did not delete, correct, normalize or reorder original bytes.
    recovered = ''.join(parts[::2])
    if recovered != text:
        raise ValueError('annotation changed original proof')
    return ''.join(parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sidecar', type=Path, default=DEFAULT)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    if args.output_dir.exists():
        parser.error('output directory exists; refusing to overwrite')
    raw_sidecar = args.sidecar.read_bytes()
    sidecar = json.loads(raw_sidecar)
    original, text = validate(sidecar)
    erratum = bound_file(sidecar['erratum']).decode()
    ledger = ledger_text(sidecar)
    prefix = ('# Annotated reader: Compress_10\n\n'
              'The original manuscript below is preserved byte for byte apart from inserted audit notes. '
              'Its original pending-review heading is historical: the complete independent review and root admission now pass with the appended required erratum. '
              '[Legend and attribution scope](../../ATTRIBUTION.md). No ten-source numerical factor or newly solved open conjecture is claimed.\n\n')
    suffix = '\n\n' + erratum + '\n\n' + ledger
    markdown = prefix + insert_notes(text, sidecar['notes']) + suffix
    pandoc = prefix + insert_notes(text, sidecar['notes'], pandoc=True) + suffix
    report = {
        'status':'PASS_annotation_integrity', 'mathematical_proof_checker':False,
        'historical_novelty_checker':False, 'sidecar_sha256':digest(raw_sidecar),
        'manuscript_sha256':digest(original), 'notes':len(sidecar['notes']),
        'marker_counts':dict(sorted(Counter(c for r in sidecar['notes'] for c in r['markers']).items())),
        'original_recovered_exactly':True, 'new_Lean_build':False,
        'frozen_manuscript_modified':False, 'annotated_edition_length_ratio':None,
        'original_bytes':len(original), 'annotated_reader_bytes':len(markdown.encode()),
        'reader_added_bytes_including_legend_erratum_and_ledger':len(markdown.encode())-len(original),
        'reader_sha256':digest(markdown.encode()), 'ledger_sha256':digest(ledger.encode())
    }
    args.output_dir.mkdir(parents=True, exist_ok=False)
    for name, content in [('reader.md', markdown), ('reader.pandoc.md', pandoc), ('ledger.md', ledger), ('report.json', json.dumps(report,indent=2)+'\n')]:
        (args.output_dir/name).write_text(content)
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
