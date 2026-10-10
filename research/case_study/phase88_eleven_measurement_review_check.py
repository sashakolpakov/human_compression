#!/usr/bin/env python3
"""Independent phase84 measurement recount; imports no author measurement helpers.

Requires the private bound primary PDFs and a completed fresh phase84 rasterized
replay. Writes only a new JSON report, never an input or existing output.
"""
import argparse
from fractions import Fraction
import hashlib
import io
import json
import logging
import os
from pathlib import Path
import re
import subprocess
import unicodedata
import pypdf

HERE = Path(__file__).resolve().parent
PROTOCOL = 'phase84_eleven_measurement_protocol.json'
PROTOCOL_HASH = '7862cfcaa472b52eb94aeca47f77f47afbf7c33ae2fc47df1a78651e84623962'
MANIFEST_HASH = 'e1d73fa3845442af52765491ab57794c69d9ec5fbb81e2b378a283c58952976d'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def require(test, message):
    if not test:
        raise ValueError(message)


def count(text, form):
    text = unicodedata.normalize(form, text)
    words = text.split()
    collapsed = ' '.join(words)
    return dict(unicode_normalization=form, whitespace_tokens=len(words),
                alphanumeric_units=len(re.findall(r'[^\W_]+', text)),
                characters_without_whitespace=sum(not c.isspace() for c in text),
                characters_with_collapsed_whitespace=len(collapsed),
                utf8_bytes_with_collapsed_whitespace=len(collapsed.encode()),
                collapsed_text_sha256=digest(collapsed.encode()))


def select(text, spec):
    def span(s):
        a, b = s['start_codepoint'], s['end_codepoint_exclusive']
        require(0 <= a < b <= len(text), 'bad span')
        require(digest(text[a:b].encode()) == s['sha256_utf8'], 'span hash')
        return a, b
    start, end = span(spec['body'])
    cursor, chunks = start, []
    for exclusion in sorted(spec['exclusions'], key=lambda s: s['start_codepoint']):
        a, b = span(exclusion)
        require(cursor <= a < b <= end, 'overlap or outside-body exclusion')
        chunks += [text[cursor:a], ' ']
        cursor = b
    chunks.append(text[cursor:end])
    return ''.join(chunks)


def extract(path):
    buffer = io.StringIO()
    logger = logging.getLogger('pypdf')
    handler = logging.StreamHandler(buffer)
    old = logger.propagate
    logger.propagate = False
    logger.addHandler(handler)
    try:
        reader = pypdf.PdfReader(path)
        pages = [page.extract_text() or '' for page in reader.pages]
    finally:
        logger.removeHandler(handler)
        logger.propagate = old
    return pages, buffer.getvalue().splitlines()


