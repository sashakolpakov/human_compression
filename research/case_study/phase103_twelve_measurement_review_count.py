#!/usr/bin/env python3
"""Independent phase103 recount; no measurement/render helper imports.

Requires private primary PDFs at the exact protocol paths. Public replacement
verification alone is available with --replacement-only. Neither mode changes
an input. --output must name a nonexistent file (including no symlink).
"""
import argparse
import hashlib
import json
import re
import unicodedata
from fractions import Fraction
from pathlib import Path

from pypdf import PdfReader

PROTOCOL_SHA = 'f297f3509ba598b5fc375e101a21e7381049d38d6cb27717c5287cc77b89f0ee'
MANIFEST_SHA = '7477a91be128f4c0fb953e4a7f4b9d422bd70a371367de1fcee2db0cd59b229d'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def bound(path, expected, size=None):
    data = path.read_bytes()
    require(sha(data) == expected, 'Hash mismatch: ' + str(path))
    if size is not None:
        require(len(data) == size, 'Size mismatch: ' + str(path))
    return data


def count(text, normalization):
    # Independent character-state implementation of maximal alphanumeric runs.
    text = unicodedata.normalize(normalization, text)
    alpha_runs = 0
    preceding_alpha = False
    nonspace = 0
    tokens = []
    word = []
    for ch in text:
        alpha = ch.isalnum()
        alpha_runs += int(alpha and not preceding_alpha)
        preceding_alpha = alpha
        if ch.isspace():
            if word:
                tokens.append(''.join(word))
                word = []
        else:
            nonspace += 1
            word.append(ch)
    if word:
        tokens.append(''.join(word))
    collapsed = ' '.join(tokens)
    return dict(unicode_normalization=normalization,
                whitespace_tokens=len(tokens), alphanumeric_units=alpha_runs,
                characters_without_whitespace=nonspace,
                characters_with_collapsed_whitespace=len(collapsed),
                utf8_bytes_with_collapsed_whitespace=len(collapsed.encode()),
                collapsed_text_sha256=sha(collapsed.encode()))


def span(text, s):
    a, b = s['start_codepoint'], s['end_codepoint_exclusive']
    require(0 <= a <= b <= len(text), 'Invalid span')
    require(sha(text[a:b].encode()) == s['sha256_utf8'], 'Span mismatch')
    return a, b


def selected(text, spec):
    start, end = span(text, spec['body'])
    ranges = sorted(span(text, ex) for ex in spec['exclusions'])
    cursor = start
    chunks = []
    for a, b in ranges:
        require(cursor <= a < b <= end, 'Overlapping/outside exclusion')
        chunks += [text[cursor:a], ' ']
        cursor = b
    return ''.join(chunks + [text[cursor:end]])


