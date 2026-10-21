#!/usr/bin/env python3
"""Distinct full-document counting; the existing PDF glyph parser is shared.

No author metric, selection, calibration, or arithmetic function is imported.
The byte-to-outline parser and synthetic-newline instrumentation are reused
explicitly; their results are checked against ordinary extraction here.
"""
import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from copy import deepcopy
from pathlib import Path
from pypdf import PdfReader

PIN = '4835714ae78f8069a7b53f6181b770a2b40286eadf8a2c53cc652b96c4ccea0a'
SCIENCE = '2d460b6a74eeef341b8bcd9a4153168b97e2e02cef56fcf4556562e20a6562b9'
UNITS = ['whitespace_tokens', 'alphanumeric_units', 'characters_without_whitespace',
         'characters_with_collapsed_whitespace', 'utf8_bytes_with_collapsed_whitespace']
CATEGORIES = ['programs', 'operational_drivers', 'formal_files']
PROGRAMS = {'central_lift.g', 'cyclotomic_carries.g', 'modularity_probe.g',
            'phase236_finite_check.g', 'phase236_models.py', 'phase248_presentation_check.g',
            'regular_byproducts.g', 'small_order_probe.g', 'verify_lift_normalforms.py'}


def need(value, message):
    if not value:
        raise ValueError(message)


def load(path):
    return json.loads(path.read_text())


def sha(data):
    return hashlib.sha256(data).hexdigest()


def bound(root, row):
    path = Path(row['path'])
    need(not path.is_absolute() and '..' not in path.parts, 'relative input path')
    data = (root / path).read_bytes()
    need(len(data) == row['bytes'] and sha(data) == row['sha256'], 'bound complete input ' + str(path))
    return root / path, data


def metric(text, normalization):
    text = unicodedata.normalize(normalization, text)
    tokens = text.split()
    collapsed = ' '.join(tokens)
    previous = False
    runs = 0
    for char in text:
        current = char.isalnum()
        if current and not previous:
            runs += 1
        previous = current
    return dict(whitespace_tokens=len(tokens), alphanumeric_units=runs,
                characters_without_whitespace=sum(map(len, tokens)),
                characters_with_collapsed_whitespace=len(collapsed),
                utf8_bytes_with_collapsed_whitespace=len(collapsed.encode()),
                normalized_text_sha256=sha(text.encode()), collapsed_text_sha256=sha(collapsed.encode()))


def scope(p):
    need(p['source_ids'] == ['L014', 'L007'] and p['original_count'] == 2 and
         (p['source_dispositions'], p['inherited_L014_rows'], p['L007_rows']) == (63, 25, 38),
         'complete two-original scientific contract')
    need({k: r['pages'] for k, r in p['documents'].items()} ==
         dict(L014=12, L007=22, U=7, A1=5, A2=6, CODE=9), 'all61 physical pages')
    need(p['whole_common'] == ['U'] and p['written_documents'] == ['U', 'A1', 'A2'] and
         p['applications'] == {'L014': ['A1'], 'L007': ['A2']} and
         p['programme_printed_alternative'] == ['CODE'], 'entire shared and local papers')
    need(len(p['programs']) == 9 and {Path(r['path']).name for r in p['programs']} == PROGRAMS and
         all(r['logical_role'] == 'validation_not_uniform_proof_premise' for r in p['programs']),
         'nine complete declared validation programs')
    need(len(p['operational_drivers']) == 4 and len(p['formal_files']) == 3 and
         all(r['whole_file'] for cat in CATEGORIES for r in p[cat]), 'whole raw files and separate drivers')
    need([r['declarations'] for r in p['formal_files']] == [5, 4, 3] and
         not any(r['source_specific_instance'] for r in p['formal_files']) and
         (p['formal_declarations'], p['new_formal_declarations']) == (12, 3), 'partial formal scope')
    need(p['primary_coordinate'] == dict(variant='raw_untrimmed', normalization='NFC',
                                         unit='characters_without_whitespace') and
         p['normalizations'] == ['NFC', 'NFKC'] and p['units'] == UNITS and
         p['variants'] == ['raw_untrimmed', 'raw_selected', 'calibrated_selected'], 'fixed primary and sensitivities')
    need('entire U and all nine complete' in p['conditional_policy'] and
         'no program is a uniform proof premise' in p['conditional_policy'] and
         not p['cross_topic_discount'] and not p['old_Topic_F_common_free_premise'], 'full acquisition')
    need(set(p['unknown_costs']) == {'full_retained_CP_proof', 'full_Huppert_Schmidt_proofs',
         'classical_external_proofs', 'source_graphics_and_formula_layout',
         'complete_runtime_and_external_software', 'operational_engineering'} and
         all(v is None for v in p['unknown_costs'].values()), 'unmeasured costs remain unknown')
    need(p['ratio'] is None and not p['factors_permitted'] and
         p['new_source_credit'] == p['new_question_credit'] == 0, 'input stage adds no credit')


