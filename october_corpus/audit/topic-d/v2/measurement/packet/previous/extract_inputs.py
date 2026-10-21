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
from calibration import glyph_alias
from pypdf import _cmap
from pypdf.generic import ContentStream, TextStringObject, ByteStringObject

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError('TOPIC_D_MEASUREMENT_REJECT: ' + message)


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


def calibrate(raw, row, fonts, key, events):
    chars, seen = list(raw), set()
    for glyph in row['glyph_substitutions']:
        at = glyph['offset']
        need(at not in seen, 'no repeated substitution')
        seen.add(at)
        original = chr(int(glyph['input_codepoint'][2:], 16))
        need(raw[at] == original and fonts[at] == glyph['input_font'], 'actual source font/glyph')
        expected = glyph_alias(key, original, fonts[at])
        need('visitor_event_location' not in glyph, 'no invented whitespace glyph event')
        need(len(glyph['output']) == 1 and glyph['output'] == expected,
             'one authorized visible Unicode glyph; no deletion')
        page = row['page_bindings'][glyph['page'] - 1]
        need(at == page['start'] + glyph['page_offset'] and page['start'] <= at < page['end'],
             'glyph physical-page locator')
        a, b = glyph['context_start'], glyph['context_end']
        need(a <= at < b and sha(raw[a:b].encode()) == glyph['context_sha256'], 'exact context')
        chars[at] = glyph['output']
    for i, c in enumerate(raw):
        bad = ((unicodedata.category(c) == 'Cc' and c not in '\n\r\t') or
               unicodedata.category(c) == 'Co' or c == '\ufffd')
        need(not bad or i in seen, 'every control/private-use glyph classified')
        if glyph_alias(key, c, fonts[i]) is not None:
            need(i in seen, 'every declared printable or whitespace glyph alias classified')
    return ''.join(chars)


def document(study, key, row):
    pdf = study / row['path']
    need(sha(pdf.read_bytes()) == row['pdf_sha256'], 'bound PDF ' + key)
    pages, texts, fonts, events = [], [], [], {}
    at = 0
    for number, page in enumerate(pypdf.PdfReader(pdf).pages, 1):
        pieces, local = [], []

        def visitor(text, cm, tm, font, size):
            fontname = str(font.get('/BaseFont', '')) if font else ''
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
    calibrated = calibrate(raw, row, fonts, key, events)
    return raw, selected(raw, row), selected(calibrated, row), fonts, events


def actual_whitespace_audit(path):
    """Read actual text-showing bytes, independently of generated layout whitespace."""
    reader = pypdf.PdfReader(path)
    actual, whitespace = 0, []
    for pno, page in enumerate(reader.pages, 1):
        need(not page['/Resources'].get('/XObject'), 'no unvisited source text form XObjects')
        font = None
        for operands, op in ContentStream(page.get_contents(), reader).operations:
            if op == b'Tf':
                font = page['/Resources']['/Font'][operands[0]].get_object()
            if op not in (b'Tj', b'TJ', b"'", b'"'):
                continue
            need(font is not None and font.get('/Subtype') == '/Type1', 'source text font is Type1')
            parts = operands[0] if op == b'TJ' else [operands[-1]]
            encoding, cmap = _cmap.get_encoding(font)
            for part in parts:
                if not isinstance(part, (TextStringObject, ByteStringObject)):
                    continue
                data = part.original_bytes if hasattr(part, 'original_bytes') else bytes(part)
                for byte in data:
                    decoded = (encoding.get(byte, chr(byte)) if isinstance(encoding, dict)
                               else bytes([byte]).decode(encoding, errors='strict'))
                    decoded = ''.join(cmap.get(c, c) for c in decoded)
                    actual += 1
                    if decoded.isspace():
                        whitespace.append(dict(page=pno, font=str(font['/BaseFont']), encoded_byte=byte,
                            decoded_codepoints=[f'U+{ord(c):04X}' for c in decoded]))
    need(not whitespace, 'no source actual glyph decoded as whitespace: do not calibrate generated layout')
    return dict(actual_text_bytes=actual, actual_whitespace_glyphs=whitespace,
                all_extracted_whitespace_is_generated_layout=True)