def nodes(tree):
    if isinstance(tree, dict):
        if 't' in tree:
            yield tree
        for value in tree.values():
            yield from nodes(value)
    elif isinstance(tree, list):
        for value in tree:
            yield from nodes(value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--replacement-pdf', type=Path)
    parser.add_argument('--replacement-only', action='store_true')
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    require(not args.output.exists() and not args.output.is_symlink(), 'Output exists')
    base = args.base
    protocol = json.loads(bound(base / 'phase98_twelve_measurement_protocol.json', PROTOCOL_SHA))
    manifest = json.loads(bound(base / 'phase98_twelve_measurement_manifest.json', MANIFEST_SHA))
    for name, binding in manifest['files'].items():
        bound(base / name, binding['sha256'], binding.get('bytes'))
    for name, binding in manifest['retained_nonprimary_inputs'].items():
        bound(base / name, binding['sha256'], binding.get('bytes'))
    report = json.loads((base / 'phase98_twelve_measurement_report.json').read_bytes())
    spec = protocol['documents']['Compress_12']
    manuscript = bound(base / spec['path'], spec['sha256']).decode()
    require(len(manuscript.encode()) == 317916, 'Manuscript size')
    require(spec['body']['start_codepoint'] == 161 and spec['body']['end_codepoint_exclusive'] == len(manuscript), 'Denominator boundary')
    require(not spec['exclusions'], 'Unexpected manuscript exclusion')
    body = selected(manuscript, spec)
    sections = [int(x) for x in re.findall(r'^## (\d+)\.', body, re.M)]
    require(sections == list(range(1, 27)), 'Section coverage')
    blocks = re.findall(r'^```(?:gap|python)\n(.*?)^```\s*$', body, re.M | re.S)
    require(len(blocks) == 8, 'Full program count')
    code_evidence = []
    for block, item in zip(blocks, protocol['certificate_programs']):
        actual = bound(base / item['path'], item['sha256'], item['bytes'])
        require(block.encode() == actual, 'Fenced program mismatch: ' + item['path'])
        code_evidence.append(item)
    pdf = args.replacement_pdf or base / 'phase98_twelve_measurement_render/replacement.pdf'
    pages = [p.extract_text() or '' for p in PdfReader(pdf).pages]
    require(len(pages) == 83, 'Replacement page count')
    rendered = '\n'.join(pages)
    require(sha(rendered.encode()) == protocol['expected_rendering']['extraction_sha256'], 'Replacement extraction')
    rendered_counts = {form: count(rendered, form) for form in ('NFC', 'NFKC')}
    require(rendered_counts == report['replacement']['rendered_metrics'], 'Replacement counts')
    compact = ''.join(rendered.split())
    start = 0
    ast_dir = base / 'phase98_twelve_measurement_render'
    # File names discovered from the frozen export; these are static AST evidence,
    # not imported executable helpers.
    ast_paths = sorted(ast_dir.glob('*.json'))
    asts = []
    for path in ast_paths:
        candidate = json.loads(path.read_text())
        if isinstance(candidate, dict) and 'pandoc-api-version' in candidate:
            asts.append((path.name, candidate))
    require(len(asts) == 2, 'Expected two Pandoc ASTs')
    structural = lambda ast: [n for n in nodes(ast) if n.get('t') in ('Math', 'CodeBlock', 'Table')]
    require(structural(asts[0][1]) == structural(asts[1][1]), 'Changed math/code/table AST')
    all_code = [n['c'][1] for n in nodes(asts[0][1]) if n.get('t') == 'CodeBlock']
    require(len(all_code) == 14, 'Total code block count')
    for block in all_code:
        target = ''.join(block.split())
        at = compact.find(target, start)
        require(at >= 0, 'Code absent or out of order in PDF')
        start = at + len(target)
    require(rendered.count('■') == 85, 'Proof-ending marks')
    results = {'schema': 'independent_phase103_helper_free_recount_v1', 'status': 'PASS',
               'author_manifest_sha256': MANIFEST_SHA, 'protocol_sha256': PROTOCOL_SHA,
               'replacement_only': args.replacement_only, 'helper_imports': [],
               'manuscript_bytes': 317916, 'excluded_initial_codepoints': 161,
               'sections': sections, 'programs': code_evidence,
               'program_bytes': sum(i['bytes'] for i in code_evidence),
               'all_14_code_blocks_complete_in_rendered_extraction': True,
               'math_code_table_AST_identity': True, 'replacement_pages': len(pages),
               'replacement_extraction_sha256': sha(rendered.encode()),
               'replacement_metrics': rendered_counts, 'source_metrics': {}}
    if not args.replacement_only:
        previous = json.loads((base / 'phase84_eleven_measurement_protocol.json').read_text())
        for key in protocol['source_keys']:
            source = protocol['documents'][key]
            if key in protocol['inherited_source_keys']:
                require(source == previous['documents'][key], 'Changed inherited source specification: ' + key)
            raw = bound(base / source['pdf_path'], source['pdf_sha256'], source['pdf_bytes'])
            primary_pages = [p.extract_text() or '' for p in PdfReader(base / source['pdf_path']).pages]
            require(len(primary_pages) == source['pages'], 'Source page count: ' + key)
            for page, page_binding in zip(primary_pages, source['page_spans']):
                require(sha(page.encode()) == page_binding['sha256_utf8'], 'Page extraction mismatch: ' + key)
            if key == 'N003':
                text = ''.join(f'\n--- PDF PAGE {i+1} ---\n{p}\n' for i, p in enumerate(primary_pages))
            elif key == 'N008':
                text = '\n\n'.join(f'[[PDF PAGE {i+1}; PRINTED {169+i}]]\n{p}' for i, p in enumerate(primary_pages))
            else:
                text = '\n'.join(primary_pages)
            require(sha(text.encode()) == source['extraction_sha256'], 'Source extraction: ' + key)
            clean = selected(text, source)
            values = {form: count(clean, form) for form in ('NFC', 'NFKC')}
            require(values == report['source_documents'][key]['metrics'], 'Source counts: ' + key)
            results['source_metrics'][key] = {'pdf_sha256': sha(raw), 'pages': len(primary_pages),
                'body_sha256': sha(clean.encode()), 'metrics': values,
                'excluded_spans': len(source['exclusions']), 'specification_verified': True}
        ratios = {}
        for form in ('NFC', 'NFKC'):
            ratios[form] = {}
            for metric in protocol['metric_keys']:
                numerator = sum(s['metrics'][form][metric] for s in results['source_metrics'].values())
                denominator = rendered_counts[form][metric]
                exact = Fraction(numerator, denominator)
                ratios[form][metric] = dict(numerator=numerator, denominator=denominator,
                    exact_rational=str(exact), decimal=float(exact))
        results['lower_bounds'] = ratios
        results['zero_credit_sources'] = {'N001': 0, 'L108': 0}
        results['exact_twelve_source_factor'] = None
        require(ratios['NFC']['whitespace_tokens']['exact_rational'] == '59636/44269', 'Primary result')
    with args.output.open('x') as stream:
        json.dump(results, stream, indent=2, ensure_ascii=False)
        stream.write('\n')
    print(json.dumps({'status': 'PASS', 'output': str(args.output), 'sha256': sha(args.output.read_bytes()),
                      'full_primary_recount': not args.replacement_only}))


if __name__ == '__main__':
    main()