def nodes(ast, kind):
    found = []
    def visit(n):
        if isinstance(n, dict):
            if n.get('t') == kind:
                found.append(n)
            for value in n.values():
                visit(value)
        elif isinstance(n, list):
            for value in n:
                visit(value)
    visit(ast)
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-root', type=Path, default=HERE)
    parser.add_argument('--replay-dir', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    require(not os.path.lexists(args.output), 'Refusing existing output')
    root, replay = args.input_root.resolve(), args.replay_dir.resolve()
    inputs = {}
    def bound(path, expected, size=None):
        path = path if path.is_absolute() else root / path
        data = path.read_bytes()
        require(digest(data) == expected, 'bound hash: ' + str(path))
        require(size is None or len(data) == size, 'bound size: ' + str(path))
        inputs[str(path)] = expected
        return data
    p = json.loads(bound(Path(PROTOCOL), PROTOCOL_HASH))
    manifest = json.loads(bound(Path('phase84_eleven_measurement_manifest.json'), MANIFEST_HASH))
    require(set(manifest['export_allowlist']) <= set(manifest['files']), 'author allowlist')
    for name, spec in manifest['files'].items():
        bound(Path(name), spec['sha256'], spec['bytes'])
    for spec in p['contract_bindings'] + p['external_costs'] + [p['measurement_helper'], p['render_helper']]:
        bound(Path(spec['path']), spec['sha256'], spec['bytes'])
    prior = json.loads((root / 'phase57_ten_source_measurement_protocol.json').read_text())
    require(pypdf.__version__ == '6.13.0', 'pypdf version')
    source = {}
    for key in p['source_keys']:
        spec = p['documents'][key]
        require(spec == prior['documents'][key], 'source specification changed: ' + key)
        bound(Path(spec['pdf_path']), spec['pdf_sha256'], spec['pdf_bytes'])
        pages, warnings = extract(root / spec['pdf_path'])
        require(len(pages) == spec['pages'], 'page count: ' + key)
        require(warnings == spec['expected_extraction_warnings'], 'warnings: ' + key)
        require(len(pages) == len(spec['page_spans']), 'page span count')
        for page, span in zip(pages, spec['page_spans']):
            require(digest(page.encode()) == span['sha256_utf8'], 'page hash: ' + key)
        if spec.get('extraction_format') == 'N003_legacy_markers':
            text = ''.join(f'\n--- PDF PAGE {i+1} ---\n' + t + '\n' for i, t in enumerate(pages))
        elif spec.get('extraction_format') == 'N008_legacy_markers':
            text = '\n\n'.join(f'[[PDF PAGE {i+1}; PRINTED {169+i}]]\n' + t for i, t in enumerate(pages))
        else:
            text = '\n'.join(pages)
        require(digest(text.encode()) == spec['extraction_sha256'], 'extraction: ' + key)
        body = select(text, spec)
        source[key] = dict(pdf_sha256=spec['pdf_sha256'], pages=len(pages),
                           extraction_sha256=digest(text.encode()),
                           body=spec['body'], exclusions=len(spec['exclusions']),
                           cleaned_body_sha256=digest(body.encode()),
                           metrics={f: count(body, f) for f in p['forms']},
                           nonwhitespace_control_codepoints=sorted({ord(c) for c in body if ord(c)<32 and not c.isspace()}),
                           extraction_warnings=warnings)
    spec = p['documents']['Compress_11']
    raw = bound(Path(spec['path']), spec['sha256'], spec['bytes']).decode()
    require(spec['body']['end_codepoint_exclusive'] == len(raw), 'replacement not through EOF')
    require(spec['body']['start_codepoint'] == 161 and not spec['exclusions'], 'replacement body policy')
    body = select(raw, spec)
    require(body == (replay / 'replacement.md').read_text(), 'selected replacement differs')
    fresh = json.loads((replay / 'report.json').read_text())
    require(all(fresh['rendering']['checks'].values()), 'author replay check failed')
    pages, warnings = extract(replay / 'replacement.pdf')
    require(not warnings and len(pages) == 57, 'replacement PDF pages/warnings')
    extracted = '\n'.join(pages)
    require(digest(extracted.encode()) == p['expected_rendering']['extraction_sha256'], 'replacement extraction')
    metrics = {f: count(extracted, f) for f in p['forms']}
    require(metrics == p['expected_rendering']['metrics'], 'independent replacement metrics')
    sums = {f: {k: sum(s['metrics'][f][k] for s in source.values()) for k in p['metric_keys']} for f in p['forms']}
    require(sums == fresh['source_body_sums'], 'independent source sums')
    for key, value in source.items():
        require(value['metrics'] == fresh['source_documents'][key]['metrics'], 'source metrics: ' + key)
    asts = []
    for text in [body, (replay / 'render.md').read_text()]:
        result = subprocess.run(['pandoc', '--from=' + p['render']['reader'], '--to=json'],
                                input=text, capture_output=True, text=True, check=True)
        require(not result.stderr, 'Pandoc diagnostic')
        asts.append(json.loads(result.stdout))
    for kind in ['Math', 'CodeBlock', 'Table']:
        require(nodes(asts[0], kind) == nodes(asts[1], kind), 'AST changed: ' + kind)
    codes = [n['c'][1] for n in nodes(asts[1], 'CodeBlock')]
    require(len(codes) == 11 and len(nodes(asts[1], 'Table')) == 7, 'AST totals')
    require([digest(c.encode()) for c in codes] == p['expected_rendering']['ast']['code_sha256'], 'code hashes')
    require(extracted.count('■') == 75, 'QED marks')
    compact = ''.join(extracted.split())
    position = 0
    for code in codes:
        needle = ''.join(code.split())
        position = compact.find(needle, position)
        require(position >= 0, 'complete ordered code block missing from PDF')
        position += len(needle)
    for program in p['certificate_programs']:
        data = bound(Path(program['path']), program['sha256'], program['bytes'])
        require(sum((code + '\n').encode() == data for code in codes) == 1, 'complete program bytes')
    raster_hashes = {}
    for name, expected in p['expected_rendering']['raster_sha256'].items():
        actual = digest((replay / name).read_bytes())
        require(actual == expected, 'fresh raster: ' + name)
        raster_hashes[name] = actual
    require(len(raster_hashes) == 57, 'raster count')
    ratios = {f: {k: dict(numerator=sums[f][k], denominator=metrics[f][k],
                          fraction=str(Fraction(sums[f][k], metrics[f][k])),
                          value=sums[f][k]/metrics[f][k]) for k in p['metric_keys']} for f in p['forms']}
    require(sums['NFC']['whitespace_tokens'] == 51739 and metrics['NFC']['whitespace_tokens'] == 34845, 'headline')
    for path, expected in inputs.items():
        require(digest(Path(path).read_bytes()) == expected, 'input changed: ' + path)
    report = dict(status='PASS', checker_sha256=digest(Path(__file__).read_bytes()),
                  pypdf_version=pypdf.__version__, unicode_database=unicodedata.unidata_version,
                  protocol_sha256=PROTOCOL_HASH, author_manifest_sha256=MANIFEST_HASH,
                  fresh_report_sha256=digest((replay/'report.json').read_bytes()),
                  input_hashes=inputs, inputs_unchanged=True, source_documents=source,
                  nine_source_specifications_field_identical=True,
                  source_body_sums=sums, full_replacement_metrics=metrics, lower_bounds=ratios,
                  zero_credit_sources=['N001','L108'], exact_eleven_source_factor=None,
                  full_programs=5, full_program_bytes=sum(s['bytes'] for s in p['certificate_programs']),
                  all_11_code_blocks_complete_in_order=True, math_code_table_AST_unchanged=True,
                  qed_marks=75, raster_sha256=raster_hashes,
                  helper_imports=False, source_fulltext_exported=False,
                  mathematical_or_GAP_reproof=False, annotations_included=False)
    with args.output.open('x') as stream:
        json.dump(report, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps(dict(status='PASS', inputs=len(inputs), pages=57,
                         NFC=ratios['NFC']['whitespace_tokens'],
                         report_sha256=digest(args.output.read_bytes())), indent=2))


if __name__ == '__main__':
    main()
