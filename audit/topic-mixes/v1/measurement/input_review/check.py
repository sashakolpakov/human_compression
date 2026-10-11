#!/usr/bin/env python3
"""Independent complete-document recount; no author arithmetic is imported."""
import argparse
import hashlib
import json
import re
import unicodedata
from copy import deepcopy
from pathlib import Path
from pypdf import PdfReader

PIN = '3f02f43dd6e0037cfded61d4b3096b69a8412eeba669ec5714ea1190a24990a8'
SCIENCE = 'cf6f5e47347a0f905a2f4a566439b3d3562164a5827ef8e7467fa2bb37c28b96'


def need(value, message):
    if not value:
        raise ValueError(message)


def load(path):
    return json.loads(path.read_text())


def digest(data):
    return hashlib.sha256(data).hexdigest()


def metrics(text, normalization):
    text = unicodedata.normalize(normalization, text)
    words = text.split()
    collapsed = ' '.join(words)
    runs = 0
    previous = False
    for character in text:
        current = character.isalnum()
        if current and not previous:
            runs += 1
        previous = current
    return dict(whitespace_tokens=len(words), alphanumeric_units=runs,
                characters_without_whitespace=sum(len(word) for word in words),
                characters_with_collapsed_whitespace=len(collapsed),
                utf8_bytes_with_collapsed_whitespace=len(collapsed.encode()),
                collapsed_text_sha256=digest(collapsed.encode()))


def bound(row, source_root, public_root):
    base = {'sources': source_root, 'public': public_root}[row['root']]
    path = base / row['path']
    data = path.read_bytes()
    need(len(data) == row['bytes'] and digest(data) == row['sha256'], 'changed entire input')
    return path, data


def scope(policy):
    need(policy['source_id'] == 'F005' and policy['source']['pages'] == 21
         and policy['original_manuscripts'] == 1 and policy['source_rows'] == 35
         and policy['source_questions_excluded'] == 3, 'one original, complete corrected contract')
    need(set(policy['replacements']) == {'U', 'A1', 'A2', 'CODE1', 'CODE2'}
         and [policy['replacements'][k]['pages'] for k in ['U', 'A1', 'A2', 'CODE1', 'CODE2']]
         == [5, 8, 4, 4, 3], 'all complete papers and programs')
    need(policy['whole_common_papers_charged'] and policy['whole_additive_application_charged']
         and policy['all_declared_code_prepurchased_for_conditional_results']
         and policy['raw_and_printed_code_are_alternatives']
         and not policy['cross_topic_discount'] and not policy['overlap_discount'], 'full cost boundary')
    need(len(policy['programs']) == 3 and len(policy['drivers']) == 3 and len(policy['formal']) == 1,
         'all seven complete raw files')
    need(policy['scientific_acceptance']['root_manifest_sha256'] == SCIENCE
         and policy['partial_formal_declarations'] == 2 and not policy['whole_source_formalized'],
         'exact science and partial formalization')
    need(policy['primary'].startswith('NFC characters_without_whitespace in raw_untrimmed entire documents,')
         and policy['variants'] == ['raw_untrimmed', 'raw_selected', 'calibrated_selected']
         and policy['normalizations'] == ['NFC', 'NFKC'], 'primary and all sensitivities')
    need(set(policy['unknown_costs']) == {'full_graphics', 'historical_software',
                                        'retained_external_proofs', 'full_formalization'}
         and all(v is None for v in policy['unknown_costs'].values()), 'unknown is not zero')


def raw_document(path):
    texts, all_fonts, page_records = [], [], []
    at = 0
    for number, page in enumerate(PdfReader(path).pages, 1):
        chunks, fonts = [], []
        def visitor(text, cm, tm, font, size):
            chunks.append(text)
            fonts.extend([str(font.get('/BaseFont', font.get('/Name', ''))) if font else ''] * len(text))
        text = page.extract_text(visitor_text=visitor) or ''
        need(text == ''.join(chunks) and len(text) == len(fonts), 'ordinary extraction/font alignment')
        page_records.append(dict(page=number, start=at, end=at + len(text),
                                 sha256=digest(text.encode()), empty_extraction=not text))
        texts.append(text)
        all_fonts.extend(fonts + [''])
        at += len(text) + 1
    return '\n'.join(texts), all_fonts[:-1], page_records


def edited(raw, replacements):
    cursor = 0
    out = []
    for start, end, value in sorted(replacements):
        need(cursor <= start < end <= len(raw), 'disjoint literal edits')
        out += [raw[cursor:start], value]
        cursor = end
    return ''.join(out) + raw[cursor:]


