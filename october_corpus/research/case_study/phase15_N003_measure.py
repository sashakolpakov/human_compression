#!/usr/bin/env python3
"""Measure the exact eight-result forest/parity proof without exporting source text.

Requires pypdf==6.13.0 and the primary PDF named by the protocol's hash.
All output contains metadata, counts and hashes only. Use --output in scratch
space when reproducing a frozen report.
"""
import argparse
from datetime import datetime, timezone
from fractions import Fraction
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import re
import unicodedata

import pypdf


def digest(data):
    return sha256(data).hexdigest()


def intervals(rows, length):
    spans = sorted((r['start_codepoint'], r['end_codepoint_exclusive']) for r in rows)
    assert all(0 <= a < b <= length for a, b in spans), 'invalid interval'
    assert all(b <= c for (_, b), (c, _) in zip(spans, spans[1:])), 'overlapping intervals'
    return spans


def metrics(raw, start, layout):
    # Remove only the source's exact hash-bound physical layout positions.
    stop = start + len(raw)
    cursor = start
    pieces = []
    for a, b in layout:
        if b <= start or a >= stop:
            continue
        a, b = max(a, start), min(b, stop)
        pieces.append(raw[cursor-start:a-start])
        cursor = b
    pieces.append(raw[cursor-start:])
    normalized = unicodedata.normalize('NFKC', ''.join(pieces)).replace('\u00ad', '')
    return {
        'normalized_nonwhitespace_codepoints': sum(not c.isspace() for c in normalized),
        'unicode_alphanumeric_tokens': len(re.findall(r'[^\W_]+', normalized)),
        'raw_utf8_bytes': len(raw.encode()),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    here = Path(__file__).resolve().parent
    parser.add_argument('--source-pdf', required=True, type=Path)
    parser.add_argument('--protocol', type=Path, default=here/'phase15_N003_measurement_protocol.json')
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    protocol_bytes = args.protocol.read_bytes()
    protocol = json.loads(protocol_bytes)
    source = protocol['source']
    assert pypdf.__version__ == source['pypdf_version'], 'extractor version differs'
    pdf_bytes = args.source_pdf.read_bytes()
    assert digest(pdf_bytes) == source['pdf_sha256'], 'primary PDF differs'
    reader = pypdf.PdfReader(BytesIO(pdf_bytes))
    assert len(reader.pages) == source['pdf_pages']
    text = ''.join('\n--- PDF PAGE '+str(i+1)+' ---\n'+(p.extract_text() or '')+'\n'
                   for i, p in enumerate(reader.pages))
    assert digest(text.encode()) == source['extracted_text_sha256'], 'extraction differs'
    replacement_path = args.protocol.parent/protocol['replacement']['file']
    replacement_bytes = replacement_path.read_bytes()
    assert digest(replacement_bytes) == protocol['replacement']['sha256'], 'replacement differs'
    replacement = replacement_bytes.decode('utf-8')
    layout = intervals(source['layout_exclusions'], len(text))
    for row in source['layout_exclusions']:
        assert digest(text[row['start_codepoint']:row['end_codepoint_exclusive']].encode()) == row['sha256']
    excluded = source['excluded_common_background_recital']
    a, b = excluded['start_codepoint'], excluded['end_codepoint_exclusive']
    assert digest(text[a:b].encode()) == excluded['raw_span_sha256']
    for c, d in intervals(source['spans'], len(text)):
        assert d <= a or b <= c, 'common background was charged'

    selected = {}
    for side, full_text in [('source', text), ('replacement', replacement)]:
        intervals(protocol[side]['spans'], len(full_text))
        selected[side] = []
        for row in protocol[side]['spans']:
            a, b = row['start_codepoint'], row['end_codepoint_exclusive']
            raw = full_text[a:b]
            assert digest(raw.encode()) == row['raw_span_sha256'], row['id']
            assert set(row['targets']) <= set(protocol['targets'])
            selected[side].append({**row, 'metrics': metrics(raw, a, layout if side == 'source' else [])})
    names = list(selected['source'][0]['metrics'])

    def total(side, ids=None):
        rows = [r for r in selected[side] if ids is None or r['id'] in ids]
        return {name: sum(r['metrics'][name] for r in rows) for name in names}

    totals = {}
    for name in names:
        a, b = total('source')[name], total('replacement')[name]
        totals[name] = {'source': a, 'replacement': b, 'ratio': a/b,
                        'exact_ratio': str(Fraction(a, b))}
    seen = {'source': set(), 'replacement': set()}
    marginal = []
    for target in protocol['accounting']['marginal_order']:
        added, costs = {}, {}
        for side in seen:
            needed = {r['id'] for r in selected[side] if target in r['targets']}
            new = needed-seen[side]
            seen[side].update(needed)
            added[side] = sorted(new)
            costs[side] = total(side, new)
        marginal.append({'target_added': target, 'new_span_ids': added, 'new_cost': costs})
    assert all(seen[side] == {r['id'] for r in selected[side]} for side in seen)
    main_metric = totals['normalized_nonwhitespace_codepoints']
    report = {
        'status': 'PASS', 'measured_at_utc': datetime.now(timezone.utc).isoformat(),
        'targets': protocol['targets'], 'pypdf_version': pypdf.__version__,
        'protocol_sha256': digest(protocol_bytes), 'script_sha256': digest(Path(__file__).read_bytes()),
        'source_pdf_sha256': digest(pdf_bytes), 'source_extraction_sha256': digest(text.encode()),
        'replacement_sha256': digest(replacement_bytes),
        'common_background_B': protocol['common_background_B'],
        'selected_spans': selected, 'totals': totals, 'marginal_in_order': marginal,
        'equal_background_cost_sensitivity': {
            'interpretation': 'Illustrative equal added costs, not estimates of retained proof lengths',
            'metric': 'normalized_nonwhitespace_codepoints',
            'scenarios': [{'added_to_each_side': c,
                           'ratio': (main_metric['source']+c)/(main_metric['replacement']+c)}
                          for c in (0, 1000, 10000, 100000)]},
        'separate_costs': {'replacement_file_utf8_bytes': len(replacement_bytes),
                           'replacement_unmeasured_scaffolding_utf8_bytes': len(replacement_bytes)-total('replacement')['raw_utf8_bytes'],
                           'measurement_script_utf8_bytes': Path(__file__).stat().st_size,
                           'protocol_utf8_bytes': len(protocol_bytes),
                           'computational_certificate_bytes_required_for_written_proof': 0,
                           'search_or_runtime_comparison': 'Not measured'},
        'accounting': protocol['accounting'], 'limitations': protocol['limitations'],
        'mathematical_proof_review': 'Separate review artifact; this program measures bytes, not proof validity',
    }
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps({'status': 'PASS', 'numbered_targets': len(protocol['targets']),
                      'totals': totals, 'output': args.output.name}, indent=2))


if __name__ == '__main__':
    main()