def ordinary_document(path, key):
    parts, fonts, pages, duplicate_pages = [], [], [], []
    offset = 0
    for n, page in enumerate(PdfReader(path).pages, 1):
        chunks, local = [], []
        def visitor(text, cm, tm, font, size):
            # L007's fontless callback repeats the immediately preceding Form text.
            if key == 'L007' and font is None and text == 'Accepted manuscript' and chunks[-1:] == [text]:
                duplicate_pages.append(n)
                return
            chunks.append(text)
            local.extend([str(font.get('/BaseFont', font.get('/Name', ''))) if font else ''] * len(text))
        text = page.extract_text(visitor_text=visitor) or ''
        need(text == ''.join(chunks) and len(text) == len(local), 'ordinary text/font alignment')
        pages.append(dict(page=n, start=offset, end=offset + len(text), sha256=sha(text.encode()),
                          empty_extraction=not text))
        parts.append(text)
        fonts.extend(local + [''])
        offset += len(text) + 1
    need(duplicate_pages == (list(range(1, 23)) if key == 'L007' else []), 'exact watermark callback scope')
    raw = '\n'.join(parts)
    need(raw == '\n'.join(p.extract_text() or '' for p in PdfReader(path).pages), 'ordinary returned text unchanged')
    if key == 'L007':
        need(raw.count('Accepted manuscript') == 22, '22 watermarks retained by primary')
    return raw, fonts[:-1], pages


def footer_spans(key, raw, pages):
    spans = []
    for pg in pages:
        n = pg['page']
        text = raw[pg['start']:pg['end']]
        local = []
        if key == 'L007':
            need(text.startswith('Accepted manuscript\n'), 'literal watermark')
            local.append((0, 20))
            if n > 1:
                header = (f'{n} Ars Math. Contemp.\n' if n % 2 == 0 else
                          f'T.-T. Konget al.: Chiral 3-polytopes of order 2pm {n}\n')
                need(text[20:].startswith(header), 'literal alternating source header')
                local.append((20, 20 + len(header)))
        elif key == 'L014' and n > 1:
            last_name = 'HAI-PE NG QU' if n < 10 else 'HAI-P ENG QU'
            header = (f'{n} DONG-DONG HOU, YAN-QUAN FENG, DIMITRI LEEMANS, AND {last_name}\n'
                      if n % 2 == 0 else f'STRING C-GROUPS OF ORDER 4 pm {n}\n')
            need(text.startswith(header), 'literal prior-source header')
            local.append((0, len(header)))
        else:
            need(text.endswith('\n' + str(n)), 'isolated physical page number')
            local.append((len(text) - len(str(n)), len(text)))
        for a, b in local:
            a += pg['start']; b += pg['start']
            spans.append(dict(page=n, start=a, end=b, literal=raw[a:b], sha256=sha(raw[a:b].encode())))
    return spans


def edit(raw, changes):
    cursor = 0
    result = []
    for start, end, replacement in sorted(changes):
        need(cursor <= start < end <= len(raw), 'disjoint literal changes')
        result.extend([raw[cursor:start], replacement])
        cursor = end
    return ''.join(result) + raw[cursor:]


