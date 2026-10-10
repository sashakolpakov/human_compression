#!/usr/bin/env python3
"""Independent byte/scope checks. Does not prove source-span completeness."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import unicodedata
from fractions import Fraction


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--directory', type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    root = args.directory
    protocol_name = 'phase15_N003_measurement_protocol.json'
    protocol_bytes = (root / protocol_name).read_bytes()
    p = json.loads(protocol_bytes)
    source_path = root / 'sources/phase10_N003_extracted.txt'
    source_bytes = source_path.read_bytes()
    source = source_bytes.decode('utf-8')
    replacement_bytes = (root / p['replacement']['file']).read_bytes()
    replacement = replacement_bytes.decode('utf-8')
    assert digest(source_bytes) == p['source']['extracted_text_sha256']
    assert digest((root / 'sources/network_independent_generators.pdf').read_bytes()) == p['source']['pdf_sha256']
    assert digest(replacement_bytes) == p['replacement']['sha256']
    for side, text in [('source', source), ('replacement', replacement)]:
        previous = -1
        for span in p[side]['spans']:
            lo, hi = span['start_codepoint'], span['end_codepoint_exclusive']
            assert previous <= lo < hi <= len(text)
            assert digest(text[lo:hi].encode()) == span['raw_span_sha256']
            assert set(span['targets']) <= p['targets'].keys()
            previous = hi
    assert len(p['source']['spans']) == 9
    assert len(p['replacement']['spans']) == 8
    markers = list(re.finditer(r'<!-- proof:([a-z]+):start -->\n(.*?)<!-- proof:\1:end -->', replacement, re.S))
    assert len(markers) == 8
    for match, span in zip(markers, p['replacement']['spans']):
        assert match.span(2) == (span['start_codepoint'], span['end_codepoint_exclusive'])
        assert span['id'] == 'replacement_' + match.group(1)
    for x in p['source']['layout_exclusions']:
        raw = source[x['start_codepoint']:x['end_codepoint_exclusive']]
        assert digest(raw.encode()) == x['sha256']
        pattern = r'--- PDF PAGE [0-9]+ ---\n' if x['kind'] == 'extraction_page_marker' else r'[0-9]+\n'
        assert re.fullmatch(pattern, raw)
    x = p['source']['excluded_common_background_recital']
    lo, hi = x['start_codepoint'], x['end_codepoint_exclusive']
    assert (lo, hi) == (5470, 5689)
    assert digest(source[lo:hi].encode()) == x['raw_span_sha256']
    assert all(hi <= s['start_codepoint'] or lo >= s['end_codepoint_exclusive'] for s in p['source']['spans'])
    assert p['accounting']['shared_spans_counted_once_per_side'] is True
    # Independent counting implementation: use a set of excluded absolute
    # character positions and an alphanumeric state machine, not the author's
    # interval-splicing routine or token regex. Do not import its runner.
    layout_positions = set()
    for x in p['source']['layout_exclusions']:
        layout_positions.update(range(x['start_codepoint'], x['end_codepoint_exclusive']))
    counted = {}
    for side, text in [('source', source), ('replacement', replacement)]:
        counted[side] = {}
        for span in p[side]['spans']:
            lo, hi = span['start_codepoint'], span['end_codepoint_exclusive']
            visible = ''.join(text[i] for i in range(lo, hi)
                              if side != 'source' or i not in layout_positions)
            normalized = unicodedata.normalize('NFKC', visible).replace('\u00ad', '')
            token_count, within_token = 0, False
            for ch in normalized:
                alnum = ch.isalnum()
                token_count += int(alnum and not within_token)
                within_token = alnum
            counted[side][span['id']] = {
                'normalized_nonwhitespace_codepoints': sum(not ch.isspace() for ch in normalized),
                'unicode_alphanumeric_tokens': token_count,
                'raw_utf8_bytes': len(text[lo:hi].encode())
            }
    author_name = 'phase15_N003_measurement.json'
    author_bytes = (root / author_name).read_bytes()
    author = json.loads(author_bytes)
    for side in counted:
        assert counted[side] == {x['id']: x['metrics'] for x in author['selected_spans'][side]}
    names = list(next(iter(counted['source'].values())))
    totals = {}
    for name in names:
        a = sum(x[name] for x in counted['source'].values())
        b = sum(x[name] for x in counted['replacement'].values())
        totals[name] = {'source': a, 'replacement': b, 'exact_ratio': str(Fraction(a, b))}
        assert all(author['totals'][name][key] == val for key, val in totals[name].items())
    allocated = {'source': set(), 'replacement': set()}
    for target, reported in zip(p['accounting']['marginal_order'], author['marginal_in_order']):
        assert reported['target_added'] == target
        for side in allocated:
            required = {x['id'] for x in p[side]['spans'] if target in x['targets']}
            newly = required - allocated[side]
            assert set(reported['new_span_ids'][side]) == newly
            assert reported['new_cost'][side] == {name: sum(counted[side][s][name] for s in newly) for name in names}
            allocated[side].update(newly)
    assert all(allocated[side] == counted[side].keys() for side in allocated)
    report = {
        'status': 'PASS',
        'protocol_sha256': digest(protocol_bytes),
        'replacement_sha256': digest(replacement_bytes),
        'source_extraction_sha256': digest(source_bytes),
        'source_spans_verified': 9,
        'replacement_spans_verified': 8,
        'replacement_markers_verified': 8,
        'physical_layout_exclusions_verified': len(p['source']['layout_exclusions']),
        'common_W2_recital_exclusion_verified': True,
        'source_or_replacement_span_overlaps': 0,
        'author_measurement_sha256': digest(author_bytes),
        'independently_recomputed_totals': totals,
        'all_per_span_metrics_match': True,
        'all_marginal_allocations_match': True,
        'independence': 'No author runner imported or executed; counts recomputed from the exact bound extraction using excluded-position sets and a character-state token counter.',
        'limits': 'Exact byte/range/marker/count checks. Complete target/dependency coverage and symmetry of background are reviewed separately. Descriptive ratio of these fixed proofs under common unexpanded background; no whole-paper or corpus claim.'
    }
    out = args.output or root / 'phase15_N003_scope_check.json'
    out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