def recount(packet, source_root, public_root):
    policy = load(packet / 'policy.json')
    scope(policy)
    spec = load(packet / 'input_spec.json')
    aliases = load(packet / 'glyph_aliases.json')['aliases']
    need(len(aliases) == 9 and all(a['document'] == 'F005' for a in aliases), 'exact nine observed aliases')
    documents, raw_texts, total_aliases = {}, {}, 0
    for key, row in {'F005': policy['source'], **policy['replacements']}.items():
        path, _ = bound(row, source_root, public_root)
        raw, fonts, pages = raw_document(path)
        record = spec[key]
        need(pages == record['page_bindings'] and len(pages) == row['pages']
             and digest(raw.encode()) == record['extraction_sha256'], 'whole ordinary extracted text')
        need(record['included_spans'] == [dict(start=0, end=len(raw), sha256=digest(raw.encode()))],
             'entire source or replacement retained')
        cuts = []
        for page in pages:
            text = raw[page['start']:page['end']]
            match = re.search(r'(?:^|\n)' + str(page['page']) + r'\s*\Z', text)
            need(match is not None, 'isolated physical page number')
            start = page['start'] + match.start() + (text[match.start()] == '\n')
            cuts.append(dict(page=page['page'], start=start, end=page['end'],
                             literal=raw[start:page['end']], sha256=digest(raw[start:page['end']].encode())))
        need(cuts == record['excluded_furniture'], 'only declared physical footer removed')
        alias_map = {(a['font'], a['input']): a for a in aliases if a['document'] == key}
        changes = []
        for i, character in enumerate(raw):
            alias = alias_map.get((fonts[i], character))
            if alias:
                changes.append((i, i + 1, alias['output']))
        declared = [(g['start'], g['end'], g['output']) for g in record['glyph_substitutions']]
        need(changes == declared, 'each observed font/character occurrence substituted once')
        for alias in alias_map.values():
            count = sum(fonts[i] == alias['font'] and c == alias['input'] for i, c in enumerate(raw))
            need(count == alias['occurrences'], 'observed alias multiplicity')
        footer_edits = [(c['start'], c['end'], '\n') for c in cuts]
        variants = dict(raw_untrimmed=raw, raw_selected=edited(raw, footer_edits),
                        calibrated_selected=edited(raw, footer_edits + changes))
        documents[key] = dict(pdf_sha256=row['sha256'], pages=len(pages), furniture_cuts=len(cuts),
                              glyph_repairs=len(changes), metrics={v: {n: metrics(t, n) for n in ['NFC', 'NFKC']}
                                                                  for v, t in variants.items()})
        raw_texts[key] = variants['raw_selected']
        total_aliases += len(changes)
    need(total_aliases == 1210, 'complete alias occurrences')
    raw_files = {}
    for category in ['programs', 'drivers', 'formal']:
        raw_files[category] = {}
        for row in policy[category]:
            _, data = bound(row, source_root, public_root)
            raw_files[category][row['path']] = dict(bytes=len(data), sha256=digest(data), role=row['role'],
                                                   metrics={n: metrics(data.decode(), n) for n in ['NFC', 'NFKC']})
    for code in ['CODE1', 'CODE2']:
        text = ''.join(unicodedata.normalize('NFKC', raw_texts[code]).split())
        rows = [r for r in policy['programs'] if r['printed_document'] == code]
        for row in rows:
            _, data = bound(row, source_root, public_root)
            complete = ''.join(unicodedata.normalize('NFKC', data.decode()).split())
            need(complete in text, 'whole literal program printed')
    return documents, raw_files


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packet', type=Path, required=True)
    p.add_argument('--sources-root', type=Path, required=True)
    p.add_argument('--public-root', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    need(not a.out.exists(), 'fresh output')
    a.out.mkdir(parents=True)
    need(digest((a.packet / 'manifest.json').read_bytes()) == PIN, 'exact reviewed input edition')
    for row in load(a.packet / 'manifest.json')['exports']:
        data = (a.packet / row['path']).read_bytes()
        need(len(data) == row['bytes'] and digest(data) == row['sha256'], 'unchanged frozen input export')
    documents, raw_files = recount(a.packet, a.sources_root, a.public_root)
    author = load(a.packet / 'author_counts.json')
    need(documents == author['documents'] and raw_files == author['raw_files'], 'all independent counts agree')
    controls = []
    for name, action in [
        ('omit_exceptional_application', lambda q: q['replacements'].pop('A2')),
        ('omit_validation_program', lambda q: q['programs'].pop()),
        ('discount_common_theory', lambda q: q.__setitem__('whole_common_papers_charged', False)),
        ('discount_prior_correction', lambda q: q.__setitem__('whole_additive_application_charged', False)),
        ('unknown_graphics_as_zero', lambda q: q['unknown_costs'].__setitem__('full_graphics', 0)),
        ('claim_final_problem_answers', lambda q: q.__setitem__('source_questions_excluded', 0))]:
        damaged = deepcopy(load(a.packet / 'policy.json'))
        action(damaged)
        try:
            scope(damaged)
        except (ValueError, KeyError):
            controls.append(name)
        else:
            raise ValueError('scope corruption accepted')
    report = dict(status='PASS_DISTINCT_COMPLETE_F005_INPUTS', input_manifest_sha256=PIN,
                  author_arithmetic_imports=False, PDFs=6, pages=45, PDF_metric_cells=180,
                  raw_files=7, raw_metric_cells=70, ordinary_extraction_and_fonts_recounted=True,
                  aliases=9, alias_occurrences=1210, all_programs_printed=True,
                  glyph_byte_and_outline_parser='Shared previously reviewed helper; separately replayed, not a second parser implementation.',
                  rejected_scope_controls=controls, factors_evaluated=False,
                  original_credit=0, new_question_credit=0, full_source_formalized=False)
    (a.out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    (a.out / 'counts.json').write_text(json.dumps(dict(documents=documents, raw_files=raw_files), indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
