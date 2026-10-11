#!/usr/bin/env python3
"""Portable full-document counts and declared font calibration; no factors."""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import re
import unicodedata
import pypdf

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError('TOPIC_B_MEASUREMENT_REJECT: ' + message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def metrics(text, form):
    text = unicodedata.normalize(form, text)
    collapsed = ' '.join(text.split())
    return dict(whitespace_tokens=len(collapsed.split()),
        alphanumeric_units=len(re.findall(r'[^\W_]+', text)),
        characters_without_whitespace=sum(not c.isspace() for c in text),
        characters_with_collapsed_whitespace=len(collapsed),
        utf8_bytes_with_collapsed_whitespace=len(collapsed.encode()),
        collapsed_text_sha256=sha(collapsed.encode()))


def selected(raw, row):
    parts = []
    for span in row['included_spans']:
        start = span['start']
        for f in row['excluded_furniture']:
            if span['start'] <= f['start'] < f['end'] <= span['end']:
                parts.append(raw[start:f['start']])
                start = f['end']
        parts.append(raw[start:span['end']])
    return '\n'.join(parts)


def authorized(c, output, font):
    hooks = {'\uf8eb': '⎛', '\uf8ed': '⎝', '\uf8f6': '⎞', '\uf8f8': '⎠'}
    if 'CMEX' in font and c in hooks:
        return output == hooks[c]
    return 'LCIRCLE' in font and c == 'i' and output == '○'


def calibrate(raw, row, fonts):
    chars, seen = list(raw), set()
    for glyph in row['glyph_substitutions']:
        at = glyph['offset']
        need(at not in seen, 'no repeated substitution')
        seen.add(at)
        original = chr(int(glyph['input_codepoint'][2:], 16))
        need(raw[at] == original and fonts[at] == glyph['input_font'], 'actual source font/glyph')
        need(len(glyph['output']) == 1 and authorized(original, glyph['output'], fonts[at]),
             'one authorized visible Unicode glyph; no deletion')
        page = row['page_bindings'][glyph['page'] - 1]
        need(at == page['start'] + glyph['page_offset'] and page['start'] <= at < page['end'],
             'glyph physical-page locator')
        a, b = glyph['context_start'], glyph['context_end']
        need(a <= at < b and sha(raw[a:b].encode()) == glyph['context_sha256'], 'exact context')
        chars[at] = glyph['output']
    for i, c in enumerate(raw):
        bad = ((ord(c) < 32 and c not in '\n\r\t') or
               unicodedata.category(c) == 'Co' or c == '\ufffd')
        need(not bad or i in seen, 'every control/private-use glyph classified')
        if 'LCIRCLE' in fonts[i] and not c.isspace():
            need(i in seen, 'every printable circle-font alias classified')
    return ''.join(chars)


def document(study, key, row):
    pdf = study / row['path']
    need(sha(pdf.read_bytes()) == row['pdf_sha256'], 'bound PDF ' + key)
    pages, texts, fonts = [], [], []
    at = 0
    for number, page in enumerate(pypdf.PdfReader(pdf).pages, 1):
        pieces, local = [], []

        def visitor(text, cm, tm, font, size):
            pieces.append(text)
            local.extend([str(font.get('/BaseFont', '')) if font else ''] * len(text))

        text = page.extract_text(visitor_text=visitor) or ''
        need(text == ''.join(pieces) and len(text) == len(local), 'font alignment ' + key)
        pages.append(dict(page=number, start=at, end=at + len(text),
                          sha256=sha(text.encode()), empty_extraction=not text))
        at += len(text) + 1
        texts.append(text)
        fonts.extend(local)
        fonts.append('')
    raw = '\n'.join(texts)
    fonts = fonts[:-1]
    need(len(pages) == row['pages'] and pages == row['page_bindings'], 'all physical pages ' + key)
    need(sha(raw.encode()) == row['extraction_sha256'], 'full extraction ' + key)
    need(row['included_spans'] == [dict(start=0, end=len(raw), sha256=sha(raw.encode()),
         role=row['included_spans'][0]['role'])], 'complete-document selection ' + key)
    previous = 0
    for f in row['excluded_furniture']:
        a, b = f['start'], f['end']
        need(previous <= a < b <= len(raw), 'ordered furniture')
        previous = b
        need(raw[a:b] == f['literal'] and sha(raw[a:b].encode()) == f['sha256'],
             'exact declared furniture ' + key)
    calibrated = calibrate(raw, row, fonts)
    return raw, selected(raw, row), selected(calibrated, row), fonts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--study-root', type=Path, default=HERE.parent)
    ap.add_argument('--public-root', type=Path,
                    help='Optional published replacement tree; primary sources remain under study-root.')
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(), 'fresh output directory')
    args.out.mkdir(parents=True)
    protocol_bytes = (HERE / 'protocol.json').read_bytes()
    protocol = json.loads(protocol_bytes)
    specs = {}
    for key in ('source_input_spec', 'replacement_input_spec'):
        data = (HERE / (key + '.json')).read_bytes()
        need(sha(data) == protocol[key + '_sha256'], 'frozen proposed boundary ' + key)
        specs[key] = json.loads(data)
    source, replacement = specs['source_input_spec'], specs['replacement_input_spec']
    need(pypdf.__version__ == source['pypdf_version'] == replacement['pypdf_version'] == '6.13.0',
         'pinned parser')
    need(set(source['sources']) == {'N003', 'N008', 'L030'}, 'all three acquired source PDFs')
    need(source['missing_source_pdf']['N001']['pdf_cost'] is None, 'N001 PDF remains unknown')
    need(set(replacement['ours']) == {'U_B', 'B1', 'B2', 'B3', 'B4'},
         'whole umbrella and all four applications, including B1')
    need(replacement['required_mathematical_programs'] == [], 'written uniform proof boundary')
    publication = json.loads((HERE / 'publication_binding.json').read_text())
    report, cached = {}, {}
    for key, row in (source['sources'] | replacement['ours']).items():
        actual_root, actual_row = args.study_root, row
        if args.public_root and key in replacement['ours']:
            target = publication['scientific_documents'][key]
            need(target['private_path'] == row['path'] and
                 target['pdf_sha256'] == row['pdf_sha256'], 'exact publication mapping ' + key)
            actual_row = dict(row, path=target['public_path'])
            actual_root = args.public_root
        raw, before, after, fonts = document(actual_root, key, actual_row)
        cached[key] = (raw, fonts)
        variants = {}
        for name, text in (('raw_untrimmed', raw), ('raw_selected', before),
                           ('calibrated_selected', after)):
            variants[name] = {form: metrics(text, form) for form in ('NFC', 'NFKC')}
        report[key] = dict(pdf_sha256=row['pdf_sha256'], pages=row['pages'],
            calibrated_occurrences=len(row['glyph_substitutions']), variants=variants,
            calibrated_minus_raw={form: {unit: variants['calibrated_selected'][form][unit]
                - variants['raw_selected'][form][unit] for unit in protocol['units']}
                for form in ('NFC', 'NFKC')})
    rejected = []
    for label, change in [
        ('deleted_visible_glyph', lambda r: r['glyph_substitutions'][0].update(output='')),
        ('wrong_font', lambda r: r['glyph_substitutions'][0].update(input_font='/wrong')),
        ('shifted_occurrence', lambda r: r['glyph_substitutions'][0].update(
            offset=r['glyph_substitutions'][0]['offset'] + 1))]:
        row = copy.deepcopy(source['sources']['N003'])
        change(row)
        try:
            calibrate(cached['N003'][0], row, cached['N003'][1])
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError('negative control accepted: ' + label)
    output = dict(status='PASS_PROPOSED_INPUT_COUNTS_ONLY_NOT_ADOPTED',
        protocol_sha256=sha(protocol_bytes), checker_sha256=sha(Path(__file__).read_bytes()),
        publication_binding_sha256=sha((HERE / 'publication_binding.json').read_bytes()),
        pypdf_version=pypdf.__version__, documents=report,
        source_physical_pages_available=31, replacement_scientific_pages=22,
        source_pdf_metrics_unknown={'N001': None}, four_source_pdf_total=None,
        complete_four_application_denominator_present=True, negative_controls_rejected=rejected,
        primary_text_exported=False, retained_external_costs=None, diagram_graphic_costs=None,
        ratio=None)
    (args.out / 'counts.json').write_text(json.dumps(output, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(dict(status=output['status'], documents=len(report), metric_cells=240,
                         controls=rejected, ratio=None)))


if __name__ == '__main__':
    main()
