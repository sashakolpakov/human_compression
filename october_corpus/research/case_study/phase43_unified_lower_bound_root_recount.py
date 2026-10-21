#!/usr/bin/env python3
"""Independent recount of a fresh phase43 rendering; no measurement-helper imports.

Needs the private bound source extractions and an existing fresh rendering.
Writes one NEW JSON file only. This is a length/integrity check, not a proof checker.
"""
import argparse
import hashlib
import json
from pathlib import Path
import unicodedata

PROTOCOL_SHA = '8c6459c1ed938f3bc8979579775b66f4b12af317029887e542e7338776dae4c0'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def count(text, form):
    text = unicodedata.normalize(form, text)
    tokens = text.split()
    # Count alphanumeric runs by transitions, independently of the author's regex.
    previous = False
    runs = 0
    for char in text:
        current = char.isalnum()
        runs += current and not previous
        previous = current
    compact = ' '.join(tokens)
    return {
        'unicode_normalization': form,
        'whitespace_tokens': len(tokens),
        'alphanumeric_units': runs,
        'characters_without_whitespace': len(''.join(tokens)),
        'characters_with_collapsed_whitespace': len(compact),
        'utf8_bytes_with_collapsed_whitespace': len(compact.encode()),
        'collapsed_text_sha256': digest(compact.encode()),
    }


def select(text, spec):
    b = spec['body']
    start, end = b['start_codepoint'], b['end_codepoint_exclusive']
    assert 0 <= start < end <= len(text)
    assert digest(text[start:end].encode()) == b['sha256_utf8']
    # Work backwards, replacing each metadata interval by exactly one space.
    result = text[start:end]
    last_start = end
    for ex in sorted(spec['exclusions'], key=lambda e: e['start_codepoint'], reverse=True):
        a, z = ex['start_codepoint'], ex['end_codepoint_exclusive']
        assert start <= a < z <= last_start
        assert digest(text[a:z].encode()) == ex['sha256_utf8']
        result = result[:a-start] + ' ' + result[z-start:]
        last_start = a
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--render-dir', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert not args.output.exists(), 'Refuse to overwrite an existing recount'
    root, render = args.input_root, args.render_dir
    data = (root/'phase43_unified_lower_bound_protocol.json').read_bytes()
    assert digest(data) == PROTOCOL_SHA
    p = json.loads(data)
    replay = json.loads((render/'report.json').read_text())
    assert replay['protocol_sha256'] == PROTOCOL_SHA
    assert all(replay['rendering']['checks'].values())
    b = json.loads((root/'phase38_compress_B_measurement_protocol.json').read_text())
    a = json.loads((root/'phase38_N001_source_boundary_proposal.json').read_text())
    inherited = {}
    for key in p['source_keys']:
        old = b['documents'][key] if key in b['source_keys'] else a['documents'][key]
        inherited[key] = all(p['documents'][key][x] == old[x] for x in ['body','exclusions'])
        assert inherited[key], key
    documents = {}
    for key in p['source_keys']:
        s = p['documents'][key]
        path = root/s.get('extraction_path', s.get('path'))
        data = path.read_bytes()
        assert digest(data) == s['extraction_sha256']
        cleaned = select(data.decode(), s)
        values = {form: count(cleaned, form) for form in p['forms']}
        assert values == replay['source_documents'][key]['metrics'], key
        assert digest(cleaned.encode()) == replay['source_documents'][key]['cleaned_body_sha256']
        documents[key] = values
    s = p['documents']['Compress_Unified']
    data = (root/s['path']).read_bytes()
    assert digest(data) == s['sha256']
    body = select(data.decode(), s)
    assert body == (render/'replacement.md').read_text()
    data = (render/'replacement_extraction.txt').read_bytes()
    assert digest(data) == p['expected_rendering']['extraction_sha256']
    replacement = {form: count(data.decode(), form) for form in p['forms']}
    assert replacement == p['expected_rendering']['metrics']
    totals = {form: {key: sum(documents[s][form][key] for s in p['source_keys'])
                     for key in p['metric_keys']} for form in p['forms']}
    assert totals == replay['source_body_sums']
    visual = json.loads((root/'phase43_unified_lower_bound_visual_review.json').read_text())
    pages = {}
    for item in visual['Compress_Unified']['page_hashes']:
        page = item['page']
        pages[page] = digest((render/f'page-{page:02d}.png').read_bytes())
        assert pages[page] == item['sha256']
    assert len(pages) == 27
    report = {
        'status': 'PASS', 'date': '2026-10-10',
        'scope': 'Independent body selection, ten counts, source-boundary inheritance and all27 raster hashes; no imported counting/body helper.',
        'protocol_sha256': PROTOCOL_SHA,
        'runner_sha256': digest(Path(__file__).read_bytes()),
        'fresh_render_report_sha256': digest((render/'report.json').read_bytes()),
        'render_directory': str(render), 'inherited_boundaries_equal': inherited,
        'source_metrics': documents, 'source_sums': totals, 'replacement_metrics': replacement,
        'raster_hashes_match_full_independent_visual_review': pages,
        'N001_numerator_credit': 0, 'exact_seven_source_factor': None,
        'primary_lower_bound_fraction': [40358, 18241],
        'mathematical_proof_check': False, 'automated_visual_judgment': False,
    }
    with args.output.open('x') as handle:
        json.dump(report, handle, indent=2)
        handle.write('\n')
    print('PASS: six bodies, full replacement, all ten metrics and all27 raster hashes.')


if __name__ == '__main__':
    main()
