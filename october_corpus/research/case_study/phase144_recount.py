#!/usr/bin/env python3
"""Portable helper-free recount; --primary-check additionally needs private PDFs.

The public path verifies the complete replacement and recomputes the arithmetic
from hash-bound source measurements. It does not claim to reread absent sources.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parent
sha = lambda b: hashlib.sha256(b).hexdigest()


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def counter(text, form):
    n = unicodedata.normalize(form, text)
    compact = ' '.join(n.split())
    return dict(unicode_normalization=form, whitespace_tokens=len(compact.split()),
        alphanumeric_units=len(re.findall(r'[^\W_]+', n)),
        characters_without_whitespace=sum(not ch.isspace() for ch in n),
        characters_with_collapsed_whitespace=len(compact),
        utf8_bytes_with_collapsed_whitespace=len(compact.encode()),
        collapsed_text_sha256=sha(compact.encode()))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=ROOT)
    ap.add_argument('--primary-check', action='store_true')
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    require(not os.path.lexists(a.output), 'Refusing existing output')
    root = a.root.resolve()
    manifest = json.loads((root / 'phase144_manifest.json').read_text())
    for binding in manifest['files'] + manifest['required_shared_inputs']:
        data = (root / binding['path']).read_bytes()
        require(sha(data) == binding['sha256'] and len(data) == binding['bytes'], 'Binding changed: ' + binding['path'])
    protocol = json.loads((root / 'phase144_measurement_protocol.json').read_text())
    report = json.loads((root / 'phase144_render/report.json').read_text())
    require(report['protocol_sha256'] == sha((root / 'phase144_measurement_protocol.json').read_bytes()), 'Protocol/report mismatch')
    import pypdf
    require(pypdf.__version__ == protocol['expected_toolchain']['pypdf'], 'pypdf version changed')
    pdf = pypdf.PdfReader(root / 'phase144_render/replacement.pdf')
    text = '\n'.join(page.extract_text() or '' for page in pdf.pages)
    require(sha(text.encode()) == report['replacement']['extraction_sha256'], 'Replacement extraction changed')
    require(len(pdf.pages) == report['replacement']['pages'], 'Page count changed')
    denominator = {form: counter(text, form) for form in protocol['forms']}
    require(denominator == report['replacement']['metrics'], 'Independent denominator mismatch')

    # Check the actual printed code, not only the Markdown AST. Whitespace is
    # layout-dependent; every nonwhitespace code character must occur in order.
    appendix = text[text.rindex('Complete computational proof appendix'):]
    code_bindings = protocol['certificate_programs']
    headings = [re.search(r'(?m)^' + re.escape(b['path']) + '$', appendix) for b in code_bindings]
    require(all(headings), 'Missing exact program heading')
    code_checks = []
    for i, b in enumerate(code_bindings):
        end = headings[i+1].start() if i+1 < len(headings) else len(appendix)
        actual = ''.join(appendix[headings[i].end():end].split())
        expected = ''.join((root / b['path']).read_text().split())
        require(actual == expected, 'Printed program character mismatch: ' + b['path'])
        code_checks.append(dict(path=b['path'], complete_nonwhitespace_characters=len(actual),
            sha256=sha(actual.encode()), exact_ordered_equality=True))

    def code_nodes(tree):
        rows = []
        def walk(x):
            if isinstance(x, dict):
                if x.get('t') == 'CodeBlock':
                    rows.append(x['c'])
                for y in x.values(): walk(y)
            elif isinstance(x, list):
                for y in x: walk(y)
        walk(tree)
        return rows
    original = code_nodes(json.loads((root / 'phase144_render/replacement.json').read_text()))
    display = code_nodes(json.loads((root / 'phase144_render/render.json').read_text()))
    mapping = json.loads((root / 'phase144_render/code_display_wrap.json').read_text())
    require(len(original) == len(display) == len(mapping) == 5, 'Code-block accounting mismatch')
    for old, new, row in zip(original, display, mapping):
        chunks = new[1].split('\n'); rebuilt = []; cursor = 0
        for count in row['original_line_chunk_counts']:
            rebuilt.append(''.join(chunks[cursor:cursor+count])); cursor += count
        require(cursor == len(chunks) and '\n'.join(rebuilt) == old[1], 'Display map is not invertible')

    source_metrics = {key: row['metrics'] for key, row in report['source_documents'].items()}
    if a.primary_check:
        source_metrics = {}
        for key in protocol['source_keys']:
            s = protocol['documents'][key]
            raw = (root / s['pdf_path']).read_bytes()
            require(sha(raw) == s['pdf_sha256'], 'Primary PDF changed: ' + key)
            pages = [page.extract_text() or '' for page in pypdf.PdfReader(root / s['pdf_path']).pages]
            full = '\n'.join(pages)
            require(sha(full.encode()) == s['extraction_sha256'] and len(pages) == s['pages'], 'Primary extraction changed: ' + key)
            def checked_span(span):
                lo, hi = span['start_codepoint'], span['end_codepoint_exclusive']
                require(0 <= lo <= hi <= len(full), 'Invalid source span')
                require(sha(full[lo:hi].encode()) == span['sha256_utf8'], 'Source span changed')
                return lo, hi
            start, end = checked_span(s['body'])
            cursor = start; pieces = []
            for exclusion in sorted(s['exclusions'], key=lambda x: x['start_codepoint']):
                lo, hi = checked_span(exclusion)
                require(cursor <= lo < hi <= end, 'Invalid or overlapping exclusion')
                pieces.extend([full[cursor:lo], ' ']); cursor = hi
            pieces.append(full[cursor:end]); body = ''.join(pieces)
            source_metrics[key] = {form: counter(body, form) for form in protocol['forms']}
            require(source_metrics[key] == report['source_documents'][key]['metrics'], 'Independent source count mismatch: ' + key)
    totals = {form: {metric: sum(source_metrics[key][form][metric] for key in protocol['source_keys'])
        for metric in protocol['metric_keys']} for form in protocol['forms']}
    require(totals == report['source_body_sums'], 'Source total mismatch')
    ratios = {form: {metric: dict(numerator=totals[form][metric], denominator=denominator[form][metric],
        factor=totals[form][metric] / denominator[form][metric]) for metric in protocol['metric_keys']} for form in protocol['forms']}
    require(ratios == report['comparisons'], 'Ratio mismatch')
    result = dict(status='PASS', helper_modules_imported=False, primary_sources_freshly_recounted=a.primary_check,
        replacement_pages=len(pdf.pages), exact_code_display_recovery=True, printed_program_checks=code_checks,
        source_body_sums=totals, denominator=denominator, comparisons=ratios,
        mathematical_proofs_or_programs_executed=False)
    with a.output.open('x') as f:
        json.dump(result, f, indent=2); f.write('\n')
    print(json.dumps(dict(status='PASS', primary_check=a.primary_check, pages=len(pdf.pages), NFC=ratios['NFC'])))


if __name__ == '__main__':
    main()