REQUIRED = {'phase110_commuting_pairs_integration_finite.g', 'phase5_j2_search.g',
            'phase5_j2_fuse.g', 'phase5_j2_verify.g', 'phase4_geometry_checks.g'}
DIAGNOSTIC = {'phase110_commuting_pairs_integration_formula.py',
              'phase10_suzuki_marked_fields_check.py', 'phase10_suzuki_marked_groups_check.g'}
DRIVERS = {'phase110_commuting_pairs_integration_run.py', 'phase164_enumeration_run.py'}


def program_boundary(replacement):
    rows = replacement['complete_mathematical_programs']
    need(len(rows) == 8 and len({r['path'] for r in rows}) == 8, 'all eight distinct whole mathematical programs')
    for label, names in [('required', REQUIRED), ('diagnostic', DIAGNOSTIC)]:
        need({Path(r['path']).name for r in rows if r['classification'] == label} == names,
             'exact ' + label + ' program roster')
    drivers = replacement['complete_drivers']
    need(len(drivers) == 2 and {Path(r['path']).name for r in drivers} == DRIVERS,
         'both complete drivers separately')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--study-root', type=Path, default=HERE.parent)
    ap.add_argument('--public-root', type=Path,
                    help='Optional published replacement tree; primary PDFs remain under study-root.')
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
    for filename, key in [('policy.json', 'policy_sha256'), ('calibration.py', 'calibration_sha256'),
                          ('publication_binding.json', 'publication_binding_sha256')]:
        need(sha((HERE / filename).read_bytes()) == protocol[key], 'frozen ' + filename)
    source, replacement = specs['source_input_spec'], specs['replacement_input_spec']
    need(pypdf.__version__ == source['pypdf_version'] == replacement['pypdf_version'] == '6.13.0',
         'pinned parser')
    need(set(source['sources']) == {'L066', 'L074', 'L104'}, 'all three whole source PDFs')
    need(set(replacement['ours']) == {'U_D', 'D1', 'D2', 'D3', 'CODE'},
         'whole umbrella, all three applications, whole appendix')
    program_boundary(replacement)
    publication = json.loads((HERE / 'publication_binding.json').read_text())
    report, cached, whitespace = {}, {}, {}
    for key, row in (source['sources'] | replacement['ours']).items():
        actual_root, actual_row = args.study_root, row
        if args.public_root and key in replacement['ours']:
            target = publication['scientific_documents'][key]
            need(target['private_path'] == row['path'] and target['pdf_sha256'] == row['pdf_sha256'],
                 'exact publication mapping ' + key)
            actual_row = dict(row, path=target['public_path'])
            actual_root = args.public_root
        raw, before, after, fonts, events = document(actual_root, key, actual_row)
        cached[key] = (raw, fonts, events)
        if key in source['sources']:
            whitespace[key] = actual_whitespace_audit(actual_root / actual_row['path'])
        variants = {}
        for name, text in (('raw_untrimmed', raw), ('raw_selected', before), ('calibrated_selected', after)):
            variants[name] = {form: metrics(text, form) for form in ('NFC', 'NFKC')}
        report[key] = dict(pdf_sha256=row['pdf_sha256'], pages=row['pages'],
            calibrated_occurrences=len(row['glyph_substitutions']), furniture_occurrences=len(row['excluded_furniture']),
            variants=variants, calibrated_minus_raw={form: {unit:
                variants['calibrated_selected'][form][unit] - variants['raw_selected'][form][unit]
                for unit in protocol['units']} for form in ('NFC', 'NFKC')})
    rejected = []
    mutations = [
        ('deleted_visible_glyph', lambda r: r['glyph_substitutions'][0].update(output='')),
        ('wrong_font', lambda r: r['glyph_substitutions'][0].update(input_font='/wrong')),
        ('shifted_occurrence', lambda r: r['glyph_substitutions'][0].update(offset=r['glyph_substitutions'][0]['offset']+1)),
        ('omitted_visible_glyph', lambda r: r['glyph_substitutions'].pop()),
        ('invented_whitespace_event', lambda r: r['glyph_substitutions'][0].update(visitor_event_location=[1,0,0]))]
    for label, change in mutations:
        row = copy.deepcopy(source['sources']['L066']); change(row)
        try:
            calibrate(cached['L066'][0], row, cached['L066'][1], 'L066', cached['L066'][2])
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError('negative control accepted: ' + label)
    trial = copy.deepcopy(source['sources']['L104'])
    trial['glyph_substitutions'] = [g for g in trial['glyph_substitutions'] if g['input_codepoint'] != 'U+2710']
    try:
        calibrate(cached['L104'][0], trial, cached['L104'][1], 'L104', cached['L104'][2])
    except ValueError:
        rejected.append('omitted_printable_diagram_alias')
    else:
        raise ValueError('negative control accepted: omitted printable alias')
    trial = copy.deepcopy(source['sources']['L074'])
    raw = cached['L074'][0]
    at = raw.index('?0')
    page = next(p for p in trial['page_bindings'] if p['start'] <= at < p['end'])
    a, b = max(page['start'], at-32), min(page['end'], at+33)
    trial['glyph_substitutions'].append(dict(offset=at, page=page['page'], page_offset=at-page['start'],
        input_codepoint='U+003F', input_font=cached['L074'][1][at], output='ρ',
        context_start=a, context_end=b, context_sha256=sha(raw[a:b].encode())))
    try:
        calibrate(raw, trial, cached['L074'][1], 'L074', cached['L074'][2])
    except ValueError:
        rejected.append('literal_source_error_rewritten')
    else:
        raise ValueError('negative control accepted: literal source error rewritten')
    for label, change in [
        ('omitted_diagnostic', lambda r: r['complete_mathematical_programs'].pop(1)),
        ('diagnostic_claimed_required', lambda r: r['complete_mathematical_programs'][1].update(classification='required')),
        ('omitted_driver', lambda r: r['complete_drivers'].pop())]:
        trial = copy.deepcopy(replacement); change(trial)
        try:
            program_boundary(trial)
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError('negative control accepted: ' + label)
    programs, drivers = {}, {}
    for row in replacement['complete_mathematical_programs'] + replacement['complete_drivers']:
        path = args.public_root / row['public_path'] if args.public_root else args.study_root / row['path']
        data = path.read_bytes()
        need(sha(data) == row['sha256'] and len(data) == row['bytes'], 'whole raw program or driver')
        target = drivers if row['classification'] == 'driver' else programs
        target[Path(row['path']).name] = dict(sha256=sha(data), bytes=len(data), classification=row['classification'],
            role=row['role'], variants={form: metrics(data.decode(), form) for form in ('NFC', 'NFKC')})
    output = dict(status='PASS_PROPOSED_INPUT_COUNTS_ONLY_NOT_ADOPTED',
        protocol_sha256=sha(protocol_bytes), checker_sha256=sha(Path(__file__).read_bytes()),
        publication_binding_sha256=sha((HERE / 'publication_binding.json').read_bytes()),
        pypdf_version=pypdf.__version__, documents=report, raw_program_alternative=programs,
        full_drivers_separate=drivers, source_whitespace_audit=whitespace,
        program_boundary='Full CODE appendix once; all eight whole raw mathematical programs are an alternative, never an addition. Full two drivers separately inventoried.',
        source_physical_pages=26, replacement_scientific_pages=19, complete_program_appendix_pages=12,
        total_physical_pages=57, all_three_sources_and_applications_present=True,
        negative_controls_rejected=rejected, primary_text_exported=False,
        retained_external_costs=None, catalogue_construction_cost=None, diagram_graphic_costs=None, ratio=None)
    (args.out / 'counts.json').write_text(json.dumps(output, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps(dict(status=output['status'], documents=len(report), metric_cells=240,
                         raw_program_and_driver_cells=100, controls=rejected, ratio=None)))


if __name__ == '__main__':
    main()
