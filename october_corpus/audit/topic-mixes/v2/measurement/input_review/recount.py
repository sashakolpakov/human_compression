#!/usr/bin/env python3
"""Independent metric recount. Glyph interpretation is reviewed separately."""
import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path

from pypdf import PdfReader


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text())


def count(text, normalization):
    normalized = unicodedata.normalize(normalization, text)
    tokens = normalized.split()
    collapsed = ' '.join(tokens)
    groups = re.findall(r'[^\W_]+', normalized)
    return {
        'whitespace_tokens': len(tokens),
        'alphanumeric_units': len(groups),
        'characters_without_whitespace': len(''.join(tokens)),
        'characters_with_collapsed_whitespace': len(collapsed),
        'utf8_bytes_with_collapsed_whitespace': len(collapsed.encode('utf-8')),
        'collapsed_text_sha256': sha(collapsed.encode('utf-8')),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--study', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(not args.out.exists(), 'fresh output')
    packet = args.packet
    need(sha((packet / 'manifest.json').read_bytes()) ==
         '6327d4327795eeebd3c3ceb044a99f056ea18ddf865bba720c4920d378db727e',
         'fixed proposed inputs')
    for row in read(packet / 'manifest.json')['exports']:
        data = (packet / row['path']).read_bytes()
        need(len(data) == row['bytes'] and sha(data) == row['sha256'], row['path'])
    policy = read(packet / 'policy.json')
    specifications = read(packet / 'input_spec.json')
    proposed = read(packet / 'author_counts.json')
    documents = {}
    for key, row in specifications.items():
        root = packet if row['root'] == 'packet' else args.study
        data = (root / row['path']).read_bytes()
        need(sha(data) == row['sha256'] and len(data) == row['bytes'], key + ' bytes')
        pages = [page.extract_text() or '' for page in PdfReader(root / row['path']).pages]
        raw = '\n'.join(pages)
        need(len(pages) == row['pages'] and sha(raw.encode()) == row['extraction_sha256'],
             key + ' complete ordinary extraction')
        cuts = row['excluded_furniture']
        for cut in cuts:
            need(raw[cut['start']:cut['end']] == cut['literal'], key + ' literal furniture')
        glyphs = row['glyph_substitutions']
        for glyph in glyphs:
            need(raw[glyph['start']:glyph['end']] == glyph['input'], key + ' literal glyph')
        variants = {'raw_untrimmed': raw}
        for name, replacements in [
            ('raw_selected', [(r['start'], r['end'], '\n') for r in cuts]),
            ('calibrated_selected', [(r['start'], r['end'], '\n') for r in cuts] +
             [(r['start'], r['end'], r['output']) for r in glyphs]),
        ]:
            replacements.sort()
            need(all(replacements[i][1] <= replacements[i + 1][0]
                     for i in range(len(replacements) - 1)), 'disjoint replacements')
            value = raw
            for left, right, replacement in reversed(replacements):
                value = value[:left] + replacement + value[right:]
            variants[name] = value
        metrics = {key: {form: count(text, form) for form in ['NFC', 'NFKC']}
                   for key, text in variants.items()}
        need(metrics == proposed['documents'][key]['metrics'], key + ' all30 metric cells')
        documents[key] = metrics

    raw_files = {}
    for category in ['programs', 'drivers', 'formal']:
        for row in policy[category]:
            data = (args.study / row['path']).read_bytes()
            need(len(data) == row['bytes'] and sha(data) == row['sha256'], 'whole raw file')
            metrics = {form: count(data.decode(), form) for form in ['NFC', 'NFKC']}
            need(metrics == proposed['raw_files'][category][row['path']]['metrics'],
                 row['path'] + ' all10 raw cells')
            raw_files[row['path']] = metrics
    old_row = policy['reused_accepted_inputs']['counts']
    old_data = (args.study / old_row['path']).read_bytes()
    need(len(old_data) == old_row['bytes'] and sha(old_data) == old_row['sha256'],
         'exact accepted earlier input counts')
    need(json.loads(old_data) == proposed['retained_accepted_inputs'],
         'all old PDF and raw cells retained literally')
    result = {
        'status': 'PASS_INDEPENDENT_ALL_COORDINATE_RECOUNT',
        'new_PDF_cells': 150, 'new_raw_cells': 60,
        'retained_PDF_cells': 180, 'retained_raw_cells': 70,
        'author_module_imported': False,
        'raw_primary_from_uninstrumented_pypdf': True,
        'calibration_semantics': 'Requires separate glyph/font evidence review; this recount checks the exact declared substitutions and their counts.',
        'no_ratio_computed': True,
        'documents': documents, 'raw_files': raw_files,
    }
    args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(result['status'])


if __name__ == '__main__':
    main()