def recount(packet, study):
    p = load(packet / 'policy.json'); scope(p)
    for row in p['scientific_bindings'] + load(packet / 'science_adoption.json')['bindings']:
        bound(study, row)
    need(load(packet / 'science_adoption.json')['root_manifest_sha256'] == SCIENCE, 'accepted scientific edition')
    need(sha((packet / 'policy.json').read_bytes()) == load(packet / 'policy_freeze.json')['policy_sha256'],
         'unchanged policy fixed before counts')
    spec = load(packet / 'input_spec.json')
    aliases = load(packet / 'glyph_aliases.json')['aliases']
    need(len(aliases) == 37 and sum(a['occurrences'] for a in aliases) == 780, 'fixed glyph sensitivities')
    sys.path.insert(0, str(packet))
    from font_tools import actual_event_alignment
    from pdf_text import extract as shared_instrumented_extract
    docs, texts, audits = {}, {}, {}
    for key, row in p['documents'].items():
        path, _ = bound(study, row)
        raw, fonts, pages = ordinary_document(path, key)
        recorded = spec[key]
        need(pages == recorded['page_bindings'] and len(pages) == row['pages'] and
             sha(raw.encode()) == recorded['extraction_sha256'], 'complete actual PDF extraction')
        need(recorded['included_spans'] == [dict(start=0, end=len(raw), sha256=sha(raw.encode()))],
             'all primary text included')
        cuts = footer_spans(key, raw, pages)
        need(cuts == recorded['excluded_furniture'], 'only exact furniture omitted in sensitivity')
        rich_raw, rich_fonts, rich_pages, metadata = shared_instrumented_extract(path, 'L007' if key == 'L007' else False)
        need((raw, fonts, pages) == (rich_raw, rich_fonts, rich_pages) and
             metadata == recorded['extraction_metadata'], 'shared metadata agrees with independent ordinary extraction')
        events, audit = actual_event_alignment(path, raw, fonts, pages, type1_math_only=True,
                                               generated_newline_offsets=set(metadata['generated_newline_offsets']))
        audits[key] = audit
        amap = {(a['font_identity'], a['encoded_byte'], a['glyph_name']): a for a in aliases if a['source'] == key}
        need(len(amap) == sum(a['source'] == key for a in aliases), 'unambiguous actual encoded classes')
        changes = []
        multiplicities = Counter()
        for offset, event in sorted(events.items()):
            alias_key = (event['font_identity'], event['encoded_byte'], event['glyph_name'])
            if alias_key not in amap:
                continue
            a = amap[alias_key]
            need(event['font_dictionary_object'] == a['font_dictionary_object'] and
                 event['font_stream_sha256'] == a['font_stream_sha256'] and
                 raw[offset] == a['input'] and len(a['output']) == 1, 'actual byte/class calibration')
            need(offset not in metadata['generated_newline_offsets'], 'no synthetic newline becomes a glyph')
            changes.append((offset, offset + 1, a['output']))
            multiplicities[alias_key] += 1
        need(all(multiplicities[k] == a['occurrences'] for k, a in amap.items()), 'all actual alias occurrences')
        declared = [(g['offset'], g['offset'] + 1, g['output']) for g in recorded['glyph_substitutions']]
        need(changes == declared, 'calibration constructed from actual events agrees')
        for g in recorded['glyph_substitutions']:
            need(events[g['offset']] == g['pdf_event'] and fonts[g['offset']] == g['input_font'] and
                 sha(raw[g['context_start']:g['context_end']].encode()) == g['context_sha256'], 'exact occurrence context')
        cut_changes = [(r['start'], r['end'], '\n') for r in cuts]
        variants = dict(raw_untrimmed=raw, raw_selected=edit(raw, cut_changes),
                        calibrated_selected=edit(raw, cut_changes + changes))
        docs[key] = dict(pdf_sha256=row['sha256'], pages=len(pages), furniture_cuts=len(cuts),
                         glyph_repairs=len(changes), metrics={v: {n: metric(t, n) for n in ['NFC', 'NFKC']}
                                                             for v, t in variants.items()})
        texts[key] = variants
    need(audits == load(packet / 'font_audit.json'), 'fresh shared actual-font audit preserved')
    raw_files = {}
    for category in CATEGORIES:
        raw_files[category] = {}
        for r in p[category]:
            _, data = bound(study, r)
            raw_files[category][r['path']] = dict(bytes=len(data), sha256=sha(data),
                                                   metrics={n: metric(data.decode(), n) for n in ['NFC', 'NFKC']})
    tex = (study / 'topic_F_L007_recovery/volume/program-appendix.tex').read_text()
    names = re.findall(r'\\VerbatimInput(?:\[[^\]]*\])?\{([^}]+)\}', tex)
    need(len(names) == 9 and set(names) == {'programs/' + name for name in PROGRAMS} and
         not any(s in tex for s in ['firstline', 'lastline', 'firstnumber', 'lastnumber']), 'whole printing directives')
    compact = lambda t: ''.join(unicodedata.normalize('NFKC', t).split())
    printed = compact(texts['CODE']['raw_selected'])
    for mark in ['↪', '↩', '⌋']:
        printed = printed.replace(mark, '')
    for r in p['programs']:
        _, data = bound(study, r)
        need(not any(mark in data.decode() for mark in ['↪', '↩', '⌋']) and
             printed.count(compact(data.decode())) == 1, 'one entire file in printed appendix')
    previous = load(packet / 'prior_source_comparison.json')
    _, old_bytes = bound(study, previous['prior'])
    old = json.loads(old_bytes)['documents']['L014']['variants']
    for v, ns in old.items():
        for n, ms in ns.items():
            for k, value in ms.items():
                need(docs['L014']['metrics'][v][n][k] == value, 'unchanged prior-source coordinate')
    return docs, raw_files


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--packet', type=Path, required=True)
    ap.add_argument('--study-root', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    need(not args.out.exists(), 'fresh result directory')
    args.out.mkdir(parents=True)
    need(sha((args.packet / 'manifest.json').read_bytes()) == PIN, 'frozen author input edition')
    for row in load(args.packet / 'manifest.json')['exports']:
        bound(args.packet, row)
    docs, raw_files = recount(args.packet, args.study_root)
    expected = load(args.packet / 'author_counts.json')
    need(docs == expected['documents'] and raw_files == expected['raw_files'], 'all340 metric cells agree')
    controls = []
    for name, mutation in [
        ('omit_L014', lambda p: p['documents'].pop('L014')),
        ('omit_L007', lambda p: p['documents'].pop('L007')),
        ('omit_cyclic_lift', lambda p: p['programs'].pop(0)),
        ('omit_application', lambda p: p['applications'].pop('L007')),
        ('discount_old_common', lambda p: p.__setitem__('old_Topic_F_common_free_premise', True)),
        ('cross_topic_discount', lambda p: p.__setitem__('cross_topic_discount', True)),
        ('truncate_appendix', lambda p: p['documents']['CODE'].__setitem__('pages', 8)),
        ('claim_whole_formalization', lambda p: p['formal_files'][0].__setitem__('source_specific_instance', True)),
        ('unknown_retained_proof_as_zero', lambda p: p['unknown_costs'].__setitem__('full_retained_CP_proof', 0)),
        ('change_primary_after_counts', lambda p: p['primary_coordinate'].__setitem__('variant', 'calibrated_selected')),
        ('finite_samples_as_uniform_proof', lambda p: p['programs'][0].__setitem__('logical_role', 'uniform_proof')),
        ('new_question_credit', lambda p: p.__setitem__('new_question_credit', 1))]:
        damaged = deepcopy(load(args.packet / 'policy.json'))
        mutation(damaged)
        try:
            scope(damaged)
        except (ValueError, KeyError):
            controls.append(name)
        else:
            raise ValueError('Invalid scope accepted: ' + name)
    report = dict(status='PASS_DISTINCT_EXPANDED_F_INPUTS', input_manifest_sha256=PIN,
                  source_originals=2, PDFs=6, physical_pages=61, PDF_metric_cells=180,
                  raw_files=16, raw_metric_cells=160, unchanged_L014_coordinates=30,
                  glyph_alias_classes=37, glyph_alias_occurrences=780,
                  source_font_dictionaries=50, encoded_source_classes=1140,
                  author_metric_imports=False, shared_glyph_parser=True,
                  ordinary_extraction_independently_checked=True, whole_programs_printed=9,
                  rejected_scope_controls=controls, factors_computed=False,
                  new_original_credit=0, new_question_credit=0)
    (args.out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    (args.out / 'counts.json').write_text(json.dumps(dict(documents=docs, raw_files=raw_files), indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
